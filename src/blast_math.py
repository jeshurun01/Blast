"""
Core blast-design calculations.
Add spacing / burden logic here when ready.
"""

from typing import Tuple
import math

# ---------- constants ----------
ROCK_DENSITY_T_M3: float = 2.7     # placeholder
POWDER_FACTOR_KG_T: float = 0.45   # placeholder

# ---------- existing ----------
def linear_charge(explosive_density: float, hole_diameter_mm: float) -> float:
    """kg/m along the hole."""
    return explosive_density * hole_diameter_mm ** 2 / 1273


# For cut holes, the required linear charge is calculated based on the hole diameter and the explosive density.
def required_linear_charge(
        o_h_diameter: int, 
        cc_distance: float) -> float:
    """
    The charge needed to break out the cut holes.
    o_h_diameter: open hole diameter
    cc_distance: center to center distance between open holes and charged holes

    return: float
    """
    return 1.67 * math.pow(10, -3) * math.pow(cc_distance/o_h_diameter, 3/2) * (cc_distance - (o_h_diameter/2))


def hole_charge_mass(linear_charge_kg_m: float, charge_length_m: float) -> float:
    """kg per hole."""
    return linear_charge_kg_m * charge_length_m


def total_charge_mass(charge_mass_per_hole: float, hole_count: int) -> float:
    """kg for the entire blast."""
    return charge_mass_per_hole * hole_count


# ---------- TODO: blast-pattern ----------
def spacing(burden: float, sp_ratio: float = 1.15) -> float:
    """
    Placeholder for spacing calculation.
    bench_height  : m
    burden        : m
    returns       : m
    """
    return sp_ratio * burden


def burden(
        charge_length_m: float, 
        linear_charge_kg_m, 
        hole_depth_m: float, 
        powder_factor: float = POWDER_FACTOR_KG_T, 
        sp_ratio: float = 1.15) -> float:
    """
    Placeholder for burden calculation.
    charge_length : m
    hole_depth    : m
    linear_charge : kg
    powder_factor : kg/m3
    sp_ratio      : burden spacing ratio
    returns       : m
    """
    return math.sqrt((linear_charge_kg_m * charge_length_m) / (sp_ratio * hole_depth_m * powder_factor)) # quick rule of thumb

