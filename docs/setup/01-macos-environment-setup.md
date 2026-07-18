# QA Commerce Automation Lab

## Документ 01 — Підготовка середовища на macOS

**Версія документа:** 1.0  
**Дата створення:** 17.07.2026  
**Операційна система:** macOS  
**Архітектура процесора:** Apple Silicon, `arm64`

---

# 1. Мета документа

Цей документ фіксує всі дії, які були виконані для підготовки MacBook до роботи над проєктом **QA Commerce Automation Lab**.

Документ потрібен для того, щоб:

- розуміти, що саме було встановлено;
- пам’ятати призначення кожного інструмента;
- швидко відновити середовище на іншому комп’ютері;
- не загубити важливі команди;
- підготуватися до співбесіди;
- мати професійну технічну документацію у GitHub.

---

# 2. Загальна ціль проєкту

Ми створюємо повноцінний QA Automation портфоліо-проєкт для e-commerce системи.

У майбутньому в проєкті будуть:

- frontend магазину;
- backend;
- Admin Panel;
- REST API;
- PostgreSQL;
- Docker;
- Playwright;
- TypeScript;
- GitHub Actions;
- Allure Report;
- API-тести;
- UI-тести;
- інтеграційні тести;
- database checks;
- test strategy;
- test cases;
- bug reports.

---

# 3. Робоча директорія

## Що це

Робоча директорія — це основна папка, у якій зберігатимуться всі файли нашого QA Automation проєкту.

## Для чого вона потрібна

Вона допомагає:

- тримати всі пов’язані файли в одному місці;
- не змішувати навчальний проєкт з іншими файлами;
- зручно відкривати проєкт у VS Code;
- працювати з Git;
- у майбутньому завантажити код у GitHub.

## Команди

```bash
mkdir -p ~/Projects/QA-AUTO-ROAD-MAP
cd ~/Projects/QA-AUTO-ROAD-MAP
```

## Що робить кожна команда

### `mkdir -p ~/Projects/QA-AUTO-ROAD-MAP`

Створює папку:

```text
~/Projects/QA-AUTO-ROAD-MAP
```

Параметр `-p` означає:

- створити також проміжні папки, якщо їх немає;
- не показувати помилку, якщо папка вже існує.

### `cd ~/Projects/QA-AUTO-ROAD-MAP`

Переходить у створену папку.

### `pwd`

Показує поточну директорію.

Очікуваний результат:

```text
/Users/volodymyryankers/Projects/QA-AUTO-ROAD-MAP
```

---

# 4. VS Code

## Що це

**Visual Studio Code** — редактор коду, у якому ми будемо працювати з:

- TypeScript;
- Playwright;
- конфігураційними файлами;
- Docker;
- Git;
- документацією;
- тестами;
- API-клієнтами.

## За що відповідає

VS Code буде нашим основним робочим середовищем.

У ньому ми будемо:

- створювати файли;
- запускати команди;
- переглядати Git-зміни;
- писати тести;
- запускати Playwright;
- працювати з терміналом;
- редагувати Markdown-документацію.

## Як відкрити Terminal у VS Code

```text
Terminal → New Terminal
```

Або комбінація клавіш:

