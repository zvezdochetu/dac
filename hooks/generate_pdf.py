import os
import sys
import threading
import base64
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

CLEAN_PDF_CSS = """
/* 1. ПОКАЗЫВАЕМ ЭЛЕМЕНТЫ ТОЛЬКО ДЛЯ PDF */
.pdf-only
/* Закомментировано, чтобы оглавление не включалось принудительно:
, .md-content .toc 
*/
{
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

/* СТАЛО: Подавляем огромный код только у спойлеров с классом .hide-code-in-pdf */
.md-typeset details.hide-code-in-pdf .admonition-content,
.md-typeset details.hide-code-in-pdf pre,
.md-typeset details.hide-code-in-pdf .highlight {
    display: none !important; /* Вырезаем код при печати */
}

/* Схлопываем плашку до аккуратной полоски и запрещаем ей разрываться между листами */
.md-typeset details.hide-code-in-pdf {
    height: auto !important;
    max-height: none !important;
    min-height: 0 !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}

/* 3. СТИЛИЗАЦИЯ ОГЛАВЛЕНИЯ [TOC] */
/* ОТКЛЮЧАЕМ ОГЛАВЛЕНИЕ ДЛЯ PDF С ПОМОЩЬЮ DISPLAY: NONE */
h2.pdf-only,
.md-content__inner .toc,
.md-typeset .toc,
.md-content .toc {
    display: none !important;
}

/* НИЖЕ ВСЕ СТАРЫЕ СТИЛИ ОГЛАВЛЕНИЯ ПРОСТО ЗАКОММЕНТИРОВАНЫ БРАУЗЕРОМ И НЕ РАБОТАЮТ:

.md-content__inner .toc,
.md-typeset .toc {
    display: block !important;
    background-color: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 6px !important;
    padding: 24px 28px 24px 35px !important; 
    margin-top: 30px !important;   
    margin-bottom: 50px !important; 
}

.md-typeset .toc > ul > li > a {
    display: none !important;
}

.md-typeset .toc ul {
    padding-left: 15px !important;
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
*/

/* 4. ЗАПРЕТ РАЗРЫВА БЛОКОВ МЕЖДУ СТРАНИЦАМИ И УНИЧТОЖЕНИЕ ПУСТОТЫ */
.md-typeset .highlight,
.md-typeset pre,
.md-typeset .toc,
.md-typeset table,
.md-typeset blockquote,
.md-typeset .admonition {
    break-inside: avoid !important;
    page-break-inside: avoid !important;
}

/* Уничтожаем внутренние CSS-переменные высоты анимации MkDocs-Material */
.md-typeset details,
.md-typeset details.admonition,
.md-typeset .admonition,
.md-typeset .admonition-content,
.md-annotation__content {
    /* Сбрасываем внутренний расчет анимации раскрытия темы */
    --md-details-height: auto !important; 
    
    display: block !important;
    height: auto !important;
    max-height: none !important;
    min-height: 0 !important;
    
    /* Убираем внутренние флексы, которые не дают рамке схлопнуться */
    flex-direction: column !important; 
    overflow: visible !important;
}

/* Принудительно убираем любые фиксированные внутренние отступы у контента спойлера */
.md-typeset details .md-typeset__scrollwrap,
.md-typeset details .md-typeset__table,
.md-typeset details .highlight {
    display: block !important;
    height: auto !important;
    max-height: none !important;
    margin: 0 !important;
}

.md-typeset h1, 
.md-typeset h2, 
.md-typeset h3, 
.md-typeset h4 {
    break-after: avoid !important;
    page-break-after: avoid !important;
}

/* Подсвечиваем все блоки примечаний (admonition) легким серым фоном */
.md-typeset .admonition,
.md-typeset details.admonition {
    background-color: #f8fafc !important; /* Нежный нейтральный фон */
    padding: 16px 20px 16px 20px !important; /* Комфортные внутренние отступы */
    margin: 1.5em 0 !important;
    border-radius: 4px !important;
    
    /* Делаем саму левую линию тоньше и изящнее */
    border-left-width: 3px !important; 
}

/* Смягчаем цвета левых полос для разных типов примечаний, чтобы они не были вырвиглазными */
.md-typeset .admonition.info,
.md-typeset details.admonition.info {
    border-left-color: #3b82f6 !important; /* Спокойный, приглушенный синий */
}

.md-typeset .admonition.warning,
.md-typeset details.admonition.warning {
    border-left-color: #f59e0b !important; /* Мягкий янтарный/оранжевый для предупреждений */
}

.md-typeset .admonition.note,
.md-typeset details.admonition.note {
    border-left-color: #06b6d4 !important; /* Приглушенный бирюзовый */
}

/* Наглухо запрещаем синей линии родительского блока прорезать вложенные элементы */
.md-typeset .admonition .admonition {
    margin: 1em 0 !important;
    /* Вложенный блок сам управляет своей левой линией */
}

/* Сбрасываем лишние внутренние фоны у контента */
.md-typeset .admonition-content,
.md-typeset details.admonition .admonition-content {
    background: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Полностью убираем внутреннюю плашку под заголовками примечаний */
.md-typeset .admonition-title,
.md-typeset details.admonition summary {
    background-color: transparent !important; 
    background: transparent !important;
    margin: 0 0 12px 0 !important; /* Легкий отступ снизу до текста */
    border-bottom: none !important;            
    
    /* ФИКСАЦИЯ: Сбрасываем веб-масштабирование темы, чтобы кегль не раздувался */
    font-family: "Fira Sans", "Segoe UI", sans-serif !important;
    font-weight: 700 !important;
    font-size: 1em !important; /* СТАЛО: Жестко 100% от размера текста, без умножения */
    color: #0f172a !important; 
    
    display: block !important; 
    position: relative !important;
    padding: 0 0 0 20px !important; /* Зазор для иконки */
}

/* ГАРАНТИРОВАННО И ФИКСИРОВАННО СТАВИМ ИКОНКУ НА СВОЕ МЕСТО */
.md-typeset .admonition-title::before,
.md-typeset details.admonition summary::before {
    position: absolute !important;
    left: 0 !important;
    top: 50% !important;
    transform: translateY(-50%) !important; /* Строго центрируем иконку по вертикали */
    margin: 0 !important;
    width: 15px !important;  /* Слегка уменьшили под базовый размер текста */
    height: 15px !important;
    display: inline-block !important;
}

/* 5. УМНАЯ ОБРАБОТКА ССЫЛОК */
.md-typeset a[href^="http://"], 
.md-typeset a[href^="https://"] {
    color: #1e40af !important; /* СТАЛО: спокойный глубокий синий (вместо #2563eb) */
    text-decoration: none !important; /* Убираем нижнее подчеркивание, чтобы текст выглядел чище */
    border-bottom: 1px dashed #cbd5e1 !important; /* Добавляем легкий аккуратный пунктир снизу */
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

/* 6. БАЗОВАЯ ТИПОГРАФИКА И ВЕРСТКА */
body, .md-typeset {
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

/* 9. СТИЛИЗАЦИЯ ГЛАВНОГО ЗАГОЛОВКА ДОКУМЕНТА */

/* Сбрасываем относительный масштаб шрифта темы для печатной версии */
html, body {
    font-size: 10.5pt !important;
}

/* Задаем жесткий фиксированный размер для H1 на ВСЕХ страницах */
.md-typeset h1,
h1 {
    font-family: "Fira Sans", "Segoe UI", sans-serif !important;
    text-align: center !important;  
    font-size: 28pt !important; /* Теперь этот размер будет строго одинаковым везде */
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

    # Путь к картинке в скомпилированной папке assets
    svg_local_path = os.path.join(site_dir, "assets", "docio-logo-grey.svg")
    svg_base64_data = ""

    # Пытаемся прочесть файл и закодировать его в Base64 для инъекции
    if os.path.exists(svg_local_path):
        with open(svg_local_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            svg_base64_data = f"data:image/svg+xml;base64,{encoded}"
    else:
        print(f"[PDF Hook] Предупреждение: Локальный логотип {svg_local_path} не найден!")
        svg_base64_data = "https://documentat.io"

    # --- УНИВЕРСАЛЬНЫЙ СКВОЗНОЙ ПОИСК ВСЕХ СТРАНИЦ САЙТА ---
    TARGET_PAGES = []
    
    for root, dirs, files in os.walk(site_dir):
        # Игнорируем технические директории MkDocs со статикой
        if any(ignored in root for ignored in [os.path.join(site_dir, "assets"), os.path.join(site_dir, "css"), os.path.join(site_dir, "js")]):
            continue
            
        for file in files:
            if file.endswith(".html"):
                full_html_path = os.path.join(root, file)
                
                # Относительный путь для сервера
                rel_html_path = os.path.relpath(full_html_path, site_dir)
                rel_html_path = rel_html_path.replace(os.sep, '/') # Нормализация слэшей под Windows
                
                # Исключаем служебные страницы темы
                if file == "404.html" or "search.html" in rel_html_path:
                    continue
                
                # Умное именование PDF
                if file == "index.html":
                    parent_folder_name = os.path.basename(root)
                    if root == site_dir:
                        pdf_filename = "index.pdf"
                    else:
                        pdf_filename = f"{parent_folder_name}.pdf"
                else:
                    pdf_filename = file.replace(".html", ".pdf")
                    
                TARGET_PAGES.append((rel_html_path, pdf_filename))

    print(f"[PDF Hook] Найдено страниц для конвертации: {len(TARGET_PAGES)}")

    # --- АВТОМАТИЧЕСКАЯ ГЕНЕРАЦИЯ ВСЕХ НАЙДЕННЫХ ФАЙЛОВ ---
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
                page.add_style_tag(content=CLEAN_PDF_CSS)
                
                # Печать: жесткое разделение контента и линии через пустой блок-распорку
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
                            <!-- Верхняя строчка с контентом -->
                            <div style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
                                <!-- Левая часть: логотип -->
                                <div style="display: flex; align-items: center;">
                                    <img src="{svg_base64_data}" style="height: 18px; width: auto; display: block;" />
                                </div>
                                
                                <!-- Правая часть: фиксированное название вашего курса -->
                                <div style="font-weight: 500; display: flex; align-items: center;">
                                    Документируй как инженер: практический курс Docs as Code
                                </div>
                            </div>

                            <!-- ИСКУССТВЕННЫЙ ОТСТУП И СЕРАЯ ЛИНИЯ -->
                            <div style="height: 10px; width: 100%; border-bottom: 1px solid #f1f5f9;"></div>
                        </div>
                    """,
                    footer_template="<div></div>"
                )

            browser.close()
        print(f"[PDF Hook] Все PDF успешно созданы! Всего файлов: {len(TARGET_PAGES)}")
    except Exception as e:
        print(f"[PDF Hook] Ошибка при генерации PDF: {e}")
