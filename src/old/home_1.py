import streamlit as st
import pandas as pd


st.title("Mini Mining engineering App")
st.write("This app is designed to assist with mining blast calculations and design.")

st.divider()
st.write("Vous pouvez charger un fichier CSV contenant les points de la grille ou utiliser le générateur de points pour créer une grille personnalisée.")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.write("Exemple de csv:")
    st.code("""
            x,y,delay
            0,0,0
            10,0,1
            20,0,2
            ...
        """, language="csv")

with col2:
    uploaded_file = st.file_uploader("📂 Charger un fichier CSV contenant les colonnes x, y, delay", type="csv")

    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        original_file_name = uploaded_file.name
        st.success(f"Fichier `{original_file_name}` chargé avec succès !")

st.write("Utilisez le menu latéral pour naviguer vers les différentes fonctionnalités de l'application.")