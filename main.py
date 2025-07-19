import streamlit as st
from src.config import DEFAULT_HOLE_DIAMETER, DEFAULT_EXPLOSIVE_DENSITY, DEFAULT_HOLE_DEPTH

import json, pathlib, io


# Initialize the Streamlit app
st.set_page_config(page_title="Mining Blast", page_icon=":bomb:")

# -----------------------------------------------------------
# 1. i18n helper – JSON
# -----------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_lang(lang: str) -> dict:
    path = pathlib.Path(__file__).parent / "locales" / f"{lang}.json"
    if not path.exists():
        st.error(f"Language file '{lang}.json' missing.")
        st.stop()
    return json.loads(path.read_text(encoding="utf-8"))

# default language
st.session_state.setdefault("lang", "en")

with st.sidebar:
    st.subheader("🌐 Langue")
    new_lang = st.radio(
        "Choisir la langue",
        options=["English", "Français"],
        index=0 if st.session_state.lang == "en" else 1,
        horizontal=True,
    )
    new_code = "en" if new_lang == "English" else "fr"
    if new_code != st.session_state.lang:
        st.session_state.lang = new_code
        st.session_state.text = load_lang(new_code)
        st.rerun()


def init_session_state():
    defaults = {
        "hole_diameter": DEFAULT_HOLE_DIAMETER,
        "explosive_density": DEFAULT_EXPLOSIVE_DENSITY,
        "hole_depth": DEFAULT_HOLE_DEPTH,
        "df": None,
        "text": load_lang(st.session_state.lang)
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

## Session state to store data
if 'hole_diameter' not in st.session_state:
    init_session_state()

TEXT = st.session_state.text

pages_list = [
    st.Page("src/home.py", title="Home", icon=":material/home:"),
    st.Page("src/charge_calculator.py", title="Charge Calculator", icon=":material/add_circle:"),
    st.Page("src/grid_design.py", title="Grid Design", icon=":material/dataset:"),
    st.Page("src/view_edit.py", title="View/Edit", icon=":material/edit:"),
    st.Page("src/analyze.py", title="Analyze", icon=":material/analytics:"),
    st.Page("src/doc.py", title="Documentation", icon=":material/help_center:"),
]

app = st.navigation(pages_list, position="top")

if __name__ == "__main__":
    app.run()
else:
    st.write("This app is designed to assist with mining blast calculations and design.")
    st.write("Please run this app in a Streamlit environment to access the full functionality.")
