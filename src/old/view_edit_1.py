import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time


@st.dialog("Delete Point")
def delete_point(point_id):
    """Delete a point from the DataFrame."""
    st.write(f"Deleting point #{point_id}...")
    if st.button("Confirm Deletion"):
        st.session_state.df = st.session_state.df.drop(point_id)
        st.session_state.df.reset_index(drop=True, inplace=True)
        st.toast(f"Point #{point_id} deleted successfully.")
        time.sleep(1)  # Simulate a delay for the deletion process
        st.rerun()



labels_display = st.sidebar.empty()
new_point = None

if st.session_state.df is not None:
    label_option = labels_display.radio(
        "🧷 Label à afficher:",
        ["Valeur du delay", "Index du point", "Aucun"],
    )
    
    if st.sidebar.checkbox("Edit the design"):
        point_id = st.sidebar.number_input("Point ID", min_value=0, max_value=len(st.session_state.df)-1, value=0)
        # get point coords
        point = st.session_state.df.loc[point_id]

        # delete point button
        if st.sidebar.button(":material/delete: Supprimer le point", use_container_width=True):
            # st.session_state.df = st.session_state.df.drop(point_id)
            # st.session_state.df.reset_index(drop=True, inplace=True)
            st.sidebar.success(f"Point #{point_id} sera supprimé.")
            delete_point(point_id)
        
        # Adding and editing a point

        with st.expander("Ajouter ou modifier le point", expanded=False):
            subtitle = st.empty()
            col1, col2, col3 = st.columns(3)
            with col1:
                new_x = st.slider("Nouvelle position X", value=float(point["x"]), max_value=10.0, min_value=-10.0)
            with col2:
                new_y = st.slider("Nouvelle position Y", value=float(point["y"]), max_value=10.0, min_value=-10.0)
            with col3:
                new_delay = st.number_input("Nouveau Delay", value=float(point["delay"]))
            add_point = st.checkbox("Ajouter un nouveau point")
            if add_point:
                subtitle.markdown("### ✏️ Ajouter un nouveau point")
                new_point = pd.DataFrame({
                    "x": [new_x],
                    "y": [new_y],
                    "text": "n",
                    "delay": [new_delay]
                })
            else:
                subtitle.markdown(f"### ✏️ Modifier le point #{point_id}")

            edit_submitted = st.button("Enregistrer les modifications")

        if edit_submitted:
            if add_point:
                # st.session_state.df = pd.concat([st.session_state.df, new_point], ignore_index=True)
                st.toast(f"Nouveau point ajouté: ({new_x}, {new_y}) avec un delay de {new_delay}.")
            else:
                st.session_state.df.at[point_id, "x"] = new_x
                st.session_state.df.at[point_id, "y"] = new_y
                st.session_state.df.at[point_id, "delay"] = new_delay
                st.toast(f"Point #{point_id} modifié avec succès.")

    else:
        # Download button
        file_name = st.sidebar.text_input("Nom du fichier CSV", value="grille_points.csv")
        st.sidebar.download_button(
            label="📥 Télécharger le fichier CSV",
            data=st.session_state.df.to_csv(index=False),
            file_name=file_name,
            mime="text/csv",
            use_container_width=True,
            # icon=":material/download:",
        )

    labels = None
    hover_data = {}
    if label_option == "Aucun":
        labels = None
        hover_data = {
            "#id": st.session_state.df.index,
        }
    elif label_option == "Index du point":
        labels = st.session_state.df.index
    elif label_option == "Valeur du delay":
        labels = st.session_state.df["delay"]
        hover_data = {
            "#id": st.session_state.df.index,
        }

    fig = px.scatter(
        st.session_state.df,
        x="x",
        y="y",
        text=labels,
        hover_data=hover_data
    )
    st.write(new_point)
    if new_point is not None:
        fig.add_trace(
            go.Scatter(
                x=new_point["x"],
                y=new_point["y"],
                text=new_point["text"],
                textfont=dict(color="black", size=12),
                textposition="top center"   
            ))
    
    fig.update_traces(
        marker=dict(color="blue", size=8, line=dict(width=1, color="black")),
        textposition="top center"
    )
    fig.update_xaxes(visible=False, showgrid=False, scaleanchor="y", scaleratio=1)
    fig.update_yaxes(visible=False, showgrid=False)
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Aucun point n'a été généré. Veuillez utiliser le générateur de points pour créer une grille.")
    st.write("Vous pouvez charger un fichier CSV contenant les points de la grille ou utiliser le générateur de points pour créer une grille personnalisée.")
    st.write("Utilisez le menu latéral pour naviguer vers les différentes fonctionnalités de l'application.")