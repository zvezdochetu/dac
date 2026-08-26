# Шпаргалки по командам и синтаксису

## Интерфейс vscode { #vscode }

[VS Code in 100 Seconds](https://www.youtube.com/watch?v=KMxo3T_MTvY) — хороший короткий ролик (к сожалению, доступен только на ютубе).

[Tutorial: Get started with Visual Studio Code](https://code.visualstudio.com/docs/editing/getting-started) — руководство формата «Быстрый старт» на официальном сайте VS Code.

[Visual Studio Code: установка, настройка, русификация и список горячих клавиш](https://skillbox.ru/media/code/visual-studio-code-ustanovka-nastroyka-rusifikatsiya-i-spisok-goryachikh-klavish/) — простое руководство Skillbox Media.

## Шпаргалка по Markdown { #md }

На курсе мы будем использовать базовый синтаксис CommonMark:

| Исходный синтаксис (Markdown) | Результат (Рендеринг) |
| :--- | :--- |
| `*Italic*` | *Italic* |
| `**Bold**` | **Bold** |
| `# Heading 1` | <h1>Heading 1</h1> |
| `## Heading 2` | <h2>Heading 2</h2> |
| `[Link](http://a.com)` | [Link](http://a.com) |
| `![Image](https://commonmark.org/help/images/favicon.png)` | ![Image](https://commonmark.org/help/images/favicon.png) |
| `> Blockquote` | <blockquote>Blockquote</blockquote> |
| `* List`<br>`* List`<br>`* List` | <ul><li>List</li><li>List</li><li>List</li></ul> |
| `1. One`<br>`2. Two`<br>`3. Three` | <ol><li>One</li><li>Two</li><li>Three</li></ol> |
| `Horizontal rule:`<br>`---` | Horizontal rule:<hr> |
| `` `Inline code` with backticks `` | `Inline code` with backticks |
| ` ``` `<br>`# code block`<br>`print '3 backticks or'`<br>`print 'indent 4 spaces'`<br>` ``` ` | <pre><code># code block<br>print '3 backticks or'<br>print 'indent 4 spaces'</code></pre> |

## Шпаргалка по работе с терминалом { #terminal }

| Действие | Windows | Linux | macOS |
| :--- | :--- | :--- | :--- |
| **Копировать из терминала** | **Ctrl + Shift + C** | **Ctrl + Shift + V** | **Cmd + C** |
| **Вставить в терминал** | **Ctrl + Shift + V** *(или правый клик)* | **Ctrl + Shift + V** *(или клик колесиком)* | **Cmd + V** |

**стрелка вверх / стрелка вниз** — листать историю ранее введенных команд.

**Ctrl + C** — прервать процесс, например остановить сервер `npm run docs:dev` или прервать долго выполняющуюся команду.

**Ctrl + R** — поиск по истории ранее выполненных команд.

`cd <имя_папки>` — перейти в папку.

`cd ..` — перейти на уровень выше.

`mkdir <имя_папки>` — создать директорию.

`rmdir <имя_папки>` — удалить пустую директорию.

<!--
4. Мини-интерактив: Попробуйте сами
Перейдите на Рабочий стол: cd Desktop (или cd Desktop из домашней папки).

Создайте папку my-first-site: mkdir my-first-site.

Зайдите в неё: cd my-first-site.

Проверьте путь: pwd.

Выйдите на уровень вверх: cd ...

mkdir — создание новой папки (например, mkdir test-folder).

rmdir — удаление пустой директории.

Нажмите стрелку вверх несколько раз, чтобы найти команду cd my-first-site и запустить её снова без повторного ввода.

Если вы смогли без ошибок пройти этот тест — вы полностью готовы к работе с курсом!

-->