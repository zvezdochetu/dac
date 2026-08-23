# Подготовка и настройка

## Подготовка окружения { #env }

Тест вкладок:

=== "Windows (PowerShell)"

    ```powershell
    cd docker-docs-course
    ```

=== "Linux / macOS (Bash)"

    ```bash
    cd docker-docs-course
    ```

## Подготовка файлов для сайта-визитки

## Создание проекта VitePress

## Клонирование репозитория docker-docs-course { #clone }

Перед клонированием [подготовьте окружение](#env).

Чтобы склонировать репозиторий docker-docs-course:

1. В удобном месте на диске создайте папку `dac`, например `C:\dac`.
1. Откройте новое окно vscode.
1. Откройте папку `dac` в vscode (меню **File -> Open Folder**).
1. Если внизу окна нет терминала, откройте его (меню **Terminal -> New Terminal**).
1. Проверьте, что терминал указывает на папку `dac`, например `C:\dac>`.
1. Клонируйте репозиторий:

    ```
    git clone git@github.com:zvezdochetu/docker-docs-course.git
    ```

1. Перейдите в созданную папку `docker-docs-course`:

    ```
    cd docker-docs-course
    ```

1. Проверьте, что клонирование завершилось успешно:

    ```
    git status
    ```
    Вы должны увидеть сообщение:
    ```
    On branch main
    Your branch is up to date with 'origin/main'.

    nothing to commit, working tree clean
    ```