import streamlit as st
import pathlib, json
from src.blast_math import (
    linear_charge,
    hole_charge_mass,
    total_charge_mass,
    spacing,
    burden,
)

TEXT = st.session_state.text

# -----------------------------------------------------------
# Page
# -----------------------------------------------------------
st.title(TEXT["calc_title"])

with st.form("charge_calc"):
    c1, c2 = st.columns(2)

    hole_diameter_mm = c1.number_input(
        TEXT["hole_diameter"],
        value=st.session_state.get("hole_diameter", 51),
        step=1,
    )
    hole_depth_m = c1.number_input(
        TEXT["hole_depth"],
        value=st.session_state.get("hole_depth", 4.0),
        step=0.1,
    )
    explosive_density = c2.number_input(
        TEXT["explosive_density"],
        value=st.session_state.get("explosive_density", 1.15),
        step=0.01,
    )
    stemming_length_m = c1.number_input(
        TEXT["stemming_length"],
        value=0.51,
        step=0.01,
    )
    hole_count = c2.number_input(
        TEXT["number_of_holes"],
        value=62,
        step=1,
    )

    submitted = st.form_submit_button(TEXT["calculate"])

# update session state
if submitted:
    st.session_state.update(
        {
            "hole_diameter": hole_diameter_mm,
            "hole_depth": hole_depth_m,
            "explosive_density": explosive_density,
        }
    )

# -----------------------------------------------------------
# Results
# -----------------------------------------------------------
st.divider()

charge_len = hole_depth_m - stemming_length_m
lin = linear_charge(explosive_density, hole_diameter_mm)
per_hole = hole_charge_mass(lin, charge_len)
total = total_charge_mass(per_hole, hole_count)

bench = hole_depth_m  # placeholder
bur = burden(charge_len, lin, hole_depth_m)  # TODO: get the PF from the user
spc = spacing(bur)

col1, col2, col3 = st.columns(3)
col1.metric(TEXT["linear_charge"], f"{lin:.2f}")
col2.metric(TEXT["charge_per_hole"], f"{per_hole:.2f}")
col3.metric(TEXT["total_charge"], f"{total:.2f}")

st.divider()
st.subheader(TEXT["blast_pattern"])
st.write(TEXT["pattern_stub"])

col4, col5 = st.columns(2)
col4.metric(TEXT["burden"], f"{bur:.2f}")
col5.metric(TEXT["spacing"], f"{spc:.2f}")

# adding spacing and burden to session state
st.session_state.update(
    {
        "spacing": spc,
        "burden": bur,
    }
)
