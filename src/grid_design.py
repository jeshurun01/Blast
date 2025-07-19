import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import math
from pathlib import Path

# ------------------------------------------------------------------
# 1. Language already injected in main.py
# ------------------------------------------------------------------
TEXT = st.session_state.text

# ------------------------------------------------------------------
# 2. Defaults from session_state or sensible fall-backs
# ------------------------------------------------------------------
defaults = {
    "points_per_row": 6,
    "row_count": 6,
    "point_spacing": st.session_state.get("spacing", 1.0),      # m
    "row_spacing": st.session_state.get("burden", 1.1),         # m
    "rotation": 0,                                              # deg
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# ------------------------------------------------------------------
# 3. Sidebar controls
# ------------------------------------------------------------------
with st.sidebar:
    st.subheader(TEXT["grid_params"])

    points_per_row = st.number_input(
        TEXT["points_per_row"],
        min_value=1,
        value=st.session_state.points_per_row,
        step=1,
    )
    row_count = st.number_input(
        TEXT["row_count"],
        min_value=1,
        value=st.session_state.row_count,
        step=1,
    )
    point_spacing = st.number_input(
        TEXT["point_spacing"],
        min_value=0.1,
        value=st.session_state.point_spacing,
        step=0.1,
        format="%.2f",
    )
    row_spacing = st.number_input(
        TEXT["row_spacing"],
        min_value=0.1,
        value=st.session_state.row_spacing,
        step=0.1,
        format="%.2f",
    )
    rotation = st.slider(
        TEXT["rotation"],
        min_value=0,
        max_value=360,
        value=st.session_state.rotation,
    )

# Persist sidebar choices
st.session_state.update(
    {
        "points_per_row": points_per_row,
        "row_count": row_count,
        "point_spacing": point_spacing,
        "row_spacing": row_spacing,
        "rotation": rotation,
    }
)

# ------------------------------------------------------------------
# 4. Geometry generation
# ------------------------------------------------------------------
theta = math.radians(rotation)
cos_t, sin_t = math.cos(theta), math.sin(theta)

coords = []
for i in range(row_count):
    for j in range(points_per_row):
        x0 = j * point_spacing
        y0 = i * row_spacing
        x = x0 * cos_t - y0 * sin_t
        y = x0 * sin_t + y0 * cos_t
        coords.append((x, y, 0.0))

df = pd.DataFrame(coords, columns=["x", "y", "delay"])

# ------------------------------------------------------------------
# 5. Layout
# ------------------------------------------------------------------
st.markdown(f"### {TEXT['preview_title']}")
st.caption(TEXT["orientation_caption"].format(angle=rotation))

col_table, col_plot = st.columns([1, 2])

with col_table:
    st.subheader(TEXT["points_table"])
    st.dataframe(df, use_container_width=True)

    if st.button(TEXT["save_grid"], use_container_width=True):
        st.session_state.df = df
        st.success(TEXT["saved_ok"])

with col_plot:
    fig = px.scatter(df, x="x", y="y", text=df.index)
    fig.update_traces(
        marker=dict(color="royalblue", size=10, line=dict(width=1, color="black")),
        textposition="top center",
    )
    fig.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(scaleanchor="y", scaleratio=1, visible=False),
        yaxis=dict(visible=False),
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------
# 6. Clear button
# ------------------------------------------------------------------
if st.button(TEXT["clear_grid"], use_container_width=True):
    st.session_state.df = None
    st.rerun()