```text
Control + `
```

---

# 5. Перевірка macOS

## Команда

```bash
sw_vers
```

## Що вона робить

Показує інформацію про операційну систему:

- назву macOS;
- версію;
- build number.

## Результат

```text
ProductName: macOS
ProductVersion: 26.5.1
BuildVersion: 25F80
```

---

# 6. Перевірка архітектури процесора

## Команда

```bash
uname -m
```

## Що вона робить

Показує архітектуру процесора.

## Результат

```text
arm64
```

## Що це означає

`arm64` означає, що MacBook працює на Apple Silicon.

Це важливо, тому що:

- Homebrew використовує шлях `/opt/homebrew`;
- Docker завантажує ARM-compatible images;
- деякі пакети мають окремі версії для Intel та Apple Silicon;
- потрібно уникати застарілих x86-only залежностей.

---

# 7. Git

## Що це

**Git** — система контролю версій.

## За що відповідає

Git дозволяє:

- зберігати історію змін;
- створювати окремі гілки;
- повертатися до попередніх версій;
- працювати через Pull Request;
- бачити, хто і що змінив;
- завантажувати код у GitHub.

## Перевірка версії

```bash
git --version
```

## Результат

```text
git version 2.50.1
```

## Перевірка глобального імені та email

```bash
git config --global user.name
git config --global user.email
```

## Для чого це потрібно

Git додає ім’я та email до кожного commit.

У майбутньому commit виглядатиме приблизно так:

```text
Author: Volodymyr
Message: feat: add Playwright configuration
```

---

# 8. Homebrew

## Що це

**Homebrew** — менеджер пакетів для macOS.

## За що відповідає

Homebrew дозволяє встановлювати технічні інструменти через Terminal.

Через нього ми встановлювали:

- NVM;
- GitHub CLI.

У майбутньому можемо встановлювати:

- PostgreSQL client;
- k6;
- jq;
- інші CLI-інструменти.

## Перевірка версії

```bash
brew --version
```

## Результат

```text
Homebrew 6.0.4
```

---

# 9. Node.js

## Що це

**Node.js** — середовище виконання JavaScript і TypeScript поза браузером.

## За що відповідає у нашому проєкті

Node.js потрібен для запуску:

- Playwright;
- Medusa backend;
- Next.js storefront;
- npm scripts;
- TypeScript;
- ESLint;
- Prettier;
- API tests;
- GitHub Actions jobs.

## Початковий стан

Було встановлено:

```text
Node.js v26.4.0
```

## Чому ми не залишили Node.js 26

Node.js 26 був занадто новим для стабільної роботи з нашим стеком.

Можливі ризики:

- несумісність залежностей;
- помилки під час встановлення;
- проблеми з Medusa;
- проблеми з Next.js;
- нестабільність у CI.

## Обрана версія

```text
Node.js 24 LTS
```

## Поточний результат

```text
Node.js v24.18.0
```

---

# 10. npm

## Що це

**npm** — менеджер пакетів для Node.js.

## За що відповідає

Через npm ми будемо:

- встановлювати залежності;
- запускати тести;
- запускати lint;
- запускати TypeScript check;
- запускати backend;
- запускати storefront;
- запускати Playwright reports;
- запускати підготовлені scripts.

## Перевірка

```bash
npm --version
```

## Результат

```text
11.16.0
```

## Приклад майбутніх команд

```bash
npm install
npm ci
npm test
npm run lint
npm run test:api
npm run test:ui
```

---

# 11. NVM

## Що це

**NVM** — Node Version Manager.

## За що відповідає

NVM дозволяє:

- встановлювати декілька версій Node.js;
- перемикатися між ними;
- фіксувати потрібну версію для конкретного проєкту;
- не ламати інші Node.js-проєкти;
- використовувати однакову версію локально та в CI.

## Встановлення

```bash
brew install nvm
```

## Створення директорії

```bash
mkdir -p ~/.nvm
```

## Налаштування в `~/.zshrc`

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"
[ -s "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm" ] && \. "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm"
```

## Що таке `~/.zshrc`

Це конфігураційний файл shell `zsh`.

macOS читає його при запуску нового Terminal.

У ньому можна зберігати:

- environment variables;
- aliases;
- налаштування NVM;
- додаткові PATH.

## Перезавантаження конфігурації

```bash
source ~/.zshrc
```

## Що робить команда

Вона перечитує файл `~/.zshrc` без перезапуску Terminal.

## Перевірка

```bash
nvm --version
```

## Результат

```text
0.40.6
```

---

# 12. Встановлення Node.js 24 через NVM

## Команди

