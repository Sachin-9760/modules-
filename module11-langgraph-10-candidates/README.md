# Module 11 - LangGraph 10 Candidate Demo

This version processes 10 sample candidates and stores each final human decision in SQLite.

## Run

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

For every candidate scoring 70 or above, enter `yes` or `no` at the human review checkpoint.

After all 10 candidates:

```cmd
python -m app.history
```

This displays candidate ID, name, score, YES/NO review, final decision, and status.

The database file `candidate_history.db` is created automatically in the project root.
