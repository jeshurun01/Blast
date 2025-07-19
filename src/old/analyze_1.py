import streamlit as st
import pandas as pd
import numpy as np
from pykrige.ok import OrdinaryKriging
import plotly.graph_objects as go


st.title("Analyse des Données")

with st.sidebar:
    with st.expander("ℹ️ Aide et informations", expanded=False):
        st.header("📊 Aide")
        st.markdown("""
        - **Format attendu** : CSV avec colonnes `x`, `y`, `delay`
        - **Exemple de données** :
        ```
        x,y,delay
        1.0,2.0,3.5
        2.0,3.0,4.5
        3.0,4.0,5.5
        ```
        - **Fonctionnalités** :
        - Estimation de valeur à un point donné
        - Visualisation de la carte interpolée
        """)
    
    # Model de variogramme
    var_model = st.selectbox(
        "Modèle de variogramme",
        options=["exponential", "spherical", "gaussian", "linear", "power"],
        index=0,
        help="Sélectionnez le modèle de variogramme à utiliser pour l'interpolation."
    )

    contour_colors = st.selectbox(
        "Couleurs des contours",
        options=["Viridis", "Cividis", "Plasma", "Magma", "Inferno", "Turbo", "Jet", "Blues", "Reds"],
        index=0,
        help="Sélectionnez la palette de couleurs pour les contours."
    )

    # === paramètres de configuration
    # contour_start = st.number_input("Début des contours", value=0.0, step=0.1)
    # contour_end = st.number_input("Fin des contours", value=7000.0, step=0.1)
    # contour_step = st.number_input("Pas des contours", value=50, step=25)

if st.session_state.df is not None:
    df = st.session_state.df

    if not {'x', 'y', 'delay'}.issubset(df.columns):
        st.error("❌ Le fichier doit contenir les colonnes : x, y, delay")
    else:
        if df["delay"].any() == 0.0:
            st.warning("Attention : la colonne `delay` ne contient que des **0.0**.", icon=":material/deployed_code_alert:")
            st.info("Modifiez les donnees pour continuer l'analyse.", icon=":material/lightbulb:")
            st.stop()

        # === Carte interpolée avec Plotly
        st.subheader("🗺️ Carte interpolée (interactive)")


        show_label = st.sidebar.checkbox("Afficher les valeurs des courbes", value=False, help="Afficher les étiquettes des niveaux sur la carte interpolée.")
        show_delay = st.sidebar.checkbox("Afficher les delays", value=False, help="Afficher les valeurs de delay sur la carte interpolée.")

        gridx = np.linspace(df["x"].min(), df["x"].max(), 100)
        gridy = np.linspace(df["y"].min(), df["y"].max(), 100)

        OK = OrdinaryKriging(
            df["x"], df["y"], df["delay"],
            variogram_model=var_model,
            verbose=False, enable_plotting=False
        )
        # z, ss = OK.execute('grid', gridx, gridy)
        z, ss = OK.execute("grid", gridx, gridy)
        zmin = np.nanmin(z)
        zmax = np.nanmax(z)

        # Tracer avec Plotly
        fig = go.Figure()

        # Les couleurs
        # custom_scale = [
        #     [0.0, "yellow"],
        #     [0.5, "green"],
        #     [1.0, "red"]
        # ]


        fig.add_trace(go.Contour(
            z=z,
            x=gridx,
            y=gridy,
            # contours=dict(start=contour_start, end=contour_end, size=contour_step),
            contours=dict(showlabels=show_label, labelfont=dict(size=12, color='white')),
            colorscale=contour_colors,
            line_smoothing=0.85
        ))

        # Points d'observation
        fig.add_trace(go.Scatter(
            x=df["x"], y=df["y"],
            mode="markers+text",
            marker=dict(color="red", size=8, line=dict(width=1, color="black")),
            name="Points mesurés",
            hovertemplate="x: %{x:.2f}<br>y: %{y:.2f}<br>valeur: %{text}",
            text=df["delay"] if show_delay else None,
            textfont=dict(color="black", size=12),
            textposition="top center"
        ))

        fig.update_layout(
            title="Carte interpolée par krigeage",
            xaxis_title="x",
            yaxis_title="y",
            height=600
        )
        fig.update_xaxes(visible=False, showgrid=False, scaleanchor="y", scaleratio=1)
        fig.update_yaxes(visible=False, showgrid=False)

        
        st.plotly_chart(fig, use_container_width=True)

        with st.expander(":material/bar_chart: Aperçu des données", expanded=False):
            col1, col2 = st.columns(2)

        # Dataframe
        col1.subheader("Datas")
        col1.dataframe(df.head(8))

        # === Valeurs statistiques
        col2.subheader("📊 Statistiques")
        col2.write(df.describe())

        # === Coordonnées à estimer
        with st.expander("📍 Point à estimer", expanded=False):
            x0 = st.number_input("x", value=float(df['x'].mean()))
            y0 = st.number_input("y", value=float(df['y'].mean()))

            if st.button("🔍 Estimer"):
                data = df[['x', 'y', 'delay']].to_numpy()
                OK = OrdinaryKriging(
                    data[:, 0], data[:, 1], data[:, 2],
                    variogram_model=var_model,
                    verbose=False, enable_plotting=False
                )
                z, ss = OK.execute('points', np.array([x0]), np.array([y0]))
                st.info(f"📈 Valeur estimée à ({x0:.2f}, {y0:.2f}) : **{z[0]:.3f}**")


else:
    st.warning("⚠️ Veuillez charger un fichier CSV contenant les colonnes `x`, `y`, `delay` pour commencer l'analyse.")
    st.info("📂 Utilisez le menu latéral pour charger un fichier CSV.")