```bash
nvm install 24
nvm use 24
nvm alias default 24
```

## Що робить кожна команда

### `nvm install 24`

Встановлює Node.js 24.

### `nvm use 24`

Активує Node.js 24 у поточному Terminal.

### `nvm alias default 24`

Робить Node.js 24 версією за замовчуванням.

Після відкриття нового Terminal NVM автоматично використовуватиме цю версію.

## Перевірка

```bash
node --version
npm --version
which node
```

## Результат

```text
v24.18.0
11.16.0
/Users/volodymyryankers/.nvm/versions/node/v24.18.0/bin/node
```

## Що показує `which node`

Команда показує, який саме Node.js запускається.

Правильний шлях містить:

```text
.nvm/versions/node/
```

Це означає, що Node.js керується через NVM.

---

# 13. GitHub

## Що це

**GitHub** — платформа для зберігання Git-репозиторіїв.

## За що відповідає

GitHub буде використовуватися для:

- зберігання коду;
- GitHub Issues;
- Pull Requests;
- code review;
- GitHub Actions;
- reports;
- releases;
- документації;
- портфоліо.

## Наш GitHub account

```text
Gunplay
```

---

# 14. GitHub CLI

## Що це

**GitHub CLI** або `gh` — офіційний командний інструмент GitHub.

## За що відповідає

Через `gh` можна:

- авторизуватися в GitHub;
- створювати repository;
- створювати Pull Request;
- створювати Issue;
- переглядати GitHub Actions;
- запускати workflow;
- створювати release;
- клонувати repository.

## Встановлення

```bash
brew install gh
```

## Авторизація

```bash
gh auth login
```

## Обрані параметри

```text
GitHub.com
HTTPS
Login with a web browser
```

## Чому HTTPS

HTTPS простіший для першого налаштування.

GitHub CLI автоматично керує авторизацією для Git operations.

## Перевірка

```bash
gh auth status
```

## Результат

```text
Logged in to github.com account Gunplay
Active account: true
Git operations protocol: https
```

## Безпека

GitHub token не можна:

- публікувати;
- додавати у GitHub repository;
- вставляти у `.env.example`;
- передавати іншим людям;
- показувати у відео або screenshots.

---

# 15. Docker

## Що це

**Docker** — платформа для запуску застосунків у контейнерах.

## Що таке контейнер

Контейнер — це ізольоване середовище, у якому запускається застосунок із потрібними залежностями.

## За що Docker відповідатиме в нашому проєкті

Через Docker ми будемо запускати:

- PostgreSQL;
- Redis;
- Medusa backend;
- storefront;
- Playwright test runner;
- повне локальне тестове середовище.

## Переваги

- однакове середовище на різних комп’ютерах;
- простий reset;
- ізоляція від macOS;
- простий запуск бази даних;
- підготовка до GitHub Actions;
- відтворюваність проєкту.

## Перевірка Docker CLI

```bash
docker --version
```

## Результат

```text
Docker version 29.5.3
```

---

# 16. Docker Compose

## Що це

**Docker Compose** — інструмент для запуску декількох Docker-контейнерів разом.

## За що відповідає

У майбутньому один файл `docker-compose.yml` зможе запускати:

```text
PostgreSQL
Redis
Medusa Backend
Storefront
Automation Tests
```

## Перевірка

```bash
docker compose version
```

## Результат

```text
Docker Compose version v5.1.4
```

---

# 17. Docker daemon

## Що це

Docker daemon — фоновий процес, який реально:

- створює контейнери;
- запускає контейнери;
- завантажує images;
- керує networks;
- керує volumes.

Docker CLI лише надсилає команди Docker daemon.

## Перевірка

```bash
docker info --format '{{.ServerVersion}}'
```

## Отримана помилка

```text
failed to connect to the docker API
```

## Причина

Docker Desktop був установлений, але не запущений.

## Що потрібно зробити

