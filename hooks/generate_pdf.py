import os
import sys
import threading
import base64
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

CLEAN_PDF_CSS = """
/* Явная загрузка шрифтов Fira Sans и Fira Code для Linux-раннеров */
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&family=Fira+Sans:wght@400;500;700&display=swap');

/* 1. ПОКАЗЫВАЕМ ЭЛЕМЕНТЫ ТОЛЬКО ДЛЯ PDF */
.pdf-only {
    display: block !important;
}

/* 2. СКРЫВАЕМ ВЕБ-ИНТЕРФЕЙС И КНОПКИ */
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

/* Подавляем огромный код только у спойлеров с классом .hide-code-in-pdf */
.md-typeset details.hide-code-in-pdf .admonition-content,
.md-typeset details.hide-code-in-pdf pre,
.md-typeset details.hide-code-in-pdf .highlight {
    display: none !important;
}

.md-typeset details.hide-code-in-pdf {
    height: auto !important;
    max-height: none !important;
    min-height: 0 !important;
}

/* 3. СКРЫВАЕМ ОГЛАВЛЕНИЕ ДЛЯ PDF */
h2.pdf-only,
.md-content__inner .toc,
.md-typeset .toc,
.md-content .toc {
    display: none !important;
}

/* 4. ПРАВИЛА ПЕРЕНОСА СТРАНИЦ */
.md-typeset details,
.md-typeset .admonition,
.md-typeset .admonition-content {
    break-inside: auto !important;
    page-break-inside: auto !important;
    overflow: visible !important;
    height: auto !important;
    max-height: none !important;
    min-height: 0 !important;
}

.md-typeset .highlight,
.md-typeset pre,
.md-typeset table,
.md-typeset blockquote,
.md-typeset tr,
.md-typeset img {
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

/* 5. ПОЛНЫЙ СБРОС РАМОК У ОБЫЧНЫХ DETAILS (УБИРАЕМ ЛИШНИЕ ПОЛОСЫ) */
.md-typeset details {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
    margin: 1em 0 !important;
    padding: 0 !important;
}

/* СТИЛИЗУЕМ ТОЛЬКО ПЛАШКИ ПРИМЕЧАНИЙ (ADMONITION) */
.md-typeset .admonition,
.md-typeset details.admonition {
    background-color: #f8fafc !important;
    padding: 14px 18px !important;
    margin: 1.2em 0 !important;
    border-radius: 4px !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    border-left: 3px solid #cbd5e1 !important;
}

/* Скрываем веб-маркеры и стрелки свертывания */
.md-typeset details summary::-webkit-details-marker,
.md-typeset details summary::after,
.md-typeset details summary .md-details__icon {
    display: none !important;
}

.md-typeset details summary {
    list-style: none !important;
    cursor: default !important;
}

/* Акцентные цвета левой линии */
.md-typeset .admonition.info,
.md-typeset details.admonition.info {
    border-left-color: #3b82f6 !important;
}

.md-typeset .admonition.warning,
.md-typeset details.admonition.warning {
    border-left-color: #f59e0b !important;
}

.md-typeset .admonition.note,
.md-typeset details.admonition.note {
    border-left-color: #06b6d4 !important;
}

/* Сброс внутренних отступов и фонов плашек */
.md-typeset .admonition .admonition,
.md-typeset details.admonition .admonition {
    margin: 1em 0 !important;
}

.md-typeset .admonition-content,
.md-typeset details.admonition .admonition-content {
    background: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

.md-typeset .admonition-title,
.md-typeset details.admonition summary {
    background-color: transparent !important; 
    background: transparent !important;
    margin: 0 0 10px 0 !important;
    border-bottom: none !important; 
    font-family: "Fira Sans", "Segoe UI", sans-serif !important;
    font-weight: 700 !important;
    font-size: 1em !important;
    color: #0f172a !important; 
    display: block !important; 
    position: relative !important;
    padding: 0 0 0 20px !important;
}

.md-typeset .admonition-title::before,
.md-typeset details.admonition summary::before {
    position: absolute !important;
    left: 0 !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    margin: 0 !important;
    width: 15px !important;
    height: 15px !important;
    display: inline-block !important;
}

/* 6. ССЫЛКИ */
.md-typeset a[href^="http://"], 
.md-typeset a[href^="https://"] {
    color: #1e40af !important;
    text-decoration: none !important;
    border-bottom: 1px dashed #cbd5e1 !important;
}

.md-typeset a[href^="#"] {
    color: #1e293b !important;
    text-decoration: none !important;
}

.md-typeset a:not([href^="http://"]):not([href^="https://"]):not([href^="#"]):not([href*="takeaway.pdf"]) {
    color: inherit !important;
    text-decoration: none !important;
    pointer-events: none !important;
    cursor: default !important;
}

/* 7. ТИПОГРАФИКА */
body, .md-typeset, .md-typeset p, .md-typeset li {
    font-family: "Fira Sans", "Segoe UI", system-ui, -apple-system, sans-serif !important;
    font-size: 10.5pt !important; 
    line-height: 1.6 !important;
    color: #1e293b !important;
    text-align: left !important;       /* Отменяет выравнивание по ширине */
    letter-spacing: normal !important; /* Сбрасывает растяжение букв */
    word-spacing: normal !important;   /* Возвращает естественные пробелы */
}

.md-typeset h1, .md-typeset h2, .md-typeset h3 {
    font-weight: 700 !important;
    color: #0f172a !important;
    letter-spacing: -0.01em !important;
}

/* 8. ИНЛАЙН-КОД (ИСХОДНЫЙ СТАБИЛЬНЫЙ СТИЛЬ) */
.md-typeset :not(pre) > code {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 4px !important;
    padding: 2px 6px !important;
    font-family: "Fira Code", Consolas, Monaco, monospace !important;
    font-size: 0.85em !important;
}

/* 9. БЛОКИ КОДА (ФИКС ЦЕНТРОВКИ И ВЕРХНЕГО ОТСТУПА) */
.md-typeset .highlight,
.md-typeset pre {
    background-color: #f8fafc !important;
    border-radius: 4px !important;
    margin: 0.8em 0 !important;
    padding: 0 !important;
}

.md-typeset .highlight pre,
.md-typeset pre {
    padding: 10px 14px !important;
    margin: 0 !important;
    overflow: visible !important;
}

.md-typeset .highlight code,
.md-typeset pre code {
    font-family: "Fira Code", Consolas, Monaco, monospace !important;
    font-size: 0.85em !important;
    line-height: 1.5 !important;
    color: #0f172a !important;
    white-space: pre-wrap !important;
    word-break: break-all !important;
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
    border: none !important;
    display: block !important;
}

/* 10. ГЛАВНЫЙ ЗАГОЛОВОК */
html, body {
    font-size: 10.5pt !important;
}

.md-typeset h1,
h1 {
    font-family: "Fira Sans", "Segoe UI", sans-serif !important;
    text-align: center !important;  
    font-size: 28pt !important;
    font-weight: 700 !important;
    line-height: 1.3 !important;
    margin-top: 20px !important;    
    margin-bottom: 80px !important; 
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

    svg_local_path = os.path.join(site_dir, "assets", "docio-logo-grey.svg")
    svg_base64_data = ""

    if os.path.exists(svg_local_path):
        with open(svg_local_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            svg_base64_data = f"data:image/svg+xml;base64,{encoded}"
    else:
        print(f"[PDF Hook] Предупреждение: Локальный логотип {svg_local_path} не найден!")
        svg_base64_data = "https://documentat.io"

    TARGET_PAGES = []
    
    for root, dirs, files in os.walk(site_dir):
        if any(ignored in root for ignored in [os.path.join(site_dir, "assets"), os.path.join(site_dir, "css"), os.path.join(site_dir, "js")]):
            continue
            
        for file in files:
            if file.endswith(".html"):
                full_html_path = os.path.join(root, file)
                rel_html_path = os.path.relpath(full_html_path, site_dir).replace(os.sep, '/')
                
                if file == "404.html" or "search.html" in rel_html_path:
                    continue
                
                if file == "index.html":
                    parent_folder_name = os.path.basename(root)
                    pdf_filename = "index.pdf" if root == site_dir else f"{parent_folder_name}.pdf"
                else:
                    pdf_filename = file.replace(".html", ".pdf")
                    
                TARGET_PAGES.append((rel_html_path, pdf_filename))

    print(f"[PDF Hook] Найдено страниц для конвертации: {len(TARGET_PAGES)}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for rel_html_path, pdf_filename in TARGET_PAGES:
                html_path = os.path.join(site_dir, rel_html_path)
                pdf_path = os.path.join(os.path.dirname(html_path), pdf_filename)
                
                clean_url = rel_html_path.lstrip('/')
                server_url = f"http://127.0.0.1:{PORT}/{clean_url}"
                
                print(f"[PDF Hook] Генерация PDF: {server_url} -> {pdf_path}")

                page.goto(server_url, wait_until="networkidle")
                
                page.evaluate("""() => {
                    document.querySelectorAll('details').forEach(d => {
                        d.setAttribute('open', '');
                    });
                }""")

                page.add_style_tag(content=CLEAN_PDF_CSS)
                
                # Ждем, пока браузер полностью загрузит и применит веб-шрифты
                page.evaluate("document.fonts.ready")

                page.pdf(
                    path=pdf_path,
                    format="A4",
                    margin={
                        "top": "20mm",     
                        "bottom": "20mm",
                        "left": "20mm",
                        "right": "20mm"
                    },
                    print_background=True,
                    display_header_footer=True,
                    header_template=f"""
                        <div style="
                            font-family: 'Fira Sans', 'Segoe UI', sans-serif; 
                            font-size: 8pt; 
                            color: #94a3b8; 
                            width: 100%; 
                            padding-left: 20mm; 
                            padding-right: 20mm;
                            margin-top: -5px;
                        ">
                            <div style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
                                <div style="display: flex; align-items: center;">
                                    <img src="{svg_base64_data}" style="height: 18px; width: auto; display: block;" />
                                </div>
                                <div style="font-weight: 500; display: flex; align-items: center;">
                                    Документируй как инженер: практический курс Docs as Code
                                </div>
                            </div>
                            <div style="height: 10px; width: 100%; border-bottom: 1px solid #f1f5f9;"></div>
                        </div>
                    """,
                    footer_template="<div style='font-size: 0px; height: 0px; line-height: 0px;'></div>"
                )

            browser.close()
        print(f"[PDF Hook] Все PDF успешно созданы! Всего файлов: {len(TARGET_PAGES)}")
    except Exception as e:
        print(f"[PDF Hook] Ошибка при генерации PDF: {e}")