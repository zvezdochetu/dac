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
