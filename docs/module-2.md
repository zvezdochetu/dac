# Модуль 2. От локального проекта к CI/CD и публикации

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

## Практика 1: настройка Git

1. Задайте имя/ник и email, которые будут указываться в истории изменений репозитория:

    ```
    git config --global user.name "<имя_фамилия_или_ник>"
    ```
    ```
    git config --global user.email "<ваш_email>"
    ```

    !!! warning "Внимание"

        Email должен совпадать с одним из адресов, указанных в вашем аккаунте на GitHub в разделе **Settings → Emails**.

1. Задайте имя главной ветки по умолчанию как `main`:

    ```
    git config --global init.defaultBranch main
    ```

1. Настройте окончания строк (защита от мусорных диффов между ОС):

    ```
    git config --global core.autocrlf input
    ```

## Практика 2: загрузка файлов в репозиторий

1. Создайте в папке `my-site` файл `.gitignore`:

    ``` title=".gitignore"
    node_modules/
    .vitepress/dist/
    .vitepress/cache/
    .DS_Store
    Thumbs.db
    *.log
    .env
    .env.*.local
    ```

1. Инициализируйте локальный репозиторий:

    ```
    git init
    ```

1. Создайте первый коммит:

    ```
    git add .
    ```
    ```
    git commit -m "feat: initial commit"
    ```

1. Создайте репозиторий `my-site` на GitHub: <https://github.com/new> (Repository name: `my-site`, остальные параметры по умолчанию).

1. Привяжите к нему ваш локальный репозиторий:

    ```
    git remote add origin git@github.com:<ваш_github_аккаунт>/my-site.git
    ```

1. Отправьте первый коммит на сервер:

    ```
    git push -u origin main
    ```

## Практика 3: настройка деплоя в GitHub Pages

1. В настройках созданного репозитория **Settings → Pages** в блоке **Source** укажите **GitHub Actions**.

1. Добавьте строчку `base: '/my-site/',` в конфигурационный файл VitePress, например:

    ``` title="config.mjs"
    import { defineConfig } from 'vitepress'

    // https://vitepress.dev/reference/site-config
    export default defineConfig({
      base: '/my-site/',
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

1. Создайте в папке `my-site` файл `.github\workflows\deploy.yml`:

    ``` title="deploy.yml"
    name: Deploy VitePress site to Pages

    on:
      push:
        branches: [main]
      workflow_dispatch:

    permissions:
      contents: read
      pages: write
      id-token: write

    concurrency:
      group: pages
      cancel-in-progress: false

    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout
            uses: actions/checkout@v4
            with:
              fetch-depth: 0

          - name: Setup Node.js
            uses: actions/setup-node@v4
            with:
              node-version: 20
              cache: npm

          - name: Setup Pages
            uses: actions/configure-pages@v5

          - name: Install dependencies
            run: npm ci

          - name: Build VitePress
            run: npm run docs:build

          - name: Upload artifact
            uses: actions/upload-pages-artifact@v3
            with:
              path: .vitepress/dist

      deploy:
        environment:
          name: github-pages
          url: ${{ steps.deployment.outputs.page_url }}
        needs: build
        runs-on: ubuntu-latest
        name: Deploy
        steps:
          - name: Deploy to GitHub Pages
            id: deployment
            uses: actions/deploy-pages@v4
    ```

1. Создайте коммит:

    ```
    git add .
    ```
    ```
    git commit -m "ci: setup github pages deployment"
    ```

1. Отправьте коммит на сервер:

    ```
    git push
    ```

1. Откройте собранный сайт по адресу: `https://<ваш_github_аккаунт>.github.io/my-site/`.
