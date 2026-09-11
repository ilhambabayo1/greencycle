#  GreenCycle — FastAPI Web App

A recycle-item tracker built with **FastAPI + Jinja2 + SQLAlchemy**, fully containerized and ready to deploy on **Railway with Docker**.

## Project structure

```
greencycle-app/
├── Dockerfile
├── railway.json
├── requirements.txt
├── .dockerignore
└── app/
    ├── main.py              # FastAPI app entry point
    ├── config.py            # Settings / env vars
    ├── database.py          # SQLAlchemy engine & session
    ├── models.py            # ORM model (RecycleItem)
    ├── schemas.py           # Pydantic schemas
    ├── crud.py              # DB operations + points logic
    ├── routers/
    │   ├── pages.py         # HTML UI routes (Jinja2)
    │   └── items.py         # JSON REST API (/api/items)
    ├── templates/
    │   ├── base.html        # Layout with navbar/footer
    │   ├── index.html       # Home: stats, add form, item table
    │   └── about.html       # About page
    └── static/
        ├── css/style.css    # Green theme styling
        └── js/main.js       # Toasts + delete confirm
```

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# open http://127.0.0.1:8000
```

## Run with Docker

```bash
docker build -t greencycle .
docker run -p 8000:8000 greencycle
```

## Deploy on Railway

1. Push this folder to a GitHub repo.
2. In Railway: **New Project → Deploy from GitHub repo**.
3. Railway auto-detects the `Dockerfile` (also declared in `railway.json`) and starts the app with the provided `$PORT`.
4. Generate a public domain in the service's **Settings → Networking** tab.

## API

| Method | Route                | Description                    |
|--------|----------------------|--------------------------------|
| GET    | `/`                  | Home UI (stats + item table)   |
| GET    | `/about`             | About page                     |
| GET    | `/api/items`         | List items (optional `?category=`) |
| GET    | `/api/items/stats`   | Aggregate stats                |
| POST   | `/api/items`         | Create item (JSON)             |
| DELETE | `/api/items/{id}`    | Delete item                    |

Interactive API docs: `/docs`
