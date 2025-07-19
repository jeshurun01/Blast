
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import math

# st.header("📍 Générateur de Points")


with st.sidebar:
    st.subheader("📐 Paramètres de la Grille")
    nb_points_par_rangee = st.number_input("Nombre de points par rangée", min_value=1, value=7)
    nb_rangees = st.number_input("Nombre de rangées", min_value=1, value=6)
    espacement_points = st.number_input("Espacement entre les points (m)", min_value=0.1, value=1.0)
    espacement_rangees = st.number_input("Espacement entre les rangées (m)", min_value=0.1, value=1.1)
    angle_deg = st.slider("Orientation des rangées (°)", min_value=0, max_value=360, value=0)

theta = math.radians(angle_deg)
cos_theta, sin_theta = math.cos(theta), math.sin(theta)

points = []
for i in range(nb_rangees):
    for j in range(nb_points_par_rangee):
        x_base = j * espacement_points
        y_base = i * espacement_rangees
        x = x_base * cos_theta - y_base * sin_theta
        y = x_base * sin_theta + y_base * cos_theta
        points.append((x, y, 0.0))


st.markdown("### 🗺️ Aperçu de la grille générée")
st.caption("📄 Grille des Points (orientation = {}°)".format(angle_deg))
gen_button = st.empty()
msg = st.empty()
col1, col2 = st.columns([1, 2])
df = pd.DataFrame(points, columns=["x", "y", "delay"])
col1.subheader("Tableau des Points")
col1.dataframe(df)

fig = px.scatter(df, x="x", y="y", text=df.index)
fig.update_traces(
    marker=dict(color="blue", size=8, line=dict(width=1, color="black")),
    textposition="top center"
)
fig.update_xaxes(visible=False, showgrid=False, scaleanchor="y", scaleratio=1)
fig.update_yaxes(visible=False, showgrid=False)
fig.update_layout(height=600)
col2.plotly_chart(fig, use_container_width=True)

if gen_button.button(":material/frame_reload: Regénérer la grille"):
    st.session_state.df = df
    msg.success(f"Grille régénérée avec succès.")
