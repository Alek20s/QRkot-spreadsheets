# QRKot — Charity Fund API

REST API для благотворительного фонда QRKot: приём пожертвований, распределение средств по проектам, формирование Excel-отчёта с выгрузкой на Яндекс.Диск.

## Стек технологий

- Python 3.12
- FastAPI
- SQLAlchemy (async) + SQLite
- Alembic (миграции)
- FastAPI Users (аутентификация)
- pandas + xlsxwriter (генерация отчётов)
- httpx (асинхронные запросы к API Яндекс.Диска)

## Возможности

- CRUD для благотворительных проектов (`/charity_project`)
- Приём пожертвований с автоматическим распределением по открытым проектам (`/donation`)
- Регистрация и аутентификация пользователей (JWT)
- Формирование Excel-отчёта по закрытым проектам, отсортированным по скорости сбора средств, с загрузкой на Яндекс.Диск и получением публичной ссылки (`/yandex`)

## Установка и запуск

1. Клонируйте репозиторий:
```
git clone https://github.com/Alek20s/QRkot-spreadsheets.git
cd QRkot-spreadsheets
```

2. Установите зависимости:
```
pip install -r requirements.txt
```

3. Создайте файл `.env` в корне проекта:
```
APP_SECRET=your-secret-key
APP_YANDEX_DISK_TOKEN=your-yandex-disk-oauth-token
```

4. Примените миграции:
```
alembic upgrade head
```

5. Запустите приложение:
```
uvicorn app.main:app --reload
```

6. Документация API доступна по адресу `http://127.0.0.1:8000/docs`.

## Переменные окружения

| Переменная | Описание |
|---|---|
| `APP_SECRET` | Секретный ключ для JWT-токенов |
| `APP_YANDEX_DISK_TOKEN` | OAuth-токен для доступа к API Яндекс.Диска |
| `APP_DATABASE_URL` | Строка подключения к БД (по умолчанию SQLite) |
| `APP_REPORT_FORMAT` | Формат даты для имени файла отчёта |

## Тестирование

```
python -m pytest
```

## Автор

Alek20s