1. Натиснути `Command + Space`.
2. Знайти `Docker`.
3. Відкрити Docker Desktop.
4. Дочекатися повного запуску.
5. Повторити перевірку.

## Контрольна команда

```bash
docker run --rm hello-world
```

## Що вона робить

- завантажує тестовий Docker image;
- запускає контейнер;
- перевіряє Docker Engine;
- автоматично видаляє контейнер після завершення через `--rm`.

Очікуваний текст:

```text
Hello from Docker!
```

---

# 18. Перевірка вільного місця

## Команда

```bash
df -h /
```

## Що вона робить

Показує:

- загальний розмір диска;
- використане місце;
- вільне місце;
- відсоток використання.

## Результат

```text
366 GiB available
```

## Чому це важливо

Наш проєкт використовуватиме:

- Docker images;
- Docker volumes;
- PostgreSQL data;
- Redis data;
- Node.js dependencies;
- Playwright browser binaries;
- test reports;
- screenshots;
- videos;
- traces.

366 GiB — більш ніж достатньо.

---

# 19. Поточний стан середовища

| Інструмент | Версія або статус | Призначення |
|---|---|---|
| macOS | 26.5.1 | Операційна система |
| Apple Silicon | arm64 | Архітектура MacBook |
| VS Code | встановлений | Редактор коду |
| Git | 2.50.1 | Контроль версій |
| Homebrew | 6.0.4 | Встановлення CLI-інструментів |
| NVM | 0.40.6 | Керування Node.js |
| Node.js | 24.18.0 | Запуск JS/TS застосунків |
| npm | 11.16.0 | Керування Node.js пакетами |
| GitHub CLI | встановлений | Робота з GitHub через Terminal |
| GitHub account | Gunplay | Репозиторії та CI/CD |
| Docker CLI | 29.5.3 | Керування Docker |
| Docker Compose | 5.1.4 | Запуск декількох контейнерів |
| Docker daemon | треба запустити | Реальний запуск контейнерів |
| Вільне місце | 366 GiB | Достатньо для проєкту |

---

# 20. Що вже виконано

- [x] Створено робочу папку.
- [x] Перевірено macOS.
- [x] Перевірено Apple Silicon.
- [x] Перевірено Git.
- [x] Перевірено Homebrew.
- [x] Встановлено NVM.
- [x] Налаштовано NVM у `.zshrc`.
- [x] Встановлено Node.js 24 LTS.
- [x] Node.js 24 зроблено версією за замовчуванням.
- [x] Перевірено npm.
- [x] Встановлено GitHub CLI.
- [x] Виконано авторизацію GitHub.
- [x] Перевірено Docker CLI.
- [x] Перевірено Docker Compose.
- [ ] Запустити Docker Desktop.
- [ ] Перевірити Docker daemon.
- [ ] Запустити `hello-world`.
- [ ] Створити GitHub repository.
- [ ] Створити Medusa application.
- [ ] Підключити PostgreSQL.
- [ ] Запустити backend.
- [ ] Запустити Admin UI.
- [ ] Запустити storefront.
- [ ] Перевірити Store API.
- [ ] Перевірити Admin API.
- [ ] Додати Playwright.

---

# 21. Команди-шпаргалка

## Перевірка поточної папки

```bash
pwd
```

## Перехід у папку проєкту

```bash
cd ~/Projects/QA-AUTO-ROAD-MAP
```

## Перевірка Git

```bash
git --version
```

## Перевірка Node.js

```bash
node --version
```

## Перевірка npm

```bash
npm --version
```

## Перевірка NVM

```bash
nvm --version
```

## Перехід на Node.js 24

```bash
nvm use 24
```

## Перевірка GitHub

```bash
gh auth status
```

## Перевірка Docker

```bash
docker --version
docker compose version
docker info --format '{{.ServerVersion}}'
```

## Тест Docker

```bash
docker run --rm hello-world
```

---

# 22. Що я повинен уміти пояснити після цього етапу

