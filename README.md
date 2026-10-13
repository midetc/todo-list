# Todo list

A small Django site for tasks and tags. A task has text, a creation time, an optional deadline, a done flag, and any number of tags. A tag has a name and can belong to many tasks.

## Pages

- `/` shows tasks that are not done first, and newer tasks before older ones. Each task can be completed, undone, edited, or deleted.
- `/task/create/`, `/task/<id>/update/`, and `/task/<id>/delete/` manage tasks.
- `/tags/` lists tags. `/tags/create/`, `/tags/<id>/update/`, and `/tags/<id>/delete/` manage tags.

The sidebar with Home and Tags is on every page.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
```

Put a real `SECRET_KEY` in `.env`. `DEBUG=True` is for local development. `.env` stays on your machine and is not committed.

```powershell
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/.

## Tests

```powershell
python manage.py test
```
