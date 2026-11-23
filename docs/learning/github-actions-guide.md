# GitHub Actions і наш workflow Playwright

Практичний посібник для переходу від manual QA до автоматичного запуску тестів. Приклади спираються на QA Commerce Automation Lab. Дата розбору локальних файлів — 24 жовтня 2026.

GitHub Actions виконує записані нами дії на runner — машині для запуску автоматизації. Наш workflow готує магазин і перевіряє його браузерними тестами. Він допомагає виявити проблему після зміни коду ще до об’єднання змін у команді.

## Як вивчати

Пройди матеріал у три короткі підходи: основи й схеми — 15 хвилин; наш YAML і діагностика — 20–30 хвилин; приклади та самоперевірка — 15 хвилин. Відкрий поруч `.github/workflows/playwright.yml`, щоб пов’язувати пояснення з кодом.

Після читання ти маєш уміти пояснити: що запускає CI; де він працює; звідки бере код і дані; як знаходить тест; що означає помилка; де читати результат. Запам’ятовувати всі команди напам’ять не потрібно — важливо розуміти їхнє призначення.

### Зміст

1. [Навіщо потрібна автоматизація запуску](#навіщо-потрібна-автоматизація-запуску)
2. [Терміни та карта процесу](#терміни-та-карта-процесу)
3. [Твій Mac і машина GitHub](#твій-mac-і-машина-github)
4. [Як читати YAML](#як-читати-yaml)
5. [Наш workflow від початку до кінця](#наш-workflow-від-початку-до-кінця)
6. [Як тест потрапляє в CI](#як-тест-потрапляє-в-ci)
7. [Де дивитися результат](#де-дивитися-результат)
8. [Як шукати причину падіння](#як-шукати-причину-падіння)
9. [Приклади з командної роботи](#приклади-з-командної-роботи)
10. [Навчальні фрагменти конфігурації](#навчальні-фрагменти-конфігурації)
11. [Поточний стан нашого CI](#поточний-стан-нашого-ci)
12. [Самоперевірка та шпаргалка](#самоперевірка-та-шпаргалка)
13. [Джерела](#джерела)
14. [Копія нашого workflow з поясненням кожного рядка](#копія-нашого-workflow-з-поясненням-кожного-рядка)

## Навіщо потрібна автоматизація запуску

Уяви команду магазину: один розробник змінює реєстрацію, другий — кошик, ти додаєш тести. На твоєму Mac є встановлені пакети, запущена БД і вручну підготовлений магазин. В іншої людини умови можуть відрізнятися.

Після кожного набору змін команда хоче однаково перевіряти критичні сценарії: чи можна зареєструватися, увійти, переглянути товар. Без автоматизації хтось повинен щоразу встановлювати залежності, запускати сервіси й тести та передавати результат колегам.

Workflow записує цю послідовність у репозиторії. GitHub запускає її за заданою подією, зберігає лог і прив’язує результат до конкретних змін. Якщо залежність не встановилася або тест упав, команда бачить, на якому кроці це сталося.

Зелений CI означає успішне виконання налаштованих перевірок для цього запуску. Повнота покриття залежить від самих тестів: якщо в них немає перевірки оплати, зелений результат нічого не доводить про оплату.

## Терміни та карта процесу

| Термін | Значення | Приклад у нас |
|---|---|---|
| Git | Система історії змін | Коміти у твоїй гілці |
| GitHub | Сервіс зберігання репозиторіїв і командної роботи | Віддалений репозиторій |
| GitHub Actions | Платформа автоматизації | Запускає наш YAML |
| Workflow | Повний сценарій автоматизації | `Playwright E2E` |
| Event | Подія запуску | Push у `feat/playwright-setup` |
| Workflow run | Один конкретний запуск | Результат певного push |
| Job | Задача всередині workflow | `e2e` |
| Runner | Машина, що виконує job | Ubuntu на GitHub |
| Step | Окремий крок job | Установлення браузера |
| Action | Готовий компонент для кроку | `actions/checkout` |
| Script | Наші команди термінала | `npm ci` |
| Artifact | Збережені файли результату | HTML-звіт |
| Cache | Повторно використовувані завантаження | Кеш npm |
| CI | Continuous Integration, безперервна інтеграція | Перевірка змін тестами |
| CD | Continuous Delivery або Deployment | Підготовка випуску або автоматичний деплой |
| Deploy | Розгортання версії застосунку | Оновлення staging |
| Staging | Середовище перед production | Тестова копія магазину |
| Production | Середовище реальних користувачів | Робочий магазин |

Один workflow може містити кілька jobs. У нас одна job і послідовні steps. У складнішому процесі незалежні jobs можуть виконуватися паралельно, а залежності задаються через `needs`. Основні поняття пояснює [GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions).

![Шлях від зміни коду до результату CI](artifacts/github-actions-lifecycle.svg)

[Відкрити схему окремо](artifacts/github-actions-lifecycle.svg).

## Твій Mac і машина GitHub

| Питання | Локально | У нашому CI |
|---|---|---|
| Де код | У твоїй папці | У робочій папці runner після checkout |
| Звідки зміни | Збережені локальні файли | Код відповідного GitHub запуску |
| Хто запускає | Ти з термінала | GitHub за `on:` |
| База | Твій локальний PostgreSQL | Окремий контейнер на runner |
| Налаштування | Локальне середовище | `env` та інші налаштовані джерела CI |
| Браузер | Можна бачити через `--headed` | Без видимого вікна |
| Що після завершення | Файли й БД залишаються | Тимчасова VM прибирається; явно завантажені артефакти зберігаються окремо |

`localhost` завжди означає поточну машину. `localhost:8000` у тесті на GitHub звертається до магазину на runner. Для цього наш YAML спочатку запускає storefront саме там.

![Компоненти нашої задачі на runner](artifacts/github-actions-runner.svg)

[Відкрити схему окремо](artifacts/github-actions-runner.svg).

На схемі показано, де працюють компоненти. У негативному тесті порожньої форми HTML-валідація блокує відправлення; сам submit не повинен створювати покупця. У позитивному тесті реєстрації потрібна взаємодія з backend і БД.

## Як читати YAML

```yaml
jobs:
  e2e:
    steps:
      - name: Install dependencies
        run: npm ci
```

`steps` належить `e2e`, а `e2e` належить `jobs`. `name` і `run` описують один елемент списку кроків. Відступи робимо пробілами й зберігаємо однаковими для одного рівня.

| Позначення | Значення |
|---|---|
| `key: value` | Назва налаштування та значення |
| `# пояснення` | Коментар |
| `- name:` | Новий елемент списку |
| `uses:` | Виклик готового action |
| `with:` | Параметри цього action |
| `run:` | Команда shell |
| `run: \|` | Багаторядковий shell-сценарій; у справжньому YAML після двокрапки стоїть звичайний `|` |

Порівняй: `uses: actions/setup-node@v4` викликає готовий інструмент, а `run: npm ci` виконує нашу команду. `@v4` — версія action; вона не є версією Node.js.

## Наш workflow від початку до кінця

### Назва та події

```yaml
name: Playwright E2E
on:
  push:
    branches:
      - main
      - feat/playwright-setup
  pull_request:
```

`name` задає підпис у GitHub Actions. `on` описує запуск: push у дві вказані гілки та стандартні події PR — відкриття, нові коміти й повторне відкриття. Для PR тут немає фільтра цільової гілки. Якщо push також оновлює відкритий PR, можуть виникнути два запуски через дві різні події.

У нашому файлі немає `workflow_dispatch`, тому кнопку ручного запуску цей YAML не налаштовує. Немає й `schedule`, тому запуску за часом він не задає.

### Задача та машина

```yaml
jobs:
  e2e:
    name: Storefront smoke test
    runs-on: ubuntu-latest
    timeout-minutes: 20
```

`e2e` — технічний ID задачі; `Storefront smoke test` — її підпис. `ubuntu-latest` вибирає образ Ubuntu runner; конкретний образ може з часом оновлюватися. `timeout-minutes` обмежує всю job двадцятьма хвилинами, а не кожен тест окремо.

### Змінні середовища

`env` у нашому файлі знаходиться на рівні job й передає налаштування її крокам.

| Змінна | Призначення |
|---|---|
| `DATABASE_URL` | Рядок підключення backend до PostgreSQL |
| `STORE_CORS` | Дозволений origin для браузерних звернень до Store API |
| `ADMIN_CORS` | Дозволений origin для Admin API |
| `AUTH_CORS` | Дозволені origins для автентифікації |
| `JWT_SECRET` | Ключ підпису токенів |
| `COOKIE_SECRET` | Ключ підпису cookies |
| `NEXT_PUBLIC_MEDUSA_BACKEND_URL` | Адреса backend для storefront |
| `NEXT_PUBLIC_BASE_URL` | Базова адреса магазину |

Origin — поєднання протоколу, хоста й порту. Через різні порти магазин на `8000` і backend на `9000` мають різні origins. CORS регулює браузерний доступ; він не замінює перевірку прав користувача.

У YAML є відкриті тестові значення для тимчасового CI-середовища. Для реальних приватних токенів використовують GitHub Secrets, наприклад `${{ secrets.STAGING_TOKEN }}`. Змінні з префіксом `NEXT_PUBLIC_` у Next.js можуть потрапляти в клієнтський код, тому приватні секрети туди не кладуть. Дивись [роботу із secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets) та [змінні Next.js](https://nextjs.org/docs/app/guides/environment-variables).

### Отримання коду

```yaml
- name: Checkout repository
  uses: actions/checkout@v4
```

`steps` починає список кроків. Checkout отримує код запуску в робочу папку runner. Для PR стандартний checkout зазвичай перевіряє підготовлений GitHub merge ref, щоб тестувати поєднання змін PR з базовою гілкою. Незбережений файл у твоєму редакторі runner не бачить. [Поведінка checkout](https://github.com/actions/checkout).

### Підготовка Node.js

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: npm
```

Node.js потрібен для backend, Next.js і Playwright. `with` передає параметри action. `node-version` вибирає Node 20; `cache: npm` налаштовує кеш завантажень npm. Кеш не переносить готовий локальний `node_modules` із Mac і не замінює наступний `npm ci`. [Опис setup-node](https://github.com/actions/setup-node).

### Залежності та браузер

```yaml
- name: Install dependencies
  run: npm ci
- name: Install Playwright browser
  run: npx playwright install --with-deps chromium
```

`npm ci` установлює залежності за lock-файлом; невідповідність між `package.json` і `package-lock.json` спричиняє помилку. Команда може запускати lifecycle-скрипти пакетів. [Правила npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci).

Наступна команда встановлює Chromium і системні бібліотеки Linux. npm-пакет Playwright і виконуваний браузер — різні складові. Наш `playwright.config.ts` має Chromium project, тому вибір браузера узгоджений із ним. [Playwright у CI](https://playwright.dev/docs/ci).

### PostgreSQL

```yaml
- name: Start PostgreSQL
  run: docker compose up -d postgres
```

Compose читає `compose.yaml`. `up` створює й запускає сервіс `postgres`; `-d` залишає контейнер у фоні. Сам факт старту процесу ще не доводить готовності БД приймати з’єднання, тому далі є окреме очікування.

```bash
for i in {1..30}; do
  if docker compose ps postgres | grep -q "healthy"; then
    echo "PostgreSQL is ready"
    exit 0
  fi
  echo "Waiting for PostgreSQL..."
  sleep 2
done
docker compose ps
exit 1
```

Це shell-код усередині `run: |`.

| Рядок | Пояснення |
|---|---|
| `for i in {1..30}; do` | До 30 спроб, номер спроби зберігається в `i` |
| `docker compose ps postgres` | Отримати стан сервісу |
| `\| grep -q "healthy"` | Передати вивід пошуку тексту; `-q` приховує знайдений текст |
| `if ...; then` | Виконати блок, якщо команда повернула успіх |
| `echo ...` | Надрукувати повідомлення в лог |
| `exit 0` | Успішно завершити поточний shell-крок |
| `fi` | Закрити `if` |
| `sleep 2` | Пауза дві секунди |
| `done` | Закрити цикл |
| `docker compose ps` після циклу | Показати стан сервісів після вичерпання спроб |
| `exit 1` | Завершити крок помилкою |

У поточній команді є недолік: `healthy` також є частиною слова `unhealthy`. Надійніше перевіряти точний health status. Це пункт наступної доробки workflow.

### Структура та дані БД

```yaml
- name: Set up database
  run: npm run db:setup
```

У нашому `package.json`: `db:setup` виконує `npm run backend:migrate && npm run backend:seed`. Міграції готують структуру; seed додає початкові дані. `&&` дозволяє почати seed лише після успіху міграцій. Скрипт seed — `apps/backend/src/scripts/seed.ts`.

Ця команда змінює базу. У workflow її призначення — підготовка окремої CI-бази. Наявність потрібного seed на диску не доводить його успішного виконання на GitHub.

### Запуск застосунків

```bash
npm run dev --workspace=apps/backend &
BACKEND_PID=$!
npm run dev --workspace=apps/storefront &
STOREFRONT_PID=$!
echo "Backend PID: $BACKEND_PID, Storefront PID: $STOREFRONT_PID"
```

`--workspace` вибирає пакет монорепозиторію — репозиторію з кількома застосунками. У backend скрипт запускає `medusa develop`; у storefront — `next dev --turbopack -p 8000`.

`&` запускає процес у фоні, щоб shell міг виконувати наступні команди. `$!` повертає PID останньої фонової команди; PID — номер процесу. `BACKEND_PID` і `STOREFRONT_PID` зберігають ці номери; зараз вони лише друкуються.

Кожен `run` має окремий shell, але працює в тій самій job на runner. Звичайна shell-змінна не переноситься автоматично в наступний крок. Для передачі env наступним крокам використовують файл `$GITHUB_ENV`. Сам перехід до наступного кроку не означає автоматичного знищення всіх запущених у фоні процесів; коментар нашого YAML про це потребує уточнення. [Передача env між кроками](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands#setting-an-environment-variable).

### Очікування готовності застосунків

Для backend виконується цикл до 60 спроб:

```bash
if curl -f http://localhost:9000/health > /dev/null 2>&1; then
  echo "Backend is ready"
  break
fi
```

`curl` робить HTTP-запит. `-f` повертає помилку для HTTP 400 і вище. `> /dev/null` приховує звичайний вивід; `2>&1` спрямовує туди ж помилки. Успіх означає, що перевірка доступності пройшла; він не доводить роботу всіх API.

`break` виходить лише з циклу, тому далі можемо перевіряти storefront. `exit` завершив би весь поточний shell-сценарій.

```bash
echo "Waiting for backend..."
sleep 2
if [ "$i" -eq 60 ]; then
  echo "Backend did not become ready in time"
  exit 1
fi
```

`-eq` порівнює числа. Після останньої невдалої спроби крок падає. 60 пауз по дві секунди дають близько двох хвилин плюс час запитів. Без власного timeout у `curl` це не точна двохвилинна межа.

Storefront перевіряється таким самим циклом через `http://localhost:8000/de/store`. Доступність цього URL не гарантує роботи `/dk/account`: тесту реєстрації потрібні й дані країни `dk`.

### Тести та звіт

```yaml
- name: Run Playwright tests
  run: npx playwright test
```

Playwright читає `playwright.config.ts`, знаходить тести в `tests/ui` і запускає налаштований Chromium project. Тут немає `-g`, тому вибір не обмежено назвою негативного тесту. Наявні позитивний тест реєстрації та тест каталогу також потрапляють у набір.

```yaml
- name: Upload Playwright report
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: playwright-report
    path: playwright-report/
    retention-days: 7
```

`if: always()` дозволяє запуск цього кроку й після попередньої помилки. `upload-artifact` завантажує вміст указаної папки. `name` всередині `with` — назва артефакту, а `path` — шлях на runner. `retention-days` задає строк зберігання сім днів у межах правил сховища.

Крок завантаження не створює звіт. Якщо папки немає, action за стандартними параметрами повідомляє попередження. Наш config поки не вмикає HTML reporter. Для нього можна окремо додати `reporter: [['html', { open: 'never' }]]`. [HTML reporter](https://playwright.dev/docs/test-reporters#html-reporter), [upload-artifact](https://github.com/actions/upload-artifact).

## Як тест потрапляє в CI

```text
Збереження файлу → git add → git commit → git push
                                           ↓
                               подія push на GitHub
                                           ↓
                          workflow → npx playwright test
                                           ↓
                  playwright.config.ts → tests/ui/*.spec.ts
                                           ↓
                         registration.spec.ts → RegistrationPage
```

| Дія | Що змінює |
|---|---|
| `⌘ + S` | Зберігає файл на диску Mac |
| `git status --short` | Показує локальні зміни |
| `git diff` | Показує змінені рядки відстежуваних файлів |
| `git diff --stat` | Показує їхню коротку статистику; нові untracked файли сюди не входять |
| `git add <шлях>` | Вибирає версію файлу для наступного коміту |
| `git commit` | Записує підготовлені зміни в локальну історію |
| `git push` | Відправляє коміти у віддалений репозиторій |

У твоєму поточному стані є багато змін застосунку, конфігурації та нових файлів. Перед комітом треба визначити залежності CI й вибрати узгоджений набір. POM має потрапити в репозиторій разом зі spec, який його імпортує.

Приклад команди локального запуску тільки нашого негативного тесту:

```bash
npx playwright test tests/ui/registration.spec.ts -g "customer cannot register" --headed
```

Ця команда вже дала у твоєму запуску `1 passed`. Вона не запускає GitHub Actions. У CI використовується ширша команда `npx playwright test`, тому потрібна готовність середовища для всього набору.

## Де дивитися результат

1. Відкрий репозиторій на GitHub і вкладку **Actions**.
2. Вибери **Playwright E2E**.
3. Відкрий запуск із потрібною гілкою й комітом. Для запуску PR GitHub може показувати службовий merge commit.
4. Відкрий задачу **Storefront smoke test**.
5. Розгорни потрібний step і прочитай лог.
6. Якщо артефакт створено й завантажено, знайди його на сторінці запуску в блоці **Artifacts**.

Назви й вигляд елементів інтерфейсу можуть змінюватися; орієнтир — запуск → job → step → log. GitHub описує це в [перегляді запусків](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs).

Якщо завантажив HTML-звіт, розпакуй його. Для папки з розпакованим звітом можна виконати `npx playwright show-report <шлях-до-папки>`. Потрібен реальний завантажений звіт; консольний лог не є HTML-звітом.

## Як шукати причину падіння

Починай із першого невдалого кроку. Позначка skipped у тестів після невдалого встановлення залежностей означає, що до них ще не дійшли.

| Де впало | Що перевірити | Що це означає для тестів |
|---|---|---|
| Install dependencies | Lock-файл, версію Node, помилку npm | Тести ще не запускалися |
| Install Playwright browser | Завантаження Chromium і системні залежності | Браузер не підготовлений |
| Wait for PostgreSQL | Health status, логи контейнера | БД не підтвердила готовність |
| Set up database | Текст помилки міграції або seed | Середовище не підготовлене |
| Wait for backend | Логи backend, URL БД, порт | Backend недоступний за перевіркою |
| Wait for storefront | Логи Next.js, publishable key, регіони | Магазин недоступний за перевіркою |
| Run Playwright tests | Назву тесту, очікуване й отримане, screenshot | Аналізуємо продукт, тест та середовище |
| Upload Playwright report | Чи створено папку звіту | Це окреме питання збереження доказів |

Приклад: `toBeFocused()` очікував First name, але фокус залишився на Join. Можливі причини: зник `required`, локатор вибрав іншу форму, змінився submit. Це напрямки перевірки, а не готовий висновок про дефект.

Повторний запуск корисний для перевірки випадкового збою. Якщо падіння повторюється, досліджуй причину. Автоматичні retries не повинні приховувати нестабільність тестів.

## Приклади з командної роботи

Нижче — навчальні ситуації, побудовані за робочими сценаріями. Вони не описують впровадження конкретної компанії.

### Магазин і перевірка pull request

Розробник змінює форму реєстрації та випадково прибирає `required` у First name. Він відкриває PR. CI піднімає тестовий магазин, запускає негативний тест, і перевірка `valueMissing` падає.

QA читає лог і порівнює фактичну поведінку з вимогою. Розробник виправляє форму й відправляє новий коміт; PR запускає перевірки ще раз. Якщо репозиторій окремо налаштований вимагати цей успішний check, невдала перевірка блокує merge. Сам YAML таке правило захисту гілки не створює. [Required status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

Цінність: команда отримує сигнал до включення зміни в основну гілку.

### API сервіс і матриця версій

Команда підтримує бібліотеку або сервіс на кількох заявлених версіях Node. Workflow запускає однакові перевірки з різними значеннями матриці. Один варіант може пройти, інший упасти через несумісність.

Цінність: перевіряється заявлена сумісність. Для нашого першого CI досить однієї узгодженої версії; матриця додає час і витрати.

### Нічна регресія на staging

На кожен PR команда запускає короткий smoke набір. Окремий workflow за розкладом запускає довші сценарії в Chromium, Firefox і WebKit проти staging. Він може знайти проблему зовнішньої інтеграції навіть без нового коміту в нашому репозиторії.

Для цього потрібні доступне середовище, ізольовані тестові дані й установлені браузери. Розклад не гарантує запуску рівно в задану секунду. У нас такого workflow поки немає.

Цінність: довгі перевірки не затримують кожен PR, але регулярно дають сигнал про ширший набір сценаріїв.

### Випуск нової версії

Після merge у main команда збирає застосунок, розгортає його на staging і запускає smoke. Далі відповідальна людина може погодити production deploy через захищене environment. Конкретні команди залежать від хостингу й прав доступу.

![Приклад розвитку CI до випуску на production](artifacts/github-actions-release.svg)

[Відкрити схему окремо](artifacts/github-actions-release.svg).

Цінність: можна простежити зв’язок між кодом, перевірками та розгорнутою версією. Наш workflow наразі завершується тестами й спробою збереження звіту; деплою в ньому немає. CI може бути частиною CD, але успішний CI сам по собі не публікує магазин.

## Навчальні фрагменти конфігурації

Це окремі приклади для читання. Вони не є заміною нашого повного workflow й не додані до виконуваної конфігурації.

### Ручний запуск і розклад

```yaml
on:
  workflow_dispatch:
  schedule:
    - cron: '0 3 * * *'
```

`workflow_dispatch` додає можливість ручного запуску; для її роботи workflow має бути на default branch. Cron вище означає щодня о 03:00 UTC. Для Києва місцевий час залежить від чинного зсуву UTC. Scheduled workflow працює з default branch; можливі затримки. [Синтаксис подій](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

### Залежність між jobs

```yaml
jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Тут були б checkout, залежності й перевірки"
  release:
    needs: checks
    runs-on: ubuntu-latest
    steps:
      - run: echo "Перевірки успішні; тут були б кроки випуску"
```

`needs: checks` задає залежність: за звичайних умов release починається після успіху checks. `echo` у цьому прикладі лише друкує текст. Кожна job має власний runner; код і файли збірки між jobs передають явно.

### Передача значення наступним крокам

```bash
echo "EXAMPLE_MODE=ci" >> "$GITHUB_ENV"
```

GitHub підхопить це значення в наступних кроках тієї самої job. Поточний shell не отримує його автоматично назад. Для нашого publishable key треба додатково визначити спосіб отримання ключа саме з CI-бази та перевірити його зв’язок із sales channel.

## Поточний стан нашого CI

| Частина | Що є в локальному коді на 24 жовтня |
|---|---|
| Події | Push у main і feat/playwright-setup; PR |
| Сервіси | PostgreSQL, backend і storefront описані |
| Дані | `db:setup` викликає міграції й seed; seed містить de та dk |
| Тести | Команда запускає весь набір tests/ui |
| Негативний тест | Учень надав локальний результат 1 passed; перевіряє First name |
| Повне REG-04 | Інші обов’язкові поля ще не перевірені цим тестом |
| Publishable key | SDK і middleware читають NEXT_PUBLIC_MEDUSA_PUBLISHABLE_KEY, а workflow його поки не передає |
| Seed ключа | Створює publishable key за потреби; зв’язок ключа з sales channel треба перевірити окремо |
| Готовність БД | Пошук healthy має неточність зі збігом unhealthy |
| HTML-звіт | Upload є, HTML reporter у config не ввімкнено |
| Trace | on-first-retry є, retries у config не задані; за цим config повторів немає й trace не виникне |
| GitHub CI | Успішний запуск ще не підтверджено |
| Deploy | Не налаштований |

Послідовність наступних робіт: узгодити зміни для коміту → підготувати CI key і точну перевірку БД → налаштувати звіт → перевірити весь локальний набір за потреби → commit і push → прочитати GitHub run. Результат вивчення цього посібника перевіримо окремо; сам факт отримання документа не є засвоєнням.

## Самоперевірка та шпаргалка

Спочатку відповідай без підглядання:

1. Чи запустить CI натискання Command + S?
2. Чому runner не використовує запущену на твоєму Mac БД?
3. Чим workflow відрізняється від job і step?
4. Чим `uses` відрізняється від `run`?
5. Навіщо чекати `/health` після запуску backend?
6. Чому новий spec не потрібно окремо вписувати в YAML?
7. Чи означає падіння `npm ci`, що тест реєстрації знайшов дефект?
8. Чи створює upload-artifact HTML-звіт?
9. Чи забороняє наш YAML сам по собі merge невдалого PR?
10. Чи розгортається production після нашого зеленого CI?

### Відповіді

1. Ні. Потрібна подія GitHub, описана в `on`.
2. Це інша машина; її localhost належить їй.
3. Workflow — весь сценарій; job — задача; step — її крок.
4. Uses викликає action, run виконує shell-команди.
5. Старт процесу не означає готовності обробляти запити.
6. Конфігурація Playwright знаходить spec у tests/ui.
7. Ні, тест ще не запустився: спочатку аналізуємо залежності.
8. Ні, він завантажує вже створені файли.
9. Ні, потрібне окреме правило required checks.
10. Ні, кроків деплою в нас немає.

### Вправа на перенесення

Уяви: команда просить запускати короткі тести на PR, а всі браузери — щоночі. Поясни своїми словами: які події потрібні, які набори запускати, де живе магазин і де знайти докази падіння. Критерій завершення — можеш намалювати шлях від зміни до результату та визначити перший крок для діагностики без копіювання готової відповіді.

### Швидке повторення

```text
on       → коли запускати
jobs     → які задачі виконати
runs-on  → на якій машині
env      → які налаштування передати
steps    → у якому порядку діяти
uses     → який готовий action викликати
with     → які параметри йому передати
run      → яку команду виконати
if       → за якої умови виконати крок
artifact → які файли результату зберегти
```

Під час падіння: правильний run → перший невдалий step → конкретна помилка → перевірка припущення → виправлення → новий запуск.

## Джерела

Визначення та приклади вище мають посилання поруч із відповідними поясненнями. Для детального пошуку параметра відкривай офіційні довідники; локальний код залишається джерелом опису нашого поточного стану.

- [Основи GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions).
- [Довідник синтаксису workflow](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).
- [Playwright у CI](https://playwright.dev/docs/ci).
- [HTML-звіти Playwright](https://playwright.dev/docs/test-reporters#html-reporter).
- [Повторні спроби тестів](https://playwright.dev/docs/test-retries).
- Локальні файли: `.github/workflows/playwright.yml`, `playwright.config.ts`, `compose.yaml`, `package.json`, `apps/backend/package.json`, `apps/storefront/package.json`, `apps/backend/src/scripts/seed.ts`, `apps/storefront/src/lib/config.ts`, `apps/storefront/src/middleware.ts`, `tests/ui/registration.spec.ts`, `tests/pages/registrationPage.ts`.

## Копія нашого workflow з поясненням кожного рядка

Нижче збережено знімок файлу на дату посібника. Номери в таблиці стосуються цього знімка. Порожні рядки лише розділяють блоки; рядки `#` — коментарі. Якщо робочий YAML зміниться, для фактичного запуску GitHub використовуватиме його нову версію.

```yaml
# Назва workflow — відображається у вкладці "Actions" на GitHub
name: Playwright E2E

# Умови, за яких запускається workflow
on:
  push:
    branches:
      - main                     # запуск при пуші в main
      - feat/playwright-setup    # запуск при пуші в цю фіча-гілку (зазвичай прибирають перед мержем)
  pull_request:                  # запуск на кожен pull request, незалежно від цільової гілки

# Список задач (jobs), які виконуються в рамках workflow
jobs:
  e2e:                            # ідентифікатор джоби (використовується у посиланнях, статусах тощо)
    name: Storefront smoke test   # людиночитабельна назва джоби, показується в UI
    runs-on: ubuntu-latest        # на якій ОС/образі виконується джоба
    timeout-minutes: 20           # якщо джоба виконується довше — примусово зупиняється (захист від "зависання" на wait-циклах)

    env: # Змінні середовища для всіх кроків job e2e.
      DATABASE_URL: postgres://medusa:medusa_password@localhost:5432/medusa_db # Підключення backend до тестової БД із compose.yaml: користувач, пароль, хост, порт, назва БД.
      STORE_CORS: http://localhost:8000 # Дозволений origin браузерних запитів магазину до Store API.
      ADMIN_CORS: http://localhost:9000 # Дозволений origin браузерних запитів адмінпанелі до Admin API.
      AUTH_CORS: http://localhost:8000,http://localhost:9000 # Дозволені origins магазину й адмінпанелі для API автентифікації.
      JWT_SECRET: ci-only-jwt-secret-for-tests # Ключ підпису JWT; відкрите тестове значення лише для CI.
      COOKIE_SECRET: ci-only-cookie-secret-for-tests # Ключ підпису cookies backend; відкрите тестове значення лише для CI.
      NEXT_PUBLIC_MEDUSA_BACKEND_URL: http://localhost:9000 # Адреса backend для SDK і middleware storefront.
      NEXT_PUBLIC_BASE_URL: http://localhost:8000 # Базова адреса магазину для формування посилань.
    steps:
      # 1. Клонуємо репозиторій у робочу директорію раннера
      - name: Checkout repository
        uses: actions/checkout@v4   # офіційний action для checkout коду

      # 2. Встановлюємо потрібну версію Node.js та кешуємо npm-залежності
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20     # версія Node.js, яку треба встановити
          cache: npm           # кешувати ~/.npm між запусками — прискорює наступні збірки

      # 3. Встановлюємо npm-залежності проєкту суворо за package-lock.json
      - name: Install dependencies
        run: npm ci    # "ci" замість "install" — детермінований, чистий інсталл, швидший у CI

      # 4. Встановлюємо браузер Chromium разом з системними залежностями, потрібними Playwright
      - name: Install Playwright browser
        run: npx playwright install --with-deps chromium
        # --with-deps ставить системні бібліотеки (fonts, libs), без яких Chromium не запуститься на ubuntu-latest

      # 5. Піднімаємо контейнер PostgreSQL у фоновому режимі через docker compose
      - name: Start PostgreSQL
        run: docker compose up -d postgres
        # -d = detached, тобто команда одразу повертає керування, а контейнер лишається жити у фоні

      # 6. Чекаємо, поки PostgreSQL стане "healthy" (тобто дійсно готовий приймати з'єднання)
      - name: Wait for PostgreSQL
        run: |
          for i in {1..30}; do                                   # максимум 30 спроб
            if docker compose ps postgres | grep -q "healthy"; then  # перевіряємо статус healthcheck
              echo "PostgreSQL is ready"
              exit 0                                              # успіх — виходимо з кроку з кодом 0
            fi
            echo "Waiting for PostgreSQL..."
            sleep 2                                                # пауза 2 секунди між спробами (макс. ~60с очікування)
          done
          docker compose ps    # якщо цикл вичерпався — виводимо стан контейнерів для діагностики в логах
          exit 1                # завершуємо крок з помилкою, щоб job впала явно, а не тихо продовжила

      # 7. Створюємо схему БД і тестові дані для чистого CI-контейнера.
      - name: Set up database
        run: npm run db:setup

      # 8. Стартуємо backend і storefront у фоні ТА чекаємо їх готовності В МЕЖАХ ОДНОГО КРОКУ.
      #    Важливо: якщо винести "npm run dev ... &" в окремий крок, GitHub Actions
      #    може прибити фоновий процес по завершенні цього кроку (кожен run — новий shell).
      #    Тому запуск і очікування об'єднані в один run-блок.
      - name: Start backend and storefront, then wait until ready
        run: |
          npm run dev --workspace=apps/backend &     # запускаємо backend у фоні (& = фоновий процес)
          BACKEND_PID=$!                              # зберігаємо PID backend-процесу (може знадобитись для дебагу)

          npm run dev --workspace=apps/storefront &   # запускаємо storefront у фоні
          STOREFRONT_PID=$!                            # зберігаємо PID storefront-процесу

          echo "Backend PID: $BACKEND_PID, Storefront PID: $STOREFRONT_PID"

          # Очікування готовності backend (порт 9000)
          for i in {1..60}; do
           if curl -f http://localhost:9000/health > /dev/null 2>&1; then
              # -f  — curl поверне помилку при HTTP-статусах >=400 (щоб не вважати 404 "готовим")
              # > /dev/null 2>&1 — приховуємо вивід curl, нам важливий лише код завершення
              echo "Backend is ready"
              break                    # виходимо з циклу очікування backend, ідемо далі
            fi
            echo "Waiting for backend..."
            sleep 2
            if [ "$i" -eq 60 ]; then
              echo "Backend did not become ready in time"
              exit 1                   # якщо після 60 спроб не піднявся — падаємо з помилкою
            fi
          done

          # Очікування готовності storefront (порт 8000, конкретна сторінка /de/store)
          for i in {1..60}; do
            if curl -f http://localhost:8000/de/store > /dev/null 2>&1; then
              echo "Storefront is ready"
              break
            fi
            echo "Waiting for storefront..."
            sleep 2
            if [ "$i" -eq 60 ]; then
              echo "Storefront did not become ready in time"
              exit 1
            fi
          done

      # 9. Запускаємо самі E2E-тести Playwright проти піднятих backend + storefront
      - name: Run Playwright tests
        run: npx playwright test

      # 10. (Опційно, рекомендується) Зберігаємо HTML-звіт Playwright як артефакт,
      #    щоб можна було завантажити й переглянути скріншоти/трейси при падінні тестів
      - name: Upload Playwright report
        if: always()    # виконати навіть якщо попередній крок (тести) впав — звіт потрібен саме тоді
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report      # назва артефакту, під якою він буде видимий в UI Actions
          path: playwright-report/     # шлях до директорії зі звітом (стандартний вивід Playwright)
          retention-days: 7            # скільки днів зберігати артефакт перед автоматичним видаленням
```

### Пояснення рядків знімка

| Рядок | Код без коментаря | Що робить |
|---|---|---|
| 2 | <code>name: Playwright E2E</code> | Назва всього workflow у вкладці Actions. |
| 5 | <code>on:</code> | Блок подій запуску. |
| 6 | <code>push:</code> | Запуск за подією push із фільтром нижче. |
| 7 | <code>branches:</code> | Список гілок для push. |
| 8 | <code>- main</code> | Запуск після push у main. |
| 9 | <code>- feat/playwright-setup</code> | Запуск після push у поточну навчальну гілку. |
| 10 | <code>pull_request:</code> | Стандартні події PR; фільтра цільової гілки тут немає. |
| 13 | <code>jobs:</code> | Оголошення задач. |
| 14 | <code>e2e:</code> | Технічний ID єдиної задачі. |
| 15 | <code>name: Storefront smoke test</code> | Назва job; не фільтрує тести. |
| 16 | <code>runs-on: ubuntu-latest</code> | Виконувати job на Ubuntu runner. |
| 17 | <code>timeout-minutes: 20</code> | Обмежити всю job двадцятьма хвилинами. |
| 19 | <code>env:</code> | Змінні середовища на рівні job. |
| 20 | <code>DATABASE_URL: postgres://medusa:medusa_password@localhost:5432/medusa_db</code> | Підключення до CI-бази. |
| 21 | <code>STORE_CORS: http://localhost:8000</code> | Дозволений origin Store API. |
| 22 | <code>ADMIN_CORS: http://localhost:9000</code> | Дозволений origin Admin API. |
| 23 | <code>AUTH_CORS: http://localhost:8000,http://localhost:9000</code> | Дозволені origins автентифікації. |
| 24 | <code>JWT_SECRET: ci-only-jwt-secret-for-tests</code> | Тестовий ключ підпису токенів. |
| 25 | <code>COOKIE_SECRET: ci-only-cookie-secret-for-tests</code> | Тестовий ключ підпису cookies. |
| 26 | <code>NEXT_PUBLIC_MEDUSA_BACKEND_URL: http://localhost:9000</code> | URL backend для storefront. |
| 27 | <code>NEXT_PUBLIC_BASE_URL: http://localhost:8000</code> | Базовий URL магазину. |
| 28 | <code>steps:</code> | Початок списку послідовних кроків. |
| 30 | <code>- name: Checkout repository</code> | Назва наступного кроку в логах: Checkout repository. |
| 31 | <code>uses: actions/checkout@v4</code> | Отримати код через action checkout версії v4. |
| 34 | <code>- name: Setup Node.js</code> | Назва наступного кроку в логах: Setup Node.js. |
| 35 | <code>uses: actions/setup-node@v4</code> | Підготувати Node через action setup-node версії v4. |
| 36 | <code>with:</code> | Параметри action цього кроку. |
| 37 | <code>node-version: 20</code> | Вибрати Node.js 20. |
| 38 | <code>cache: npm</code> | Увімкнути кеш завантажень npm. |
| 41 | <code>- name: Install dependencies</code> | Назва наступного кроку в логах: Install dependencies. |
| 42 | <code>run: npm ci</code> | Установити залежності за lock-файлом. |
| 45 | <code>- name: Install Playwright browser</code> | Назва наступного кроку в логах: Install Playwright browser. |
| 46 | <code>run: npx playwright install --with-deps chromium</code> | Установити Chromium і залежності Linux. |
| 50 | <code>- name: Start PostgreSQL</code> | Назва наступного кроку в логах: Start PostgreSQL. |
| 51 | <code>run: docker compose up -d postgres</code> | Запустити сервіс postgres із compose.yaml у фоні. |
| 55 | <code>- name: Wait for PostgreSQL</code> | Назва наступного кроку в логах: Wait for PostgreSQL. |
| 56 | <code>run: &#124;</code> | Далі починається багаторядковий shell-сценарій. |
| 57 | <code>for i in {1..30}; do</code> | Цикл до 30 спроб; i — номер спроби. |
| 58 | <code>if docker compose ps postgres &#124; grep -q "healthy"; then</code> | Пошук healthy у статусі. Недолік: збігається також із unhealthy. |
| 59 | <code>echo "PostgreSQL is ready"</code> | Надрукувати повідомлення або значення PID у лог. |
| 60 | <code>exit 0</code> | Успішно завершити поточний крок. |
| 61 | <code>fi</code> | Завершити блок if. |
| 62 | <code>echo "Waiting for PostgreSQL..."</code> | Надрукувати повідомлення або значення PID у лог. |
| 63 | <code>sleep 2</code> | Пауза дві секунди. |
| 64 | <code>done</code> | Завершити тіло циклу. |
| 65 | <code>docker compose ps</code> | Надрукувати стан контейнерів для діагностики. |
| 66 | <code>exit 1</code> | Завершити крок помилкою. |
| 69 | <code>- name: Set up database</code> | Назва наступного кроку в логах: Set up database. |
| 70 | <code>run: npm run db:setup</code> | Запустити міграції та seed через root package.json. |
| 76 | <code>- name: Start backend and storefront, then wait until ready</code> | Назва наступного кроку в логах: Start backend and storefront, then wait until ready. |
| 77 | <code>run: &#124;</code> | Далі починається багаторядковий shell-сценарій. |
| 78 | <code>npm run dev --workspace=apps/backend &</code> | Запустити dev backend у фоні. |
| 79 | <code>BACKEND_PID=$!</code> | Зберегти PID останньої фонової команди. |
| 81 | <code>npm run dev --workspace=apps/storefront &</code> | Запустити dev storefront у фоні. |
| 82 | <code>STOREFRONT_PID=$!</code> | Зберегти PID останньої фонової команди. |
| 84 | <code>echo "Backend PID: $BACKEND_PID, Storefront PID: $STOREFRONT_PID"</code> | Надрукувати повідомлення або значення PID у лог. |
| 87 | <code>for i in {1..60}; do</code> | Цикл до 60 спроб готовності відповідного застосунку. |
| 88 | <code>if curl -f http://localhost:9000/health > /dev/null 2>&1; then</code> | Перевірити backend HTTP-запитом; приховати вивід. |
| 91 | <code>echo "Backend is ready"</code> | Надрукувати повідомлення або значення PID у лог. |
| 92 | <code>break</code> | Вийти з поточного циклу та продовжити shell-сценарій. |
| 93 | <code>fi</code> | Завершити блок if. |
| 94 | <code>echo "Waiting for backend..."</code> | Надрукувати повідомлення або значення PID у лог. |
| 95 | <code>sleep 2</code> | Пауза дві секунди. |
| 96 | <code>if [ "$i" -eq 60 ]; then</code> | Якщо це остання спроба, виконати блок помилки. |
| 97 | <code>echo "Backend did not become ready in time"</code> | Надрукувати повідомлення або значення PID у лог. |
| 98 | <code>exit 1</code> | Завершити крок помилкою. |
| 99 | <code>fi</code> | Завершити блок if. |
| 100 | <code>done</code> | Завершити тіло циклу. |
| 103 | <code>for i in {1..60}; do</code> | Цикл до 60 спроб готовності відповідного застосунку. |
| 104 | <code>if curl -f http://localhost:8000/de/store > /dev/null 2>&1; then</code> | Перевірити storefront HTTP-запитом; приховати вивід. |
| 105 | <code>echo "Storefront is ready"</code> | Надрукувати повідомлення або значення PID у лог. |
| 106 | <code>break</code> | Вийти з поточного циклу та продовжити shell-сценарій. |
| 107 | <code>fi</code> | Завершити блок if. |
| 108 | <code>echo "Waiting for storefront..."</code> | Надрукувати повідомлення або значення PID у лог. |
| 109 | <code>sleep 2</code> | Пауза дві секунди. |
| 110 | <code>if [ "$i" -eq 60 ]; then</code> | Якщо це остання спроба, виконати блок помилки. |
| 111 | <code>echo "Storefront did not become ready in time"</code> | Надрукувати повідомлення або значення PID у лог. |
| 112 | <code>exit 1</code> | Завершити крок помилкою. |
| 113 | <code>fi</code> | Завершити блок if. |
| 114 | <code>done</code> | Завершити тіло циклу. |
| 117 | <code>- name: Run Playwright tests</code> | Назва наступного кроку в логах: Run Playwright tests. |
| 118 | <code>run: npx playwright test</code> | Запустити тести за playwright.config.ts. |
| 122 | <code>- name: Upload Playwright report</code> | Назва наступного кроку в логах: Upload Playwright report. |
| 123 | <code>if: always()</code> | Запускати крок збереження й після попередньої помилки. |
| 124 | <code>uses: actions/upload-artifact@v4</code> | Завантажити готові файли результату. |
| 125 | <code>with:</code> | Параметри action цього кроку. |
| 126 | <code>name: playwright-report</code> | Назва артефакту всередині параметрів upload action. |
| 127 | <code>path: playwright-report/</code> | Папка з файлами для завантаження. |
| 128 | <code>retention-days: 7</code> | Зберігати артефакт сім днів у межах політик GitHub. |
