import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tempfile
import os
import io

def create_timing_gif(df: pd.DataFrame, fps: int = 2, duration_ms: int = 500) -> bytes:
    df = df.sort_values("delay").reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Blast Timing Animation", fontsize=14)

    sc = ax.scatter(df["x"], df["y"], c="red", s=150, edgecolors="k")
    for _, row in df.iterrows():
        ax.text(row.x, row.y, str(row.delay), ha="center", va="center", fontsize=8)

    def init():
        sc.set_color(["red"] * len(df))
        return sc,

    def animate(frame):
        colors = ["red"] * len(df)
        colors[frame] = "lime"
        sc.set_color(colors)
        return sc,

    frames = len(df)
    anim = FuncAnimation(fig, animate, init_func=init, frames=frames,
                         interval=duration_ms, blit=False)

    # 1️⃣ Write to temporary file
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp:
        tmp_path = tmp.name
    anim.save(tmp_path, writer="pillow", fps=fps)
    plt.close(fig)

    # 2️⃣ Read back into BytesIO
    with open(tmp_path, "rb") as f:
        gif_bytes = f.read()
    os.remove(tmp_path)
    return gif_bytes