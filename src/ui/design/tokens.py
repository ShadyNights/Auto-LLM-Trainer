"""
Primitive Design Tokens.
These are the foundational values. They have no semantic meaning.
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
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
    "full": "9999px",
}

# Primitive Grays (Deep Charcoal Scale)
gray: Dict[str, str] = {
    "50": "#F9FAFB",
    "100": "#F3F4F6",
    "200": "#E5E7EB",
    "300": "#D1D5DB",
    "400": "#9CA3AF",
    "500": "#6B7280",
    "600": "#4B5563",
    "700": "#374151",
    "800": "#1F2937",
    "900": "#111827",
    "950": "#0B0F14",
}

# Primitive Indigo (Primary Accent)
indigo: Dict[str, str] = {
    "50": "#EEF2FF",
    "100": "#E0E7FF",
    "500": "#6366F1",
    "600": "#4F46E5",
    "700": "#4338CA",
    "900": "#312E81",
}

# Primitive System Colors (Success, Warning, Error, Info)
green: Dict[str, str] = {"500": "#10B981"}
amber: Dict[str, str] = {"500": "#F59E0B"}
red: Dict[str, str] = {"500": "#EF4444"}
blue: Dict[str, str] = {"500": "#3B82F6"}
