import streamlit as st


charge_calculator = st.Page("charge_calculator.py", title="Explosive Charge Mass Calculator", icon=":material/add_circle:")
ug_design = st.Page("ug_design.py", title="Design a UG Stope", icon=":material/dataset:")

pg = st.navigation([charge_calculator, ug_design])
st.set_page_config(page_title="Mining Blast", page_icon=":bomb:")

pg.run()
