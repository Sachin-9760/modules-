# Module 16 — Streamlit Evaluation Console

## Assignment
Build a Streamlit evaluation console to compare model outputs and collect feedback.

## What this project demonstrates

- Rapid internal UI using Streamlit
- Prompt input
- Side-by-side model output comparison
- `st.session_state` for maintaining generated outputs
- Widgets such as buttons, radio buttons, sliders, text areas, and file upload
- CSV/TXT file upload and preview
- Reviewer feedback collection
- JSONL-based evaluation logs
- Pandas table for reviewing saved evaluations
- Simple operational metrics

## Project structure

```text
module 16/
├── app.py
├── requirements.txt
├── README.md
└── feedback.jsonl   # created automatically after feedback is saved
```

## Run on Windows 11

Open CMD or PowerShell inside this folder.

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate it

CMD:

```bash
venv\Scripts\activate
```

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Streamlit

```bash
streamlit run app.py
```

The browser will open the Streamlit application automatically.

## How to use

1. Enter a prompt.
2. Click **Generate Model Outputs**.
3. Review Model A and Model B side by side.
4. Select the preferred output.
5. Give a quality score from 1–5.
6. Add reviewer notes.
7. Click **Save Feedback**.
8. Review saved records in the Evaluation Logs table.
9. Optionally upload a `.csv` or `.txt` evaluation file.

## Important implementation note

The two model functions are intentionally demo functions:

```python
def demo_model_a(prompt):
    ...

def demo_model_b(prompt):
    ...
```

For a real project, these functions can be replaced with calls to the company's actual LLM/API. The Streamlit UI does not need to change significantly.

## Why Streamlit is used here

Streamlit is useful for internal evaluation tools because a working interface can be created directly in Python without building a separate frontend application.

This project intentionally keeps the frontend simple instead of forcing a complex React-style architecture into Streamlit.