Після завершення підготовки середовища потрібно вміти пояснити:

1. Що таке Git.
2. Чим Git відрізняється від GitHub.
3. Для чого потрібен GitHub CLI.
4. Що таке Node.js.
5. Для чого потрібен npm.
6. Що таке LTS-версія Node.js.
7. Для чого потрібен NVM.
8. Що таке Homebrew.
9. Що таке Docker.
10. Чим Docker CLI відрізняється від Docker daemon.
11. Для чого потрібен Docker Compose.
12. Чому PostgreSQL краще запускати через Docker.
13. Чому не можна публікувати tokens і secrets.
14. Чому версію Node.js потрібно фіксувати.

---

# 23. Наступний етап

Після успішної перевірки Docker:

```bash
docker info --format '{{.ServerVersion}}'
docker run --rm hello-world
```

переходимо до:

```text
QCAL-002 — Створення GitHub repository
```

Після цього почнемо створення та запуск:

```text
Medusa backend
Admin Dashboard
Next.js storefront
PostgreSQL
REST API
```

---

# 24. Детальний розбір Docker-команд

## Команда 1

```bash
docker info --format '{{.ServerVersion}}'
```

### Загальне призначення

Ця команда перевіряє, чи запущений Docker Engine, і виводить тільки версію Docker Server.

### Розбір кожної частини

#### `docker`

Це основна команда Docker CLI.

Docker CLI — інструмент, через який користувач надсилає команди Docker Engine.

Сам `docker` не запускає контейнери. Він лише звертається до Docker daemon.

#### `info`

Підкоманда `info` запитує загальну інформацію про Docker-середовище.

Без додаткових параметрів:

```bash
docker info
```

команда показує багато даних:

- версію Docker Server;
- кількість контейнерів;
- кількість images;
- тип storage driver;
- інформацію про CPU;
- доступну пам’ять;
- налаштування Docker Engine;
- дані про Docker daemon.

#### `--format`

Параметр `--format` змінює формат виводу.

Без нього Docker показує великий звіт.

З ним ми можемо вивести тільки конкретне поле.

#### `'{{.ServerVersion}}'`

Це шаблон Go Template, який Docker використовує для форматування результатів.

Розбір:

- одинарні лапки `'...'` передають шаблон як один аргумент;
- `{{ ... }}` означає шаблонний вираз;
- крапка `.` означає поточний об’єкт із даними;
- `ServerVersion` — поле, у якому знаходиться версія Docker Engine.

### Очікуваний результат

```text
29.5.3
```

### Що підтверджує успішний результат

Якщо команда повернула версію, це означає:

- Docker CLI встановлений;
- Docker Desktop запущений;
- Docker daemon працює;
- CLI може підключитися до Docker Engine;
- Docker API доступний.

### Типова помилка

```text
Cannot connect to the Docker daemon
```

або:

```text
failed to connect to the docker API
```

Це зазвичай означає, що Docker Desktop не запущений.

---

## Команда 2

```bash
docker run --rm hello-world
```

### Загальне призначення

Ця команда виконує повну тестову перевірку Docker:

1. шукає image `hello-world` локально;
2. якщо image немає — завантажує його з Docker Hub;
3. створює контейнер;
4. запускає контейнер;
5. контейнер виводить тестове повідомлення;
6. після завершення контейнер автоматично видаляється.

### Розбір кожної частини

#### `docker`

Основна команда Docker CLI.

Вона надсилає запит Docker Engine.

#### `run`

Підкоманда `run` створює і запускає новий контейнер з указаного image.

Фактично вона поєднує дві дії:

```text
docker create
+
docker start
```

Тобто:

- спочатку створюється контейнер;
- потім він одразу запускається.

#### `--rm`

Параметр `--rm` означає:

```text
видалити контейнер автоматично після завершення
```

Без `--rm` зупинений контейнер залишився б у системі.

