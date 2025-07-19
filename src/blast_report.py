import pandas as pd
import numpy as np
from typing import Dict

def delay_continuity(df: pd.DataFrame, max_jump: float = 2.0) -> Dict[str, any]:
    """Check if delay increases monotonically within tolerance."""
    diffs = df["delay"].diff().dropna()
    violations = diffs[diffs.abs() > max_jump]
    return {
        "ok": violations.empty,
        "violations": violations.to_dict(),
        "max_jump": max_jump,
    }

def gap_overlap_map(df: pd.DataFrame, spacing: float, burden: float) -> pd.DataFrame:
    """Return hole-to-hole distance vs expected spacing/burden."""
    from scipy.spatial.distance import pdist, squareform
    dist = squareform(pdist(df[["x", "y"]]))
    np.fill_diagonal(dist, np.nan)
    df["min_dist"] = np.nanmin(dist, axis=1)
    df["gap_ratio"] = df["min_dist"] / min(spacing, burden)
    return df

def symmetry_score(df: pd.DataFrame) -> float:
    """Simple symmetry score 0-1 based on centroid distance."""
    centroid = df[["x", "y"]].mean()
    mirrored = df.copy()
    mirrored[["x", "y"]] = 2 * centroid - mirrored[["x", "y"]]
    dists = pd.merge(df, mirrored, on=["x", "y"], how="inner")
    return len(dists) / len(df)