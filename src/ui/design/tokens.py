"""
Primitive Design Tokens.
Extracted from the Tailwind design language specification.
"""
from typing import Dict

# 8-pt spacing system
spacing: Dict[str, str] = {
    "0": "0px",
    "1": "4px",
    "2": "8px",
    "3": "12px",
    "4": "16px",
    "5": "20px",
    "6": "24px",
    "8": "32px",
    "10": "40px",
    "12": "48px",
    "16": "64px",
    "20": "80px",
    "24": "96px",
}

# Border radii
radius: Dict[str, str] = {
    "none": "0px",
    "sm": "0.125rem",
    "md": "0.25rem",
    "lg": "0.5rem",
    "xl": "0.75rem",
    "full": "9999px",
}

# Primitive Space Blue Scale
space_blue: Dict[str, str] = {
    "100": "#dae2fd",
    "200": "#bac9cd",
    "300": "#859397",
    "400": "#3b494c",
    "500": "#2d3449",
    "600": "#222a3d",
    "700": "#171f33",
    "800": "#131b2e",
    "900": "#0b1326",
    "950": "#060e20",
}

# Primitive Cyan Scale
cyan: Dict[str, str] = {
    "200": "#baf2ff",
    "300": "#a5eeff",
    "400": "#00e0ff",
    "500": "#00daf8",
    "600": "#006877",
    "700": "#005f6d",
    "800": "#004e5a",
    "900": "#00363f",
}

# Primitive System Colors
green: Dict[str, str] = {"500": "#10B981"}
amber: Dict[str, str] = {"500": "#F59E0B"}
red: Dict[str, str] = {"500": "#ffb4ab"}
blue: Dict[str, str] = {"500": "#bcc7de"}
