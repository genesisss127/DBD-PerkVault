# DBD PerkVault — Part 1: Backend API

FastAPI + SQLAlchemy + SQLite backend for managing Dead by Daylight survivor perks. The Python files are kept directly in the project root.

## Database behavior

- `DBD.db` is the original uploaded database. The application opens it in read-only mode and never writes to it.
- On the first startup, the application imports the perk rows into `perkvault.db`.
- All API Create, Read, Update, and Delete operations use `perkvault.db`.
- Changes in `perkvault.db` persist after restarting the API.
- The original file has columns `Column1` (icon), `Column2` (name), `Column3` (description), and `Column4` (character). The first row contains headings and is skipped.

Keep `DBD.db` in the project root beside `requirements.txt`.

## Setup

From the project root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

From the project root:

```bash
uvicorn main:app --reload
```

Run the command from the project root (the folder containing `main.py`). Open the interactive API documentation at http://127.0.0.1:8000/docs.

## Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/perks/` | Create a perk |
| GET | `/perks/` | Retrieve all perks |
| GET | `/perks/{perk_id}` | Retrieve one perk |
| PUT | `/perks/{perk_id}` | Update a perk |
| DELETE | `/perks/{perk_id}` | Delete a perk |

## Notes

`PerkUpdate` uses PUT, so send all fields (`name`, `character`, `description`, and `icon`) when updating. The `icon` field can be `null`.

The working database `perkvault.db` is created automatically. Do not delete it if you want to keep your API changes.