Його можна було б побачити командою:

```bash
docker ps -a
```

З параметром `--rm` тестовий контейнер не засмічує Docker.

Важливо: видаляється контейнер, але image `hello-world` залишається локально.

#### `hello-world`

Це назва Docker image.

Image — це шаблон, з якого створюється контейнер.

`hello-world` — офіційний мінімальний тестовий image Docker.

Його задача:

- перевірити завантаження image;
- перевірити створення контейнера;
- перевірити запуск контейнера;
- підтвердити роботу Docker Engine.

### Що відбувається всередині

```text
Docker CLI
→ Docker daemon
→ перевірка локального image
→ Docker Hub, якщо image відсутній
→ завантаження image
→ створення контейнера
→ запуск контейнера
→ вивід повідомлення
→ видалення контейнера через --rm
```

### Очікуваний результат

У терміналі має з’явитися:

```text
Hello from Docker!
```

### Що підтверджує успішний результат

Команда підтверджує, що:

- Docker Desktop запущений;
- Docker daemon працює;
- Docker CLI підключається до daemon;
- є доступ до Docker Hub;
- images можуть завантажуватися;
- контейнери можуть створюватися;
- контейнери можуть запускатися;
- автоматичне видалення контейнера працює.

---

# 25. Різниця між Docker image і container

## Docker image

Image — це незмінний шаблон застосунку.

Він містить:

- файлову систему;
- залежності;
- інструкції запуску;
- необхідні бібліотеки.

Приклади:

```text
hello-world
postgres
node
```

## Docker container

Container — це запущений або створений екземпляр image.

Аналогія:

```text
Image = креслення будинку
Container = побудований будинок
```

Один image можна використати для створення багатьох контейнерів.

---

# 26. Корисні команди після тесту

## Показати запущені контейнери

```bash
docker ps
```

## Показати всі контейнери

```bash
docker ps -a
```

## Показати локальні images

```bash
docker images
```

Після запуску `hello-world` image можна побачити командою:

```bash
docker images
```

Контейнер після завершення не залишиться, тому що використаний параметр:

```bash
--rm
```

---

# 27. Фактичний результат перевірки Docker

Після запуску Docker Desktop команда:

```bash
docker info --format '{{.ServerVersion}}'
```

повернула:

```text
29.5.3
```

Це підтверджує, що:

- Docker Desktop запущений;
- Docker daemon працює;
- Docker CLI успішно підключається до Docker Engine;
- Docker API доступний;
- локальне середовище готове до запуску контейнерів.

Після цього була виконана команда:

```bash
docker run --rm hello-world
```

Docker не знайшов image `hello-world:latest` локально, тому автоматично:

1. звернувся до Docker Hub;
2. завантажив image для архітектури `arm64v8`;
3. створив контейнер;
4. запустив контейнер;
5. вивів повідомлення:

```text
Hello from Docker!
```

6. видалив контейнер після завершення через параметр `--rm`.

## Підсумок перевірки Docker

- [x] Docker CLI встановлений.
- [x] Docker Desktop запущений.
- [x] Docker daemon працює.
- [x] Docker Hub доступний.
- [x] Docker image завантажується.
- [x] Контейнер створюється.
- [x] Контейнер запускається.
- [x] Контейнер автоматично видаляється після завершення.
- [x] Apple Silicon image `arm64v8` підтримується.

---

# 28. Створення GitHub-репозиторію

## Назва репозиторію

```text
qa-commerce-automation-lab
```

## Призначення репозиторію

Репозиторій буде містити:

- вихідний код QA Automation Framework;
- Playwright-тести;
- API-тести;
- Docker-конфігурацію;
- GitHub Actions;
- документацію;
- test strategy;
- test cases;
- bug reports;
- test reports;
- інструкції для локального запуску.

## Команда створення

```bash
gh repo create qa-commerce-automation-lab --public --clone --add-readme
```

## Детальний розбір команди

