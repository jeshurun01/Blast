import streamlit as st
import pandas as pd
import numpy as np
from pykrige.ok import OrdinaryKriging
import plotly.express as px
import plotly.graph_objects as go
from src.blast_report import delay_continuity, gap_overlap_map, symmetry_score
from src.blast_gif import create_timing_gif


TEXT = st.session_state.text

st.title(TEXT["analysis_title"])

# ------------------------------------------------------------------
# Guard
# ------------------------------------------------------------------
if st.session_state.df is None or st.session_state.df.empty:
    st.warning(TEXT["no_data"])
    st.stop()

df = st.session_state.df
required = {"x", "y", "delay"}
if not required.issubset(df.columns):
    st.error(TEXT["bad_cols"])
    st.stop()

if df["delay"].any() == 0.0:
    st.warning("Attention : la colonne `delay` ne contient que des **0.0**.", icon=":material/deployed_code_alert:")
    st.info("Modifiez les donnees pour continuer l'analyse.", icon=":material/lightbulb:")
    st.stop()

# ------------------------------------------------------------------
# Sidebar controls
# ------------------------------------------------------------------
with st.sidebar:
    st.subheader(TEXT["settings"])
    var_model = st.selectbox(
        TEXT["variogram_model"],
        ["exponential", "spherical", "gaussian", "linear", "power"],
        index=0,
    )
    color_scale = st.selectbox(TEXT["color_scale"], px.colors.named_colorscales(), index=0)
    spacing = st.number_input("Spacing (m)", value=st.session_state.get("spacing", 1.0), step=0.1)
    burden = st.number_input("Burden (m)", value=st.session_state.get("burden", 1.0), step=0.1)

# ------------------------------------------------------------------
# 1. Technical Report Card
# ------------------------------------------------------------------
cont = delay_continuity(df)
gaps = gap_overlap_map(df.copy(), spacing, burden)
sym = symmetry_score(df)

col1, col2, col3 = st.columns(3)
col1.metric("Delay Continuity", "✅ PASS" if cont["ok"] else "❌ FAIL")
col2.metric("Min Gap Ratio", f"{gaps['gap_ratio'].min():.2f}")
col3.metric("Symmetry Score", f"{sym:.2%}")

# ------------------------------------------------------------------
# 2. Kriging Map (unchanged logic, shorter layout)
# ------------------------------------------------------------------
gridx = np.linspace(df["x"].min(), df["x"].max(), 100)
gridy = np.linspace(df["y"].min(), df["y"].max(), 100)

ok = OrdinaryKriging(df["x"], df["y"], df["delay"], variogram_model=var_model)
z, _ = ok.execute("grid", gridx, gridy)

fig = go.Figure()
fig.add_trace(
    go.Contour(
        z=z,
        x=gridx,
        y=gridy,
        colorscale=color_scale,
        contours=dict(showlabels=True),
    )
)
fig.add_trace(
    go.Scatter(
        x=df["x"],
        y=df["y"],
        mode="markers+text",
        marker=dict(color="red", size=8),
        text=df["delay"].round(1),
        textposition="top center",
        name=TEXT["holes"],
    )
)
fig.update_xaxes(visible=False, showgrid=False, scaleanchor="y", scaleratio=1)
fig.update_yaxes(visible=False, showgrid=False)

fig.update_layout(height=600, margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------
# 3. Gap / Overlap Table
# ------------------------------------------------------------------
with st.expander(TEXT["gap_table"], expanded=False):
    st.dataframe(gaps[["x", "y", "min_dist", "gap_ratio"]])

# ------------------------------------------------------------------
# 4. Export PDF Summary (optional)
# ------------------------------------------------------------------
if st.button(TEXT["export_pdf"]):
    pdf = (
        f"Blast Design Report\n"
        f"Delay Continuity: {'PASS' if cont['ok'] else 'FAIL'}\n"
        f"Min Gap Ratio: {gaps['gap_ratio'].min():.2f}\n"
        f"Symmetry Score: {sym:.2%}"
    )
    st.download_button(label="📥 Download PDF", data=pdf, file_name="blast_report.txt")

    # ------------------------------------------------------------------
    # Blast-timing GIF
    # ------------------------------------------------------------------
gif_bytes = create_timing_gif(df)
st.download_button(
    label="📥 Download GIF",
    data=gif_bytes,
    file_name="blast_timing.gif",
    mime="image/gif",
)