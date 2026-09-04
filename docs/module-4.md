# Модуль 4. Командная работа: от создания Issue до слияния PR

## Давайте начнем

1. Сделайте полный сброс локальной ветки `main`, чтобы гарантировать отсутствие конфликтов:

    ```
    git checkout main
    ```
    ```
    git fetch origin
    ```
    ```
    git reset --hard origin/main
    ```

1. Проверьте, что вы находитесь в папке `docker-docs-course`. В терминале должно быть:

    ```
    <путь_к_папке>\dac\docker-docs-course>
    ```

## 1. Уточнение задачи (Issue)

1. Зайдите в раздел **Issues** учебного репозитория: https://github.com/zvezdochetu/docker-docs-course/issues

1. Нажмите на фильтр **Assignees** и выберите в списке себя.

1. Откройте свой Issue и если нужно, уточните в комментариях детали задачи, тегнув тимлида (@zvezdochetu).

## 2. Создание изолированной ветки

1. Убедитесь, что вы находитесь на ветке `main`.

1. Подтяните изменения с сервера:

    ```
    git pull origin main
    ```

1. Создайте новую ветку с именем `fix/issue-<номер_issue>-<ваш_аккаунт>-<краткое-описание-через-дефисы>`, например:

    ```
    git switch -c fix/issue-16-zvezdochetu-fix-typo-in-setup
    ```

## 3. Первичные изменения и стартовый коммит

1. Внесите изменения в локальной ветке, достаточные для первого коммита.

1. Отправьте изменения на сервер.

## 4. Создание Draft PR

1. Зайдите в раздел **Pull Requests** учебного репозитория: https://github.com/zvezdochetu/docker-docs-course/pulls

1. Нажмите кнопку **Compare & Pull request**.

1. Заполните поля:

    1. **Title** — кратко опишите суть изменений по-английски.

    1. **Description** — удалите стандартный шаблон описания и добавьте пока только одну строчку: `Closes #<номер_issue>`.

    1. **Assignee** — выберите себя.

    1. **Reviewers** — выберите тимлида.

1. Создайте PR-черновик. Для этого внизу на зеленой кнопке **Create pull request** нажмите на выпадающий список и выберите **Create draft pull request**.

## 5. Запуск сборки превью и проверки Vale

1. Добавьте комментарий `/vale` и проверьте отчет vale.

1. Добавьте комментарий `/preview` и проверьте, что изменения выглядят корректно на превью-сборке.

## 6. Завершение изменений по задаче

Внесите все изменения и отправьте их на сервер.

Если в процессе работы по задаче возникли вопросы, задайте их в комментариях к PR, тегнув тимлида.

## 7. Проверка перевод в статус Ready for review

1. Откройте ваш PR и просмотрите изменения, которые вы внесли, на вкладке **Files Changed**.

1. Если вы меняли что-то с момента создания PR, еще раз запустите сборку (`/preview`) и проверку (`/vale`). Проверьте, что превью-сборка открывается по ссылке и в отчете Vale нет предупреждений.

1. Добавьте к PR описание:
    * Что конкретно сделано.
    * Ссылку, по которой можно посмотреть превью статьи.

1. Внизу окна PR нажмите серую кнопку **Ready for review**.

1. Если тимлид не начнет ревью в течение 5 минут, напишите ему в телеграм-чате.

## 8. Прохождение Code Review

Посмотрите результаты ревью.

## 9. Разрешение конфликтов

Если вы видите внизу окна PR сообщение *This branch has conflicts that must be resolved*, разрешите конфликт:

1. Переключитесь на вашу ветку.

1. Выполните команду:

    ```
    git pull origin main
    ```

1. Разрешите конфликт слияния.

1. Если вы выполнили слияние неверно, но еще не закоммитили изменения, выполните:

    ```
    git merge --abort
    ```

    Далее начните слияние заново.

1. Создайте коммит и отправьте изменения на сервер.

## Открытые проекты для получения первого опыта

### Canonical Open Documentation Academy (reST)

Безусловный фаворит: много понятно оформленных задач для новичков, открытое дружелюбное сообщество. 

Сайт проекта: <https://canonical.com/documentation/open-documentation-academy>

Issues: <https://github.com/canonical/open-documentation-academy/issues>

### MDN Web Docs (Markdown)

Сайт проекта: <https://developer.mozilla.org/>

Правила контрибьюта: <https://github.com/mdn/content/blob/main/CONTRIBUTING.md>

Issues: <https://github.com/mdn/content/issues>

### Cloud Native Glossary (Markdown)

Сайт проекта: <https://glossary.cncf.io/>

Правила контрибьюта: <https://github.com/cncf/glossary/blob/main/CONTRIBUTING.md>

Issues: <https://github.com/cncf/glossary/issues>

### Документация Яндекс Клауд (Markdown)

**Минусы:** задачи придется искать самому.

**Плюсы:** всё на русском, огромное количество сервисов и такое же огромное поле для работы.

Сайт проекта: <https://yandex.cloud/ru/content-program>

Issues: <https://github.com/canonical/open-documentation-academy/issues>

### GitHub (Markdown)

Сайт проекта: <https://github.com/>

Правила контрибьюта: <https://github.com/github/docs/blob/main/.github/CONTRIBUTING.md>

Issues: <https://github.com/github/docs/issues>

### Ethereum website (Markdown)

Сайт проекта: <https://ethereum.org/>

Правила контрибьюта: <https://ethereum.org/contributing/>

Issues: <https://github.com/ethereum/ethereum-org-website/issues>

### Nextcloud (Markdown)

Сайт проекта: <https://nextcloud.com/>

Правила контрибьюта: <https://github.com/nextcloud/documentation/blob/master/CONTRIBUTING.md>

Issues: <https://github.com/nextcloud/documentation/issues>

### Fedora (AsciiDoc)

Если хочется получить опыт работы с AsciiDoc, а также отдельной forge-системой (Fedora Forge) вместо GitHub.

Сайт проекта: <https://fedoraproject.org/>

Правила контрибьюта: <https://docs.fedoraproject.org/en-US/fedora-docs/contributing-docs/>

Issues: <https://forge.fedoraproject.org/docs/tickets/issues>