### `gh`

GitHub CLI — інструмент для роботи з GitHub через Terminal.

### `repo`

Група команд для роботи з репозиторіями.

### `create`

Створює новий GitHub-репозиторій.

### `qa-commerce-automation-lab`

Назва нового репозиторію.

### `--public`

Робить репозиторій публічним.

Це потрібно, щоб:

- використовувати репозиторій як портфоліо;
- показувати його рекрутерам;
- демонструвати код на співбесіді;
- відкривати документацію без додаткового доступу.

У публічний репозиторій не можна додавати:

- паролі;
- API tokens;
- access keys;
- приватні `.env` файли;
- персональні дані;
- конфіденційні робочі матеріали.

### `--clone`

Після створення репозиторію одразу клонує його на MacBook.

Тобто створюється локальна папка:

```text
qa-commerce-automation-lab
```

яка вже підключена до GitHub.

### `--add-readme`

Автоматично створює файл:

```text
README.md
```

README — головний документ репозиторію, який GitHub показує на стартовій сторінці проєкту.

---

# 29. Перехід у локальний репозиторій

Команда:

```bash
cd qa-commerce-automation-lab
```

## Що вона робить

Переходить у локальну папку репозиторію.

Перевірка:

```bash
pwd
```

Очікуваний шлях:

```text
/Users/volodymyryankers/Projects/QA-AUTO-ROAD-MAP/qa-commerce-automation-lab
```

---

# 30. Перевірка Git-репозиторію

## Перевірка поточного стану

```bash
git status
```

Команда показує:

- поточну гілку;
- змінені файли;
- нові файли;
- staged files;
- чи є незбережені зміни.

Нормальний результат після створення репозиторію:

```text
On branch main
nothing to commit, working tree clean
```

## Перевірка віддаленого репозиторію

```bash
git remote -v
```

Команда показує адресу GitHub-репозиторію для:

- `fetch` — отримання змін;
- `push` — відправлення змін.

Очікуваний результат:

```text
origin  https://github.com/Gunplay/qa-commerce-automation-lab.git (fetch)
origin  https://github.com/Gunplay/qa-commerce-automation-lab.git (push)
```

## Що таке `origin`

`origin` — стандартне коротке ім’я віддаленого GitHub-репозиторію.

Схема:

```text
Локальний репозиторій на MacBook
            ↕
         origin
            ↕
GitHub-репозиторій qa-commerce-automation-lab
```

## Відкриття репозиторію у браузері

```bash
gh repo view --web
```

Команда відкриває поточний GitHub-репозиторій у браузері.

---

# 31. Базова структура документації

Для документації проєкту запланована така структура:

```text
docs/
├── 00-roadmap.md
├── setup/
│   └── 01-macos-environment-setup.md
├── architecture/
│   └── project-architecture.md
├── api/
│   └── api-testing.md
├── database/
│   └── postgresql.md
├── ci-cd/
│   └── github-actions.md
└── cheatsheets/
    ├── git.md
    └── docker.md
```

## Команда створення папок

```bash
mkdir -p docs/setup docs/architecture docs/api docs/database docs/ci-cd docs/cheatsheets
```

## Детальний розбір

### `mkdir`

Команда створення директорій.

Назва походить від:

```text
make directory
```

### `-p`

Параметр `-p` означає `parents`.

Він:

- створює батьківські папки автоматично;
- дозволяє створювати вкладені директорії;
- не показує помилку, якщо папка вже існує.

Наприклад:

```bash
mkdir -p docs/setup
```

створить одночасно:

```text
docs/
└── setup/
```

навіть якщо папки `docs` ще не було.

### `docs/setup`

Папка з інструкціями зі встановлення та підготовки середовища.

### `docs/architecture`

Папка з описом архітектури QA Automation Framework.

### `docs/api`

Папка з документацією API testing.

### `docs/database`

Папка з матеріалами про PostgreSQL та database testing.

