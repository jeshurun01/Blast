import streamlit as st

st.set_page_config(page_title="Explosive Charge Mass Calculator", page_icon=":bomb:")


st.title("Explosive Charge Mass Calculator")
st.write("This app calculates the mass of explosive charge required for mining operations using the formula:")
col1, col2 = st.columns([4, 2])

with col1:
    diameter = st.number_input("Enter the diameter of the hole (mm): ", step=1)
    explosive_density = st.number_input("Enter the explosive density: ")

    linear_charge = explosive_density * diameter**2 / 1273
    st.write(f"The mass of the explosive charge is: **:red[{linear_charge:.2f}] kg/m**")

    charge_length = st.number_input("Enter the charge length (m):")
    hole_charge_mass = linear_charge * charge_length
    st.write(f"Charge Mass per Hole: **:red[{hole_charge_mass:.2f}] kg**")

    number_of_holes = st.number_input("Enter the number of holes:", step=1)
    total_charge_mass = hole_charge_mass * number_of_holes
    st.write(f"Total Charge Mass: **:red[{total_charge_mass:.2f}] kg**")


with col2:
    st.latex(r"M_c = \frac{\rho  \times D^2}{1273}")

    st.markdown("<p style='text-align: center;'>Linear charge formula</p>", unsafe_allow_html=True)
    st.divider()

    st.write("Where:")
    st.write("M_c = Linear charge (kg/m³)")
    st.write("ρ = Explosive density (kg/m³)")
    st.write("D = Diameter of the circle (mm)")


# Dictionary

hole_details = {
    "Diameter": diameter,
    "Explosive Density": explosive_density,
    "Charge Length": charge_length,
    "Charge Mass": round(hole_charge_mass,2)
}

face_details = {
    "Number of Holes": number_of_holes,
    "Total Charge Mass": round(total_charge_mass,2),
    "Holes details": hole_details
}

# st.write(hole_details)
# st.write(face_details)

st.write("---")
st.write("Made by *Nasser K.* -- Whatsapp number: :green[+243 972 488 648]")