# Модуль 1. Быстрый старт: Markdown и локальная сборка сайта


Канонические ссылки по CommonMark

https://commonmark.org/help/

https://spec.commonmark.org/current/


Подробнейший справочник по GFM:

https://github.github.com/gfm/

https://github.com/lifeparticle/Markdown-Cheatsheet

GFM поддерживают большинство популярных SSG:

Hugo — по умолчанию использует парсер Goldmark, в котором расширения GFM (таблицы, зачеркивание, чекбоксы, автоссылки) включены из коробки.

Astro / Gatsby / Next.js — работают на экосистеме Unified/Remark. Поддержка GFM подключается базовым плагином remark-gfm.

VitePress / VuePress — используют парсер markdown-it, где расширения GFM (таблицы, зачеркивание) включены по умолчанию.

Jekyll — стандартный SSG для GitHub Pages. Использует парсер Kramdown с режимом kramdown-parser-gfm (или парсер gfm).

MkDocs — с движком Python-Markdown включает таблицы и зачеркивание через стандартное расширение tables и pymdownx.extra.


Помимо этого почти каждый SSG использует свои шорткоды и расширения:

Hugo: Использует синтаксис {{< shortcode >}} или {{% shortcode %}}.

Пример: {{< highlight python >}}, {{< youtube w7Ft2ymGmfc >}}, {{< figure src="image.jpg" caption="Описание" >}}.

Расширения VitePress

https://vitepress.dev/guide/markdown

https://vitepress.dev/guide/markdown#custom-containers