### `docs/ci-cd`

Папка з документацією GitHub Actions та CI/CD.

### `docs/cheatsheets`

Папка з короткими шпаргалками по командах Git, Docker, Playwright та інших інструментах.

---

# 32. Перенесення цього документа в репозиторій

Після завантаження оновленого файла його потрібно помістити у:

```text
docs/setup/01-macos-environment-setup.md
```

Якщо файл знаходиться у `Downloads`, команда буде такою:

```bash
mv ~/Downloads/01-macos-environment-setup-v3.md docs/setup/01-macos-environment-setup.md
```

## Розбір команди

### `mv`

Команда `move`.

Вона:

- переміщує файли;
- або перейменовує файли.

### `~/Downloads/01-macos-environment-setup-v3.md`

Поточне розташування завантаженого файла.

### `docs/setup/01-macos-environment-setup.md`

Нове розташування та фінальна назва документа в репозиторії.

## Перевірка

```bash
ls -la docs/setup
```

Очікуваний файл:

```text
01-macos-environment-setup.md
```

---

# 33. Поточний прогрес проєкту

- [x] Підготовлено macOS.
- [x] Перевірено Apple Silicon `arm64`.
- [x] Перевірено Git.
- [x] Перевірено Homebrew.
- [x] Встановлено NVM.
- [x] Встановлено Node.js 24 LTS.
- [x] Налаштовано npm.
- [x] Встановлено GitHub CLI.
- [x] Виконано авторизацію GitHub CLI.
- [x] Перевірено GitHub account `Gunplay`.
- [x] Перевірено Docker CLI.
- [x] Запущено Docker Desktop.
- [x] Перевірено Docker daemon.
- [x] Успішно запущено контейнер `hello-world`.
- [x] Створено публічний GitHub-репозиторій.
- [x] Репозиторій клоновано на MacBook.
- [x] Створено початковий `README.md`.
- [ ] Створити папки документації.
- [ ] Перенести цей документ у `docs/setup`.
- [ ] Створити інші Markdown-документи.
- [ ] Виконати перший documentation commit.
- [ ] Відправити зміни через `git push`.
- [ ] Розгорнути PostgreSQL.
- [ ] Створити Medusa application.
- [ ] Запустити Medusa backend.
- [ ] Запустити Admin Dashboard.
- [ ] Запустити Storefront.
- [ ] Додати Playwright.

---

# 34. Наступні Git-команди після перенесення документа

Після того як документ буде перенесено в репозиторій:

```bash
git status
git add .
git commit -m "docs: add environment setup documentation"
git push origin main
```

## `git status`

Показує нові та змінені файли.

## `git add .`

Додає всі зміни з поточної директорії та вкладених папок у staging area.

Крапка `.` означає:

```text
поточна директорія
```

## `git commit -m "docs: add environment setup documentation"`

Створює локальну зафіксовану версію змін.

### `commit`

Зберігає набір підготовлених змін в історії Git.

### `-m`

Дозволяє вказати текст commit message прямо у команді.

### `docs:`

Префікс Conventional Commits, який означає, що зміни стосуються документації.

## `git push origin main`

Відправляє локальні commits у GitHub.

### `push`

Відправити зміни.

### `origin`

Віддалений GitHub-репозиторій.

### `main`

Основна гілка проєкту.

---

# 35. Фактичний статус середовища

| Компонент | Статус |
|---|---|
| Git | Працює |
| Homebrew | Працює |
| NVM | Працює |
| Node.js 24 LTS | Працює |
| npm | Працює |
| GitHub CLI | Працює |
| GitHub авторизація | Виконана |
| Docker Desktop | Запущений |
| Docker daemon | Працює |
| Docker Hub | Доступний |
| Docker containers | Успішно запускаються |
| GitHub repository | Створений |
| Repository clone | Створений локально |
| README.md | Створений |
| Документація | У процесі перенесення |
