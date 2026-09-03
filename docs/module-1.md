# Модуль 1. Быстрый старт: Markdown и статическая генерация сайта

## Давайте начнем

Перед началом практической части проделайте следующие шаги:

1. Запустите VS Code и откройте в нем папку [my-site](prerequisites.md#vite) (меню **File -> Open Folder**).

1. Если в VS Code закрыт встроенный терминал, откройте его (правой кнопкой мыши на папке `my-site`, **Open in Integrated Terminal**).

    ??? info "Как понять, что всё ок"

        В проводнике VS Code вы видите:

        ```
        my-site\
        .vitepress
        node-modules
        ...
        ```

        В терминале внизу:

        ```
        <путь_к_папке>\my-site>
        ```

        При запуске в терминале команды `npm run docs:dev`:

        ```
        > my-site@1.0.0 docs:dev
        > vitepress dev


        vitepress v1.6.4

        ➜  Local:   http://localhost:5173/
        ➜  Network: use --host to expose
        ➜  press h to show help
        ```

        Нажмите **Ctrl+C**, чтобы завершить запущенный процесс.

## Практика 1: работа с md-файлами в редакторе VS Code

1. Создайте в папке `my-site` файлы `cv.md` и `about.md`.

1. Скопируйте в них собственные описания или [тексты-заглушки](prerequisites.md#portfolio).

1. Добавьте в файлы разметку Markdown. Должно получиться примерно так:

    ``` title="cv.md"
    # Алиса Котикова — резюме

    Стек и технологии: `Docs-as-Code` `OpenAPI 3.0` `Git` `CI/CD` `VitePress` `Markdownlint`

    ## Опыт работы

    ### Lead Technical Writer | Fintech Corp (2021–н.в.)

    * Построила централизованный портал документации:
        1. Перевела 120+ инженеров с Confluence на Markdown.
        2. Внедрила автоматический линтинг текстов в Git.
    * Сократила время онбординга разработчиков на **40%**.

    ### Senior Technical Writer | Cloud Systems (2016–2021)

    * Поддержка API Reference для 40+ микросервисов.
    * Разработка единого корпоративного Style Guide.
    ```

    ``` title="about.md"
    # Обо мне

    Я 10 лет проектирую и внедряю **Docs-as-Code** для enterprise-инфраструктуры, API-порталов и инженерных команд.

    **Моя философия**

    > Архитектура документации должна быть такой же чистой, как и архитектура кода.

    ## Контакты

    Связаться со мной можно по почте <writer@example.com> или в соцсетях:

    * Профиль с проектами: [GitHub](https://github.com/example)
    * Профессиональный трек: [LinkedIn](https://linkedin.com/in/example)
    * Оперативная связь: [Telegram](https://t.me/example)
    ```

## Практика 2: локальная сборка проекта VitePress

1. Запустите локальную сборку сайта:

    ```
    npm run docs:build
    ```

1. Проверьте, что в папке `.vitepress` появилась подпапка `dist` с файлами статического сайта.

1. Запустите сервер предпросмотра:

    ```
    npx vitepress preview
    ```

1. Перейдите по ссылке в терминале (обычно это <http://localhost:4173/>).

1. Остановите сервер (**Ctrl + C**).

1. Запустите сервер разработки:

    ```
    npm run docs:dev
    ```

1. Перейдите по ссылке в терминале (обычно это <http://localhost:5173/>).

1. Остановите сервер (**Ctrl + C**).

## Практика 3: верстка и конфигурирование сайта в VitePress

1. Измените конфигурационный файл проекта:

    ``` title="config.mjs"
    import { defineConfig } from 'vitepress'

    // https://vitepress.dev/reference/site-config
    export default defineConfig({
      title: "А. К.",
      description: "Личный сайт и портфолио Алисы Котиковой",
      themeConfig: {
        // https://vitepress.dev/reference/default-theme-config
        nav: [
          { text: 'Обо мне', link: '/about' },
          { text: 'Резюме', link: '/cv' }
        ],

        socialLinks: [
          { icon: 'github', link: 'https://github.com/vuejs/vitepress' }
        ]
      }
    })
    ```

1. Измените заглавную страницу:

    ``` title="index.md"
    ---
    # https://vitepress.dev/reference/default-theme-home-page
    layout: home

    hero:
    name: "Алиса Котикова"
    tagline: Staff Technical Writer с 10-летним треком в архивировании и автоматизации документации для enterprise-систем
    actions:
        - theme: brand
        text: Профиль на GitHub
        link: https://github.com/example
        - theme: alt
        text: 📄 Резюме в формате PDF
        link: ./cv.pdf
        target: _blank
    ---
    ```

1. Удалите файлы `api-examples.md` и `markdown-examples.md` из проекта.

1. Создайте в папке `my-site` подпапку `public` и скопируйте в нее [файлы-заглушки](prerequisites.md#portfolio) `cv.md` и `ava.png`.

1. Измените страницу «Резюме»:

    ``` title="cv.md"
    # Алиса Котикова — резюме

    ::: info 📄 Печатная версия
    **[Скачать резюме в формате PDF](./cv.pdf){target="_blank"}**
    :::

    ## Стек и технологии
    <Badge type="info" text="Docs-as-Code" /> <Badge type="info" text="OpenAPI 3.0" /> <br>
    <Badge type="tip" text="Git / CI/CD" /> <Badge type="tip" text="VitePress" />  <br>
    <Badge type="warning" text="Markdownlint" />

    ## Опыт работы

    ### Lead Technical Writer | Fintech Corp (2021–н.в.)

    * Построила централизованный портал документации:
        1. Перевела 120+ инженеров с Confluence на Markdown.
        2. Внедрила автоматический линтинг текстов в Git.
    * Сократила время онбординга разработчиков на **40%**.

    ### Senior Technical Writer | Cloud Systems (2016–2021)

    * Поддержка API Reference для 40+ микросервисов.
    * Разработка единого корпоративного Style Guide.
    ```

1. Измените страницу «Обо мне»:

    ``` title="about.md"
    # Обо мне

    <div class="profile-section">
    <img src="/ava.png" alt="Иван Петров" class="profile-avatar" />

    Я 10 лет проектирую и внедряю **Docs-as-Code** для enterprise-инфраструктуры, API-порталов и инженерных команд. 
    </div>

    ::: tip Моя философия
    Архитектура документации должна быть такой же чистой, как и архитектура кода.
    :::

    ## Контакты

    Связаться со мной можно по почте <writer@example.com> или в соцсетях:

    * Профиль с проектами: [GitHub](https://github.com/example "Профиль GitHub")
    * Профессиональный трек: [LinkedIn](https://linkedin.com/in/example "Профиль LinkedIn")
    * Оперативная связь: [Telegram](https://t.me/example "Написать в Telegram")

    <style scoped>
    .profile-section {
    display: flow-root;
    margin-bottom: 24px;
    }

    .profile-avatar {
    width: 140px;
    height: 140px;
    border-radius: 16px;
    float: right;
    margin: 12px 0 16px 24px; /* 12px сверху отделяют фото от заголовка */
    object-fit: cover;
    box-shadow: var(--vp-shadow-2);
    }

    /* На мобильных сохраняем float, но пропорционально уменьшаем фото */
    @media (max-width: 640px) {
    .profile-avatar {
        width: 96px;
        height: 96px;
        margin: 6px 0 12px 14px; /* Компактные отступы для узких экранов */
    }
    }
    </style>
    ```

1. Запустите сервер разработки:

    ```
    npm run docs:dev
    ```

1. Перейдите по ссылке в терминале (обычно это <http://localhost:5173/>).

1. Остановите сервер (**Ctrl + C**).

## Полезные ссылки

### Синтаксис Markdown

**CommonMark**

Шпаргалка по синтаксису: <https://commonmark.org/help/>

Полная спецификация: <https://spec.commonmark.org/current/>

**GitHub Flavored Markdown (GFM)**

<https://github.github.com/gfm/>

<https://github.com/lifeparticle/Markdown-Cheatsheet>

**Синтаксис расширений VitePress**

<https://vitepress.dev/guide/markdown>

### Сравнение Markdown, reST и AsciiDoc

<https://www.freescribe.cz/2026/06/28/markdown-restructuredtext-asciidoc-comparison/>

### Примеры сайтов документации на Markdown (разные SSG)

**VitePress**

* <https://vuejs.org/>
* <https://grammy.dev/>

**MkDocs**

* <https://docs.vllm.ai/>
* <https://fastapi.tiangolo.com/>
* этот сайт )

**Hugo**

* <https://docs.docker.com/>
* <https://kubernetes.io/docs/home/>

**Docusaurus**

* <https://docsearch.algolia.com/>
* <https://docs.dyte.io/>

**Diplodoc**

* <https://yandex.cloud/ru/docs/compute/>
* <https://double.cloud/docs/en/>

### Примеры сайтов документации на Asciidocs (Antora и другие SSG)

* <https://git-scm.com/docs/user-manual>
* <https://docs.fedoraproject.org/en-US/docs/>

### Примеры сайтов документации на reST (SSG Sphinx)

* <https://www.python.org/>
* <https://ubuntu.com/pro/docs/>
* <https://docs.openstack.org/>

### Кастомизация стилей сайта-визитки

1. Создайте в папке `.vitepress` подпапку `theme`, содержащую файлы.

1. Создайте в папке `theme` файл index.js:

    ``` title="index.js"
    import DefaultTheme from 'vitepress/theme'
    import './custom.css'

    export default {
      extends: DefaultTheme
    }
    ```

1. Создайте в папке `theme` файл стилей `custom.css`:

    * Пример файла для стиля «под терминал»:
    
        ??? info "Файл большой, поэтому под катом"

            ``` title="custom.css"
            /* .vitepress/theme/custom.css — Matrix / Terminal Edition */

            /* Базовые моноширинные шрифты */
            :root {
              --vp-font-family-base: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace;
              --vp-font-family-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;

              /* Светлая тема (Retro CRT Paper / Светлый консольный режим) */
              --vp-c-bg: #eaf4ea;
              --vp-c-bg-alt: #dceedc;
              --vp-c-bg-elv: #f4faf4;
              --vp-c-text-1: #052b09;
              --vp-c-text-2: #16521e;
              --vp-c-brand-1: #008f28;
              --vp-c-brand-2: #00b333;

              --custom-border-color: rgba(0, 143, 40, 0.35);
              --custom-shadow: 0 2px 8px rgba(0, 143, 40, 0.1);
              --custom-glow: none;
            }

            /* Тёмная тема (Classic Matrix / OLED Terminal) */
            .dark {
              --vp-c-bg: #030703;
              --vp-c-bg-alt: #081008;
              --vp-c-bg-elv: #0f1c0f;
              --vp-c-text-1: #00ff66; /* Люминофорный зелёный */
              --vp-c-text-2: #00b347;
              --vp-c-brand-1: #00ff66;
              --vp-c-brand-2: #33ff85;

              --custom-border-color: rgba(0, 255, 102, 0.35);
              --custom-shadow: 0 0 15px rgba(0, 255, 102, 0.12);
              --custom-glow: 0 0 8px rgba(0, 255, 102, 0.45); /* Неоновое свечение */
            }

            /* Консольные заголовки с эффектом свечения люминофора */
            h1, h2, h3, .vp-doc h1, .vp-doc h2, .VPHero .name {
              font-family: var(--vp-font-family-base) !important;
              font-weight: 700 !important;
              letter-spacing: -0.01em;
              text-shadow: var(--custom-glow);
            }

            /* Строгие углы (4px вместо 12px) и рамочные карточки */
            .VPFeature, .VPButton, .VPDoc .custom-block {
              border-radius: 4px !important;
              border: 1px solid var(--custom-border-color) !important;
              box-shadow: var(--custom-shadow);
            }

            .VPButton {
              font-family: var(--vp-font-family-base);
              text-transform: uppercase;
              letter-spacing: 0.05em;
            }

            /* Консольное выделение текста */
            ::selection {
              background: var(--vp-c-brand-1);
              color: var(--vp-c-bg);
            }

            /* Переопределение фирменных цветов кнопок VitePress */
            :root {
              --vp-button-brand-bg: var(--vp-c-brand-1);
              --vp-button-brand-border: var(--vp-c-brand-1);
              --vp-button-brand-text: #000000;
              --vp-button-brand-hover-bg: var(--vp-c-brand-2);
              --vp-button-brand-hover-border: var(--vp-c-brand-2);
              --vp-button-brand-hover-text: #000000;
              --vp-button-brand-active-bg: var(--vp-c-brand-1);
              --vp-button-brand-active-text: #000000;
            }

            /* Полная подгонка акцентной кнопки (GitHub) под консольный стиль */
            .VPButton.brand {
              background-color: var(--vp-c-brand-1) !important;
              border-color: var(--vp-c-brand-1) !important;
              color: #000000 !important; /* Черный текст на инвертированном люминофорном фоне */
              font-weight: 700 !important;
              box-shadow: 0 0 12px rgba(0, 255, 102, 0.4);
            }

            .VPButton.brand:hover {
              background-color: var(--vp-c-brand-2) !important;
              border-color: var(--vp-c-brand-2) !important;
              color: #000000 !important;
              box-shadow: 0 0 20px rgba(0, 255, 102, 0.75);
            }

            /* Вторичная кнопка (PDF) */
            .VPButton.alt {
              background-color: var(--vp-c-bg-elv) !important;
              border: 1px solid var(--custom-border-color) !important;
              color: var(--vp-c-text-1) !important;
              transition: border-color 0.25s, color 0.25s, box-shadow 0.25s !important;
            }

            .VPButton.alt:hover {
              border-color: var(--vp-c-brand-1) !important;
              color: var(--vp-c-brand-1) !important;
              /* Зелёное неоновое свечение границы и текста при наведении */
              box-shadow: 0 0 18px rgba(0, 255, 102, 0.6) !important;
            }

            /* Эффект свечения для карточек Features (VPFeature) */
            .VPFeature {
              transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s !important;
            }

            .VPFeature:hover {
              border-color: var(--vp-c-brand-1) !important;
              /* Мягкое неоновое свечение вокруг всей карточки */
              box-shadow: 0 0 20px rgba(0, 255, 102, 0.25) !important;
            }

            /* Опционально: подсветка иконки и заголовка внутри карточки при наведении */
            .VPFeature:hover .icon {
              filter: drop-shadow(0 0 6px var(--vp-c-brand-1));
            }

            .VPFeature:hover .title {
              color: var(--vp-c-brand-1) !important;
            }

            /* Ссылки в тексте документа */
            .vp-doc a {
              color: var(--vp-c-brand-1) !important;
              text-decoration-color: var(--custom-border-color);
              text-underline-offset: 4px;
              transition: color 0.25s, text-shadow 0.25s, text-decoration-color 0.25s !important;
            }

            .vp-doc a:hover {
              color: var(--vp-c-brand-2) !important;
              text-decoration-color: var(--vp-c-brand-1) !important;
              /* Мягкое неоновое свечение текста ссылки */
              text-shadow: 0 0 8px rgba(0, 255, 102, 0.6) !important;
            }

            /* Элементы верхнего меню (логотип, ссылки и выпадающие списки) */
            .VPNavBarTitle:hover,
            .VPNavBarMenuLink:hover,
            .VPNavBar .VPFlyout button:hover {
              color: var(--vp-c-brand-1) !important;
              text-shadow: 0 0 8px rgba(0, 255, 102, 0.6) !important;
              transition: color 0.25s, text-shadow 0.25s !important;
            }

            /* Активный пункт меню (текущая страница) */
            .VPNavBarMenuLink.active {
              color: var(--vp-c-brand-1) !important;
              text-shadow: 0 0 5px rgba(0, 255, 102, 0.4);
            }
            ```

    * Пример файла для «плакатного» стиля:
    
        ??? info "Файл большой, поэтому под катом"

            ``` title="custom.css"
            /* .vitepress/theme/custom.css — Швейцарская плакатная редакция */

            /* Светлая тема (Light Mode — Теплая бумага / Терракота) */
            :root {
              --vp-c-bg: #fbf9f5;
              --vp-c-bg-alt: #f3efe6;
              --vp-c-bg-elv: #ffffff;
              --vp-c-text-1: #2b2826;
              --vp-c-text-2: #59534f;
              
              --vp-c-brand-1: #c85a32; /* Тёплый терракотовый */
              --vp-c-brand-2: #a74320;
              --vp-c-brand-3: #873215;

              /* Переменные брендовых кнопок VitePress (перебивают синий цвет по умолчанию) */
              --vp-button-brand-bg: #c85a32;
              --vp-button-brand-border: #c85a32;
              --vp-button-brand-text: #ffffff;
              --vp-button-brand-hover-bg: #a74320;
              --vp-button-brand-hover-border: #a74320;
              --vp-button-brand-hover-text: #ffffff;
              --vp-button-brand-active-bg: #873215;

              --vp-font-family-base: 'Georgia', 'Times New Roman', serif;

              /* Мягкие плакатные тени и рамки */
              --custom-border-color: rgba(200, 90, 50, 0.2);
              --custom-shadow: 0 4px 16px rgba(43, 40, 38, 0.05);
              --custom-shadow-hover: 0 8px 24px rgba(200, 90, 50, 0.15);
            }

            /* Тёмная тема (Dark Mode — Тёплый графит / Эспрессо) */
            .dark {
              --vp-c-bg: #1c1a19;
              --vp-c-bg-alt: #24211f;
              --vp-c-bg-elv: #2c2826;
              --vp-c-text-1: #eee8e1;
              --vp-c-text-2: #b5aba0;

              --vp-c-brand-1: #e07148; /* Высветленный кораллово-терракотовый */
              --vp-c-brand-2: #f28b65;
              --vp-c-brand-3: #ff9e79;

              /* Переменные брендовых кнопок для темной темы */
              --vp-button-brand-bg: #e07148;
              --vp-button-brand-border: #e07148;
              --vp-button-brand-text: #1c1a19; /* Контрастный темный текст на терракотовой кнопке */
              --vp-button-brand-hover-bg: #f28b65;
              --vp-button-brand-hover-border: #f28b65;
              --vp-button-brand-hover-text: #1c1a19;

              --custom-border-color: rgba(224, 113, 72, 0.22);
              --custom-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
              --custom-shadow-hover: 0 8px 28px rgba(224, 113, 72, 0.22);
            }

            /* --- Аккуратная плакатная типографика --- */
            h1, h2, h3, .vp-doc h1, .vp-doc h2, .VPHero .name {
              font-family: 'Georgia', 'Playfair Display', serif !important;
              font-weight: 400 !important;
              letter-spacing: -0.02em;
            }

            .VPHero .name {
              color: var(--vp-c-brand-1) !important;
            }

            /* --- Главная кнопка (GitHub / Primary) --- */
            .VPButton.brand {
              background-color: var(--vp-button-brand-bg) !important;
              border-color: var(--vp-button-brand-border) !important;
              color: var(--vp-button-brand-text) !important;
              font-weight: 600 !important;
              border-radius: 12px !important;
              box-shadow: var(--custom-shadow);
              transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
            }

            .VPButton.brand:hover {
              background-color: var(--vp-button-brand-hover-bg) !important;
              border-color: var(--vp-button-brand-hover-border) !important;
              color: var(--vp-button-brand-hover-text) !important;
              transform: translateY(-2px);
              box-shadow: var(--custom-shadow-hover);
            }

            /* --- Вторичная кнопка (PDF / Alt) --- */
            .VPButton.alt {
              background-color: var(--vp-c-bg-alt) !important;
              border: 1px solid var(--custom-border-color) !important;
              color: var(--vp-c-text-1) !important;
              border-radius: 12px !important;
              font-weight: 500 !important;
              transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
            }

            .VPButton.alt:hover {
              background-color: var(--vp-c-bg-elv) !important;
              border-color: var(--vp-c-brand-1) !important;
              color: var(--vp-c-brand-1) !important;
              transform: translateY(-2px);
              box-shadow: var(--custom-shadow-hover);
            }

            /* --- Плакатные карточки Features --- */
            .VPFeature, .VPDoc .custom-block {
              border-radius: 16px !important;
              border: 1px solid var(--custom-border-color) !important;
              background-color: var(--vp-c-bg-alt) !important; /* Цвет как у кнопки "Резюме" */
              box-shadow: var(--custom-shadow);
              transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
            }

            .VPFeature:hover {
              transform: translateY(-3px);
              border-color: var(--vp-c-brand-1) !important;
              box-shadow: var(--custom-shadow-hover);
            }

            /* --- Ссылки в статьях --- */
            .vp-doc a {
              color: var(--vp-c-brand-1);
              text-decoration: underline;
              text-decoration-color: var(--custom-border-color);
              text-underline-offset: 4px;
              transition: all 0.2s ease;
            }

            .vp-doc a:hover {
              color: var(--vp-c-brand-2);
              text-decoration-color: var(--vp-c-brand-1);
            }
            ```
