import streamlit as st
import pandas as pd

TEXT = st.session_state.text


# -----------------------------------------------------------
# 2. Page
# -----------------------------------------------------------
# st.set_page_config(page_title=TEXT.get("page_title", "Mining Blast"), page_icon="💣")
st.title(TEXT["title"])
st.write(TEXT["intro"])
st.divider()

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.write(TEXT["csv_hint"])
    st.code(TEXT["csv_sample"], language="csv")

    # Download template
    template = pd.DataFrame({"x": [0, 10, 20], "y": [0, 0, 0], "delay": [0, 1, 2]})
    csv_bytes = template.to_csv(index=False).encode()
    st.download_button(
        label=TEXT["download_template"],
        data=csv_bytes,
        file_name="template.csv",
        mime="text/csv",
    )

with col2:
    uploaded = st.file_uploader(TEXT["upload_label"], type="csv")
    if uploaded:
        try:
            with st.spinner(TEXT["loading"]):
                df = pd.read_csv(uploaded)

            missing = {"x", "y", "delay"} - set(df.columns)
            if missing:
                st.error(TEXT["missing_cols"].format(cols=", ".join(missing)))
            else:
                # Optional: coerce to numeric
                df = df.apply(pd.to_numeric, errors="coerce")
                if df.isna().any().any():
                    st.warning(TEXT["nan_warning"])
                st.session_state.df = df
                st.success(TEXT["upload_success"].format(file=uploaded.name))
        except Exception as e:
            st.error(TEXT["upload_error"].format(err=e))

# -----------------------------------------------------------
# 3. Clear grid
# -----------------------------------------------------------
if st.button(TEXT["clear_grid"], use_container_width=True):
    st.session_state.df = None
    st.rerun()

st.info(TEXT["sidebar_note"], icon="ℹ️")