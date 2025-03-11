import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


def cords_generator(x_start, y_start, spacing, burden):
    x = x_start
    y = y_start
    while True:
        yield x, y
        x += spacing
        if x > width:
            x = x_start
            y += burden
        if y > height:
            break


def draw_graph(stope_cords: list):
    fig, ax = plt.subplots()

    for cord in stope_cords:
        circle = plt.Circle(cord, hole_diameter, color=stope_color, fill=True)
        ax.add_patch(circle)

    # Masquer les axes
    ax.set_xticks([])  # Masquer les ticks de l'axe X
    ax.set_yticks([])  # Masquer les ticks de l'axe Y

    ax.set_xlim(0 , stope_cords[-1][0] + side_stand_off)
    ax.set_ylim(0, stope_cords[-1][1] + top_stand_off)

    plt.gca().set_aspect('equal', adjustable='box')

    return fig, ax


def draw_cut(cut_cords: list):
    cut_fig, cut_ax = plt.subplots()
    for cut_cord in cut_cords:
        circle = plt.Circle(cut_cord, hole_diameter, color=cut_color, fill=True)
        cut_ax.add_patch(circle)

        plt.gca().set_aspect('equal', adjustable='box')

    # Masquer les axes
    cut_ax.set_xticks([])  # Masquer les ticks de l'axe X
    cut_ax.set_yticks([])  # Masquer les ticks de l'axe Y

    cut_ax.set_xlim(-2 , 2)
    cut_ax.set_ylim(-2, 2)

    return cut_fig

def add_cut(cut_cord, ax):
    for cut_cord in cut_cords:
        circle = plt.Circle((cut_cord[0] + x_move, cut_cord[1] + y_move), hole_diameter, color=cut_color, fill=True)
        ax.add_patch(circle)



# Sidebar
with st.sidebar:
    st.title("Design your stope")
    diameter = st.number_input("Hole Diameter", 32, 300, 51)
    spacing = st.number_input("Spacing", 0.5, 10.0, 1.1)
    burden = st.number_input("Burden", 0.5, 10.0, 1.0)
    # Cut holes
    is_cut = st.checkbox("Cut Holes")
    a = 0.250
    b = 0.300
    cut_cords = [(0, 0), (0, a), (a, 0), (0, -a), (-a, 0), (a, a), (-a, -a), (a, -a), (-a, a), (0, a + b), (0, -a - b), (a + b, 0), (-a - b, 0)]

    with st.expander("Tweak cut position"):
        if is_cut:
            x_move = st.slider("Cut horizontal move", 0.0, 8.0, 2.95)
            y_move = st.slider("Cut Vertical move", 0.0, 8.0, 1.8)

    st.divider()

    with st.expander("Stope Dimensions"):
        width = st.slider("Gallery Width", 0, 10, 7)
        height = st.slider("Gallery Height", 0, 10, 6)
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        stope_color = st.color_picker("Stope Color", "#FF0000")
    with col2:
        cut_color = st.color_picker("Cut color", "#00FF00")

    st.divider()
    with st.expander("Stand-Offs"):
        bottom_stand_off = st.slider("Bottom Stand-Off", 0.0, 0.5, 0.3)
        top_stand_off = st.slider("Top Stand-Off", 0.0, 0.5, 0.2)
        side_stand_off = st.slider("Side Stand-Off", 0.0, 0.5, 0.2)



hole_diameter = diameter / 1000
spacing = spacing
burden = burden
x_start = side_stand_off
y_start = bottom_stand_off

cords = list(cords_generator(x_start, y_start, spacing, burden))


df = pd.DataFrame(cords, columns=["x", "y"])
if is_cut:
    df = pd.concat([df, pd.DataFrame(cut_cords, columns=["x", "y"])], ignore_index=True)

design, data, cut = st.tabs(["Stope Design", "Stope Data", "Cut design"])

with design:
    fig, ax = draw_graph(cords)
    if is_cut:
        add_cut(cut_cords, ax)
    st.pyplot(fig)
with data:
    # Number of holes
    total_number_holes = df["x"].count()
    st.write(f"Number of Hole: {total_number_holes}")
    st.divider()
    st.dataframe(df)
with cut:
    if is_cut:
        st.text("Here is the cut")
        cut_fig = draw_cut(cut_cords)
        st.pyplot(cut_fig)
    else:
        st.text("Building in progress")
        st.info("Please check the Cut Holes checkbox in the sidebar to see the cut design")

