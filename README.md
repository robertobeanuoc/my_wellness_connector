# whellness_conector
My whellness connector

# my_wellness_connector

Small utility to sync MyWellness workout sessions into a MySQL database.

## Quick overview
- Scrapes MyWellness using credentials and saves sessions into a MySQL database.
- Two supported run modes: local (virtualenv) and Docker (compose).

## Prerequisites
- Python 3.11+ (for local venv)
- Docker & Docker Compose (for container runs)

## Local development (virtual environment)
1. Create and activate a virtual environment in the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install --upgrade pip setuptools wheel
pip install -r src/requirements.txt
```

3. Run the app (reads env vars from your shell or a local `.env` file):

```bash
# from project root
python src/main.py
```

4. Run tests:

```bash
source .venv/bin/activate
pip install -r src/requirements.txt
pip install pytest
pytest -q
```

## Docker (recommended for reproducible runs)
1. Copy the example env file and edit it with real credentials:

```bash
cp .env.example .env
# edit .env and fill in values
```

2. Start the application and a MySQL service with Docker Compose:

```bash
docker compose up --build
```

The compose setup starts the application container. The app expects an existing MySQL
instance reachable at `DB_HOST` (set that in your `.env`).

- `app`: the Python app built from `docker/Dockerfile`.

## Required environment variables
Fill these in `.env` (see `.env.example` for sample values):

- `DB_NAME` — MySQL database name used by the app and DB container.
- `DB_USERNAME` — DB user for the app.
-- `DB_PASSWORD` — DB user's password.
-- `DB_TZ_DATES` — (optional) timezone for DB datetime conversion (default `UTC`).
- `MYWELLNESS_USERNAME` — MyWellness login username (required).
- `MYWELLNESS_PASSWORD` — MyWellness login password (required).
- `DAYS_BACK` / `START_DATE` / `END_DATE` — optional run controls used by `main.py`.

## Notes
- The project expects sources under `src/` and the package `my_wellness_connector` lives there.
- `.venv` and `.env` are ignored by git by default; see [`.gitignore`](.gitignore#L1).

## Files added/updated
- [docker-compose.yml](docker-compose.yml#L1) — compose configuration for `app` and `db`.
- [.env.example](.env.example#L1) — example environment variables to copy to `.env`.

If you want, I can populate a `.env` with placeholder values, run the compose stack, or run the test suite locally.



# Update alembic model 

1. Load enviroment variables `source local_env.sh`
2. Generate auto upgrade `alembic revision --autogenerat-m "Initial migration"`
3. Sync database `alembic upgrade head`