import streamlit as st


st.title("Explosive Charge Mass Calculator")

with st.form("charge_calculator_form"):
    in_col1, in_col2 = st.columns(2)

    hole_diameter = in_col1.number_input("Hole diameter (mm): ", value=st.session_state.get("hole_diameter", 51), step=1)
    hole_depth = in_col1.number_input("Hole depth (m): ", value=st.session_state.get("hole_depth", 4.0), step=0.1)
    explosive_density = in_col2.number_input("Explosive density: ", value=st.session_state.get("explosive_density", 1.15), step=0.01)

    stemming_length = in_col1.number_input("Stemming length (m): ", value=0.51, step=0.01)
    charge_length = hole_depth - stemming_length

    number_of_holes = in_col2.number_input("Number of holes:", value=62, step=1)

    submitted = st.form_submit_button("Calculate")

if submitted:
    st.session_state.hole_diameter = hole_diameter
    st.session_state.hole_depth = hole_depth
    st.session_state.explosive_density = explosive_density
else:
    # Use previous values or defaults if not submitted yet
    hole_diameter = st.session_state.get("hole_diameter", 51)
    hole_depth = st.session_state.get("hole_depth", 4.0)
    explosive_density = st.session_state.get("explosive_density", 1.15)
    charge_length = hole_depth - stemming_length
    number_of_holes = number_of_holes

st.divider()
linear_charge = st.session_state.explosive_density * st.session_state.hole_diameter**2 / 1273
hole_charge_mass = linear_charge * charge_length
total_charge_mass = hole_charge_mass * number_of_holes

## Calculations


out_col1, out_col2, out_col3 = st.columns(3)
out_col1.metric("Linear Charge (kg/m)", f"{linear_charge:.2f}")
out_col2.metric("Charge Mass per Hole (kg)", f"{hole_charge_mass:.2f}")
out_col3.metric("Total Charge Mass (kg)", f"{total_charge_mass:.2f}")

