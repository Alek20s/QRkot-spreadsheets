# QRKot --- Charity Fund API

A REST API for the QRKot charity fund that accepts donations,
automatically allocates funds to charity projects, and generates Excel
reports uploaded to Yandex.Disk.

## Technology Stack

-   Python 3.12
-   FastAPI
-   SQLAlchemy (Async) + SQLite
-   Alembic (database migrations)
-   FastAPI Users (authentication)
-   pandas + xlsxwriter (Excel report generation)
-   httpx (asynchronous requests to the Yandex.Disk API)

## Features

-   CRUD operations for charity projects (`/charity_project`)
-   Donation management with automatic allocation of funds to open
    charity projects (`/donation`)
-   User registration and JWT-based authentication
-   Generation of Excel reports for completed charity projects, sorted
    by fundraising completion time, with automatic upload to Yandex.Disk
    and a public download link (`/yandex`)

## Installation and Setup

Clone the repository:

``` bash
git clone https://github.com/Alek20s/QRkot-spreadsheets.git
cd QRkot-spreadsheets
```

Install the dependencies:

``` bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

``` env
APP_SECRET=your-secret-key
APP_YANDEX_DISK_TOKEN=your-yandex-disk-oauth-token
```

Apply the database migrations:

``` bash
alembic upgrade head
```

Start the application:

``` bash
uvicorn app.main:app --reload
```

The API documentation will be available at:

`http://127.0.0.1:8000/docs`

## Environment Variables

  -----------------------------------------------------------------------
  Variable                       Description
  ------------------------------ ----------------------------------------
  `APP_SECRET`                   Secret key used for JWT token generation

  `APP_YANDEX_DISK_TOKEN`        OAuth token for accessing the
                                 Yandex.Disk API

  `APP_DATABASE_URL`             Database connection string (SQLite by
                                 default)

  `APP_REPORT_FORMAT`            Date format used in generated report
                                 filenames
  -----------------------------------------------------------------------

## Running Tests

``` bash
python -m pytest
```

## Author

**Alek20s**
