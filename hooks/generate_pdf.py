import os
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
    margin-top: 1.5em !important;
    margin-bottom: 0.6em !important;
    font-size: 13pt !important;
}

.md-typeset .toc {
    background-color: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 6px !important;
    padding: 18px 24px !important;
    margin: 0.8em 0 2em 0 !important;
}

/* Скрываем заголовок H1 из оглавления */
.md-typeset .toc > ul > li > a {
    display: none !important;
}

/* Обнуляем левый сдвиг у списков */
.md-typeset .toc ul,
.md-typeset .toc li {
    padding-left: 0 !important;
    margin-left: 0 !important;
    list-style-type: none !important;
    list-style-image: none !important;
}

.md-typeset .toc li {
    margin-bottom: 8px !important;
}

.md-typeset .toc li:last-child {
    margin-bottom: 0 !important;
}

.md-typeset .toc a {
    color: #334155 !important;
    font-size: 10.5pt !important;
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

/* 6. БАЗОВАЯ ТИПОГРАФИКА И ВЕРСТКА */
body, .md-typeset {
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif !important;
    font-size: 10.5pt !important;
    line-height: 1.6 !important;
    color: #1e293b !important;
}

.md-main__inner, .md-content {
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    max-width: none !important;
}

/* 7. ИНЛАЙН-КОД */
.md-typeset :not(pre) > code {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 4px !important;
    padding: 2px 6px !important;
    font-family: Consolas, "Courier New", monospace !important;
    font-size: 0.88em !important;
}

/* 8. БЛОКИ КОДА */
.md-typeset .highlight pre,
.md-typeset .highlight code,
.md-typeset .highlight span,
.md-typeset pre > code {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

.md-typeset .highlight,
.md-typeset pre:not(.highlight pre) {
    background-color: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 6px !important;
    padding: 10px 14px !important;
    margin: 0.8em 0 !important;
    display: block !important;
}

.md-typeset .highlight code,
.md-typeset pre code {
    font-family: Consolas, "Courier New", monospace !important;
    font-size: 0.9em !important;
    line-height: 1.5 !important;
    color: #0f172a !important;
    white-space: pre-wrap !important;
    word-break: break-all !important;
}
"""

def on_post_build(config):
    site_dir = config['site_dir']
    
    html_path = os.path.join(site_dir, 'takeaway', 'index.html')
    if not os.path.exists(html_path):
        html_path = os.path.join(site_dir, 'takeaway.html')

    if not os.path.exists(html_path):
        print(f"[PDF Hook] Файл {html_path} не найден. Пропуск генерации PDF.")
        return

    pdf_path = os.path.join(os.path.dirname(html_path), 'takeaway.pdf')

    print(f"[PDF Hook] Генерация PDF: {html_path} -> {pdf_path}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{os.path.abspath(html_path)}")
        page.add_style_tag(content=CLEAN_PDF_CSS)
        page.pdf(
            path=pdf_path,
            format="A4",
            margin={
                "top": "20mm",
                "bottom": "20mm",
                "left": "20mm",
                "right": "20mm"
            },
            print_background=True
        )
        browser.close()

    print("[PDF Hook] PDF успешно создан!")