import streamlit as st
import papermill as pm
from datetime import date
from pathlib import Path
import pickle

RESULT_PATH = Path("final_result.pkl")

# -----------------------------
# Streamlit page config
# -----------------------------
st.set_page_config(
    page_title="Telegram OSINT Incident Mapping",
    layout="wide",
)

st.title("Telegram OSINT Incident Mapping")

# -----------------------------
# UI: Date selection
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Start date",
        value=date.today(),
    )

with col2:
    end_date = st.date_input(
        "End date",
        value=date.today(),
    )

run_button = st.button("Generate map")

# -----------------------------
# Main execution (only runs on click)
# -----------------------------
if run_button:
    if start_date > end_date:
        st.error("Start date must be before end date.")
        st.stop()

    with st.spinner("Running agentic analysis…"):
        # Ensure clean slate
        if RESULT_PATH.exists():
            RESULT_PATH.unlink()

        pm.execute_notebook(
            input_path="main.ipynb",
            output_path="executed.ipynb",
            parameters={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )

        if not RESULT_PATH.exists():
            st.error(
                "Notebook execution finished, but no result artifact was produced. "
                "Ensure `final_result.pkl` is written at the end of the notebook."
            )
            st.stop()

        with RESULT_PATH.open("rb") as f:
            st.session_state["final_result"] = pickle.load(f)

# -----------------------------
# Render output (persistent across reruns)
# -----------------------------
if "final_result" in st.session_state:
    final_result = st.session_state["final_result"]

    if not isinstance(final_result, dict):
        st.error("Unsupported result format returned by notebook.")
        st.stop()

    # ---- Render map from file ----
    st.divider()

    from streamlit.components.v1 import html

    map_html_path = final_result.get("map_html_path")

    if map_html_path and Path(map_html_path).exists():
        html(
            Path(map_html_path).read_text(encoding="utf-8"),
            height=650,
            scrolling=False,
        )


