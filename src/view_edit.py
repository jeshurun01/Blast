import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from collections import deque


TEXT = st.session_state.text  # injected in main.py

# ------------------------------------------------------------------
# 1. Undo / Redo helpers
# ------------------------------------------------------------------
MAX_HISTORY = 30


def push_state(df: pd.DataFrame):
    """Save current dataframe to history."""
    if st.session_state.df is not None:
        st.session_state.history.append(df.copy())


def undo():
    if len(st.session_state.history) > 1:
        st.session_state.redo_stack.append(st.session_state.history.pop())
        st.session_state.df = st.session_state.history[-1].copy()
        st.toast("Undo last action")
        st.rerun()


def redo():
    if st.session_state.redo_stack:
        st.session_state.df = st.session_state.redo_stack.pop()
        st.session_state.history.append(st.session_state.df.copy())
        st.toast("Redo last action")
        st.rerun()


# Initialise once
if "history" not in st.session_state:
    st.session_state.history = deque(maxlen=MAX_HISTORY)
    st.session_state.redo_stack = deque(maxlen=MAX_HISTORY)
    push_state(st.session_state.df)   # seed


# ------------------------------------------------------------------
# Validation helpers
# ------------------------------------------------------------------
MIN_SEPARATION_M = 0.5
UNIQUE_DELAY = False

def validate_new(x: float, y: float, delay: float, df: pd.DataFrame) -> str | None:
    """Return error string if invalid, else None."""
    dist = ((df["x"] - x) ** 2 + (df["y"] - y) ** 2) ** 0.5
    if dist.min() < MIN_SEPARATION_M:
        return f"Too close to existing hole (min {MIN_SEPARATION_M} m)."
    if UNIQUE_DELAY and delay in df["delay"].values:
        return "Delay must be unique."
    return None


# ------------------------------------------------------------------
# Dialog: delete a point
# ------------------------------------------------------------------
@st.dialog(TEXT["dlg_delete_title"])
def delete_point(point_id: int):
    st.write(TEXT["dlg_delete_msg"].format(id=point_id))
    if st.button(TEXT["dlg_delete_confirm"], type="primary"):
        push_state(st.session_state.df)
        st.session_state.df = st.session_state.df.drop(point_id)
        st.session_state.df.reset_index(drop=True, inplace=True)
        st.toast(TEXT["toast_deleted"].format(id=point_id))
        time.sleep(0.6)
        st.rerun()


# ------------------------------------------------------------------
# Sidebar undo / redo
# ------------------------------------------------------------------
with st.sidebar:
    st.subheader("History")
    col_undo, col_redo = st.columns(2)
    col_undo.button("↶ Undo", on_click=undo, disabled=len(st.session_state.history) <= 1)
    col_redo.button("↷ Redo", on_click=redo, disabled=len(st.session_state.redo_stack) == 0)

# ------------------------------------------------------------------
# Guard clause
# ------------------------------------------------------------------
if st.session_state.df is None or st.session_state.df.empty:
    st.warning(TEXT["no_points"])
    st.info(TEXT["use_generator"])
    st.stop()

# ------------------------------------------------------------------
# Sidebar controls
# ------------------------------------------------------------------
labels_display = st.sidebar.empty()
label_option = labels_display.radio(
    TEXT["label_display"],
    [TEXT["label_delay"], TEXT["label_index"], TEXT["label_none"]],
)

edit_mode = st.sidebar.checkbox(TEXT["edit_design"], value=False)

# ------------------------------------------------------------------
# Editing section
# ------------------------------------------------------------------
if edit_mode:
    max_id = len(st.session_state.df) - 1
    point_id = st.sidebar.number_input(
        TEXT["point_id"],
        min_value=0,
        max_value=max_id,
        value=0,
    )
    point = st.session_state.df.loc[point_id]

    # Delete button
    if st.sidebar.button(TEXT["delete_point"], use_container_width=True):
        delete_point(point_id)

    # Add/Edit expander
    with st.expander(TEXT["add_edit_exp"], expanded=False):
        adding = st.checkbox(TEXT["add_new_point"], value=False)
        subtitle = st.empty()

        c1, c2, c3 = st.columns(3)
        with c1:
            new_x = st.slider(
                TEXT["new_x"],
                value=float(point["x"]),
                min_value=-50.0,
                max_value=50.0,
            )
        with c2:
            new_y = st.slider(
                TEXT["new_y"],
                value=float(point["y"]),
                min_value=-50.0,
                max_value=50.0,
            )
        with c3:
            new_delay = st.number_input(
                TEXT["new_delay"],
                value=float(point["delay"]),
                step=1.0,
            )

        if adding:
            subtitle.markdown(f"### {TEXT['subtitle_add']}")
            preview_point = pd.DataFrame(
                {"x": [new_x], "y": [new_y], "delay": [new_delay]}
            )
        else:
            subtitle.markdown(f"### {TEXT['subtitle_edit'].format(id=point_id)}")
            preview_point = None  # no preview when editing existing

        submitted = st.button(TEXT["save_changes"], type="primary")

        if submitted:
            err = None
            if adding:
                err = validate_new(new_x, new_y, new_delay, st.session_state.df)
                if err:
                    st.error(err)
                else:
                    push_state(st.session_state.df)
                    new_row = pd.DataFrame({"x": [new_x], "y": [new_y], "delay": [new_delay]})
                    st.session_state.df = pd.concat(
                        [st.session_state.df, new_row], ignore_index=True
                    )
                    st.toast(TEXT["toast_added"].format(x=new_x, y=new_y, d=new_delay))
                    st.rerun()
            else:
                # Editing existing point
                push_state(st.session_state.df)
                st.session_state.df.at[point_id, "x"] = new_x
                st.session_state.df.at[point_id, "y"] = new_y
                st.session_state.df.at[point_id, "delay"] = new_delay
                st.toast(TEXT["toast_edited"].format(id=point_id))
                st.rerun()

else:
    # ------------------------------------------------------------------
    # Download section (only visible when not editing)
    # ------------------------------------------------------------------
    file_name = st.sidebar.text_input(
        TEXT["csv_filename"],
        value="blast_grid.csv",
    )
    st.sidebar.download_button(
        label=TEXT["download_csv"],
        data=st.session_state.df.to_csv(index=False),
        file_name=file_name,
        mime="text/csv",
        use_container_width=True,
    )

# ------------------------------------------------------------------
# Plot
# ------------------------------------------------------------------
labels = None
hover_data = {"#id": st.session_state.df.index}

if label_option == TEXT["label_delay"]:
    labels = st.session_state.df["delay"]
elif label_option == TEXT["label_index"]:
    labels = st.session_state.df.index
# label_none ⇒ no text labels

fig = px.scatter(
    st.session_state.df,
    x="x",
    y="y",
    text=labels,
    hover_data=hover_data,
)

# Live preview dot for “add” mode
if edit_mode and adding:
    fig.add_trace(
        go.Scatter(
            x=[new_x],
            y=[new_y],
            mode="markers+text",
            marker=dict(color="red", size=12, symbol="x"),
            text=[TEXT["preview_text"]],
            textposition="top center",
            name=TEXT["preview_legend"],
        )
    )

fig.update_traces(
    marker=dict(color="blue", size=8, line=dict(width=1, color="black")),
    textposition="top center",
)
fig.update_xaxes(visible=False, showgrid=False, scaleanchor="y", scaleratio=1)
fig.update_yaxes(visible=False, showgrid=False)
fig.update_layout(height=600, margin=dict(l=0, r=0, t=0, b=0))

st.plotly_chart(fig, use_container_width=True)