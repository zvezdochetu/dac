import os
import sys
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

CLEAN_PDF_CSS = """
/* 1. ПОКАЗЫВАЕМ ЭЛЕМЕНТЫ ТОЛЬКО ДЛЯ PDF */
.pdf-only,
.md-content .toc {
    display: block !important;
}

/* 2. СКРЫВАЕМ ВЕБ-ИНТЕРФЕЙС И КНОПКУ СКАЧИВАНИЯ */
.no-pdf, 
.md-header, 
.md-sidebar, 
.md-footer, 
.md-nav, 
.md-content__button, 
.md-search, 
.md-clipboard, 
.md-code__button {
    display: none !important;
}

/* 3. СТИЛИЗАЦИЯ ОГЛАВЛЕНИЯ [TOC] */
.pdf-only,
h2.pdf-only {
    display: block !important;
    margin-top: 40px !important;    
    margin-bottom: 20px !important; 
    font-size: 14pt !important;
    padding-left: 5px !important; /* Легкий сдвиг самого слова "Оглавление" вправо */
}

.md-content__inner .toc,
.md-typeset .toc {
    display: block !important;
    background-color: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 6px !important;
    
    /* ТАКЖЕ увеличиваем общий padding рамки (вверх, право, низ, лево) */
    padding: 24px 28px 24px 35px !important; 
    
    margin-top: 20px !important;   
    margin-bottom: 50px !important; 
}

/* Скрываем заголовок H1 из оглавления */
.md-typeset .toc > ul > li > a {
    display: none !important;
}

/* ГАРАНТИРОВАННО СДВИГАЕМ СПИСОК ВПРАВО ОТ ЛЕВОГО КРАЯ/БЛОКА */
.md-typeset .toc ul {
    padding-left: 15px !important; /* Вот этот параметр отодвинет весь текст вправо */
    margin-left: 0 !important;
    list-style-type: none !important;
}

.md-typeset .toc li {
    padding-left: 0 !important;
    margin-left: 0 !important;
    margin-bottom: 10px !important; 
    list-style-type: none !important;
}

.md-typeset .toc li:last-child {
    margin-bottom: 0 !important;
}

.md-typeset .toc a {
    color: #334155 !important;
    font-size: 11pt !important;
    text-decoration: none !important;
}

/* 4. ЗАПРЕТ РАЗРЫВА БЛОКОВ МЕЖДУ СТРАНИЦАМИ */
.md-typeset .highlight,
.md-typeset pre,
.md-typeset .toc,
.md-typeset table,
.md-typeset blockquote,
.md-typeset .admonition {
    break-inside: avoid !important;
    page-break-inside: avoid !important;
}

.md-typeset h1, 
.md-typeset h2, 
.md-typeset h3, 
.md-typeset h4 {
    break-after: avoid !important;
    page-break-after: avoid !important;
}

/* 5. УМНАЯ ОБРАБОТКА ССЫЛОК */
.md-typeset a[href^="http://"], 
.md-typeset a[href^="https://"] {
    color: #2563eb !important;
    text-decoration: underline !important;
}

.md-typeset a[href^="#"] {
    color: #0f172a !important;
    text-decoration: none !important;
}

.md-typeset a:not([href^="http://"]):not([href^="https://"]):not([href^="#"]):not([href*="takeaway.pdf"]) {
    color: inherit !important;
    text-decoration: none !important;
    pointer-events: none !important;
    cursor: default !important;
}

/* 6. БАЗОВАЯ ТИПОГРАФИКА И ВЕРСТКА (Инженерный стиль Fira) */
body, .md-typeset {
    /* Если в системе есть Fira Sans — берем его, если нет — чистый современный системный шрифт */
    font-family: "Fira Sans", "Segoe UI", system-ui, -apple-system, sans-serif !important;
    font-size: 10.5pt !important; 
    line-height: 1.6 !important;
    color: #1e293b !important;
}

.md-typeset h1, .md-typeset h2, .md-typeset h3 {
    font-weight: 700 !important;
    color: #0f172a !important;
    letter-spacing: -0.01em !important;
}

/* 7. ИНЛАЙН-КОД */
.md-typeset :not(pre) > code {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 4px !important;
    padding: 2px 6px !important;
    font-family: "Fira Code", Consolas, Monaco, monospace !important;
    font-size: 0.85em !important;
}

/* 8. БЛОКИ КОДА */
.md-typeset .highlight code,
.md-typeset pre code {
    font-family: "Fira Code", Consolas, Monaco, monospace !important;
    font-size: 0.85em !important;
    line-height: 1.5 !important;
    color: #0f172a !important;
    white-space: pre-wrap !important;
    word-break: break-all !important;
}
"""

class TargetDirectoryHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        self.target_dir = directory
        super().__init__(*args, **kwargs)

    def translate_path(self, path):
        path = super().translate_path(path)
        rel_path = os.path.relpath(path, os.getcwd())
        return os.path.join(self.target_dir, rel_path)

    def log_message(self, format, *args):
        pass

def run_temporary_server(site_dir, port):
    handler = lambda *args, **kwargs: TargetDirectoryHTTPRequestHandler(*args, directory=site_dir, **kwargs)
    server = HTTPServer(('127.0.0.1', port), handler)
    server.serve_forever()

def on_post_build(config):
    if 'serve' in sys.argv:
        print("[PDF Hook] Режим 'mkdocs serve' — генерация PDF пропущена.")
        return

    site_dir = os.path.abspath(config['site_dir'])
    PORT = 8555
    
    server_thread = threading.Thread(
        target=run_temporary_server, 
        args=(site_dir, PORT), 
        daemon=True
    )
    server_thread.start()

    TARGET_PAGES = [
        ("takeaway/index.html", "takeaway.pdf"),
        ("cheatsheet/index.html", "cheatsheet.pdf"), 
    ]

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for rel_html_path, pdf_filename in TARGET_PAGES:
                html_path = os.path.join(site_dir, rel_html_path)
                url_path = rel_html_path

                if not os.path.exists(html_path):
                    fallback_path = rel_html_path.replace('/index.html', '.html')
                    if os.path.exists(os.path.join(site_dir, fallback_path)):
                        html_path = os.path.join(site_dir, fallback_path)
                        url_path = fallback_path
                    else:
                        print(f"[PDF Hook] Файл {html_path} не найден. Пропуск.")
                        continue

                pdf_path = os.path.join(os.path.dirname(html_path), pdf_filename)
                clean_url = url_path.lstrip('/')
                server_url = f"http://127.0.0.1:{PORT}/{clean_url}"
                
                print(f"[PDF Hook] Генерация PDF: {server_url} -> {pdf_path}")

                # Переходим на сервер и ждем полной загрузки структуры сайта
                page.goto(server_url, wait_until="networkidle")
                
                # Применяем стили оформления БЕЗ внешних сетевых инъекций скриптов
                page.add_style_tag(content=CLEAN_PDF_CSS)
                
                # Печать с автоматическим верхним колонтитулом
                page.pdf(
                    path=pdf_path,
                    format="A4",
                    margin={
                        "top": "25mm",     # Чуть увеличили верхнее поле, чтобы колонтитулу было просторно
                        "bottom": "20mm",
                        "left": "20mm",
                        "right": "20mm"
                    },
                    print_background=True,
                    
                    # Включаем отображение колонтитулов
                    display_header_footer=True,
                    
                    # HTML-шаблон для верхнего колонтитула (header)
                    header_template="""
                        <div style="
                            font-family: 'Fira Sans', 'Segoe UI', sans-serif; 
                            font-size: 8pt; 
                            color: #94a3b8; 
                            display: flex; 
                            align-items: center; 
                            justify-content: space-between; 
                            width: 100%; 
                            padding-left: 20mm; 
                            padding-right: 20mm;
                            border-bottom: 1px solid #f1f5f9;
                            padding-bottom: 5px;
                        ">
                            <!-- Левая часть: логотип и текст -->
                            <div style="display: flex; align-items: center; gap: 6px;">
                                <img src="https://documentat.io/assets/img/docio-logo-grey.svg" style="height: 12px; width: auto;" />
                                <span>Техническая документация</span>
                            </div>
                            
                            <!-- Правая часть: Название страницы (подтягивается автоматически браузером) -->
                            <div class="title" style="font-weight: 500;"></div>
                        </div>
                    """,
                    
                    # Пустой нижний колонтитул (footer), чтобы убрать стандартные системные надписи Chromium
                    footer_template="<div></div>"
                )

            browser.close()
        print("[PDF Hook] Все PDF успешно созданы!")
    except Exception as e:
        print(f"[PDF Hook] Ошибка при генерации PDF: {e}")
