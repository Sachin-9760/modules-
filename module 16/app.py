import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

st.set_page_config(
    page_title="Module 16 - Streamlit Evaluation Console",
    page_icon="🧪",
    layout="wide"
)

FEEDBACK_FILE = "feedback.jsonl"

st.title("🧪 Model Evaluation Console")
st.caption("Module 16 — Streamlit for internal review and operations tools")

if "model_a_output" not in st.session_state:
    st.session_state.model_a_output = ""
if "model_b_output" not in st.session_state:
    st.session_state.model_b_output = ""
if "generated" not in st.session_state:
    st.session_state.generated = False

def demo_model_a(prompt):
    return (
        f"Model A response to: {prompt}\n\n"
        "This is a concise demonstration response. "
        "It focuses on the main answer and keeps the explanation short."
    )

def demo_model_b(prompt):
    return (
        f"Model B response to: {prompt}\n\n"
        "This is a detailed demonstration response. "
        "It adds context, examples, and a clearer step-by-step explanation."
    )

def save_feedback(record):
    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

st.sidebar.header("Evaluation Settings")
reviewer = st.sidebar.text_input("Reviewer name", value="Internal Reviewer")
model_a_name = st.sidebar.text_input("Model A", value="Model A")
model_b_name = st.sidebar.text_input("Model B", value="Model B")

uploaded = st.sidebar.file_uploader(
    "Upload evaluation prompts (.txt or .csv)",
    type=["txt", "csv"]
)

if uploaded:
    st.sidebar.success(f"Uploaded: {uploaded.name}")

st.subheader("1. Enter an evaluation prompt")
prompt = st.text_area(
    "Prompt",
    placeholder="Example: Explain why session state is useful in Streamlit.",
    height=120
)

col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Model Outputs", type="primary", use_container_width=True):
        if not prompt.strip():
            st.warning("Please enter a prompt first.")
        else:
            st.session_state.model_a_output = demo_model_a(prompt)
            st.session_state.model_b_output = demo_model_b(prompt)
            st.session_state.generated = True
            st.session_state.generated_at = datetime.now().isoformat(timespec="seconds")

if st.session_state.generated:
    st.divider()
    st.subheader("2. Compare outputs")

    out1, out2 = st.columns(2)

    with out1:
        st.markdown(f"### {model_a_name}")
        st.text_area(
            "Model A output",
            value=st.session_state.model_a_output,
            height=260,
            key="output_a_display"
        )

    with out2:
        st.markdown(f"### {model_b_name}")
        st.text_area(
            "Model B output",
            value=st.session_state.model_b_output,
            height=260,
            key="output_b_display"
        )

    st.subheader("3. Collect reviewer feedback")

    rating = st.radio(
        "Which output is preferred?",
        [model_a_name, model_b_name, "Tie / Both similar"],
        horizontal=True
    )

    quality = st.slider("Overall quality", 1, 5, 3)
    notes = st.text_area(
        "Reviewer notes",
        placeholder="Explain why you selected this output...",
        height=100
    )

    if st.button("Save Feedback", use_container_width=True):
        record = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "reviewer": reviewer,
            "prompt": prompt,
            "model_a": model_a_name,
            "model_b": model_b_name,
            "preferred": rating,
            "quality": quality,
            "notes": notes
        }
        save_feedback(record)
        st.success("Feedback saved successfully.")

st.divider()
st.subheader("4. Evaluation Logs")

if os.path.exists(FEEDBACK_FILE):
    records = []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    if records:
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True, hide_index=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Reviews", len(df))
        with c2:
            st.metric("Average Quality", round(df["quality"].mean(), 2))
        with c3:
            st.metric("Model A Preferred", int((df["preferred"] == model_a_name).sum()))
    else:
        st.info("No feedback has been recorded yet.")
else:
    st.info("No evaluation logs yet. Generate outputs and save feedback to create logs.")

st.divider()
st.subheader("5. Uploaded File Preview")

if uploaded:
    try:
        if uploaded.name.lower().endswith(".csv"):
            data = pd.read_csv(uploaded)
            st.dataframe(data, use_container_width=True)
        else:
            content = uploaded.read().decode("utf-8")
            st.text_area("File contents", content, height=180)
    except Exception as e:
        st.error(f"Could not read the uploaded file: {e}")

st.caption("Internal evaluation demo — replace the demo model functions with your real model/API calls when needed.")
