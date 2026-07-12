# QA Automation Foundation (Python)

Тестовий фреймворк з нуля: API тести, E2E тести, unit тести, конфіг середовищ і CI.
Обґрунтування вибору стеку і стратегія тестування — у [`docs/STRATEGY.md`](./docs/STRATEGY.md).

Тестуємо два публічні сервіси:

- [dummyjson.com](https://dummyjson.com) — API (авторизація, список ресурсів, схема відповіді)
- [the-internet.herokuapp.com](https://the-internet.herokuapp.com) — E2E (логін, навігація, валідація форм)
- локальний Flask-фікстур-сервер (піднімається/гаситься автоматично) — для CRUD-chain тесту, де потрібна реальна персистентність

## Структура

```
config/
  environments/        # dev.env / staging.env / prod.env
  env.py                # завантажувач конфігурації (читає TEST_ENV)
tests/
  api/                  # API тести (requests + pydantic)
    schemas/            # pydantic-схеми відповідей
    fixtures/            # db.json + локальний Flask fixture_server.py
  e2e/                  # E2E тести (pytest-playwright + Page Object Model)
    pages/
  unit/                 # unit тести хелперів фреймворку (pytest)
src/utils/               # чисті функції, які юзаються і в тестах, і покриті unit-тестами
conftest.py               # спільні pytest-фікстури (config, локальний fixture-сервер)
docs/STRATEGY.md          # обґрунтування стеку + стратегія покриття
.github/workflows/        # CI pipeline
```

## Локальний запуск

Потрібен Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

HTML-звіт генерується через Allure, який окремо вимагає Java (JRE 8+) і сам Allure
CLI:

```bash
# CLI ставиться один раз, будь-яким зі способів:
npm install -g allure-commandline     # якщо є Node
# або: brew install allure            # macOS
# або: завантажити з https://github.com/allure-framework/allure2/releases
```

Запуск усього набору (unit + API + E2E):

```bash
pytest
```

Або окремо, за маркером:

```bash
pytest -m unit   # хелпери фреймворку
pytest -m api    # API тести (dummyjson.com + локальний Flask fixture-сервер)
pytest -m e2e    # E2E тести (the-internet.herokuapp.com, Chromium)
```

Allure-звіт — двокроково: спершу тести пишуть сирі результати, потім CLI збирає з них
HTML:

```bash
pytest --alluredir=allure-results
allure generate allure-results --clean -o allure-report
allure open allure-report   # піднімає локальний сервер і відкриває звіт у браузері
```

На відміну від `pytest-html`, звіт — не один файл, а папка зі статикою; `allure open`
або будь-який локальний http-сервер (`python -m http.server` з `allure-report/`)
потрібні, бо відкриття `index.html` напряму з диска (`file://`) в частини браузерів
блокує підвантаження даних звіту.

### Перемикання середовищ

Конфігурація читається з `config/environments/<TEST_ENV>.env` через змінну `TEST_ENV`
(`dev` за замовчуванням):

```bash
TEST_ENV=staging pytest -m api
TEST_ENV=prod pytest
```

Публічні демо-сервіси не мають окремих dev/staging/prod хостів, тому всі три файли
зараз вказують на одні й ті самі URL — сама механіка перемикання середовищ від цього
не змінюється, і на реальному проєкті кожен файл вказував би на свій хост і свої секрети.

## CI

`.github/workflows/tests.yml` запускається на `push` і `pull_request` у `main`:
ставить Python і брауз