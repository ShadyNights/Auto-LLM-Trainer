"""
Semantic Design Tokens (Themes).
Extracted directly from Tailwind configuration mapping.
"""
from src.ui.design import tokens

dark_theme = {
    # Backgrounds
    "color.bg.base": tokens.space_blue["900"],
    "color.bg.surface.lowest": tokens.space_blue["950"],
    "color.bg.surface.low": tokens.space_blue["800"],
    "color.bg.surface": tokens.space_blue["700"],
    "color.bg.surface.high": tokens.space_blue["600"],
    "color.bg.surface.highest": tokens.space_blue["500"],
    
    # Text
    "color.text.primary": tokens.space_blue["100"],
    "color.text.secondary": tokens.space_blue["200"],
    "color.text.muted": tokens.space_blue["300"],
    
    # Borders
    "color.border.default": tokens.space_blue["400"],
    "color.border.hover": tokens.space_blue["300"],
    
    # Primary Accent (Cyan)
    "color.accent.primary": tokens.cyan["400"],
    "color.accent.hover": tokens.cyan["300"],
    "color.accent.active": tokens.cyan["500"],
    "color.accent.subtle": f"{tokens.cyan['400']}26", # 15% opacity hex
    
    # On-Primary (Text on top of Primary backgrounds)
    "color.text.on.primary": tokens.cyan["900"],
    "color.text.on.primary.container": tokens.cyan["700"],
    
    # Semantic Status
    "color.status.success": tokens.green["500"],
    "color.status.success.subtle": f"{tokens.green['500']}26",
    
    "color.status.warning": tokens.amber["500"],
    "color.status.warning.subtle": f"{tokens.amber['500']}26",
    
    "color.status.error": tokens.red["500"],
    "color.status.error.subtle": f"{tokens.red['500']}26",
    
    "color.status.info": tokens.blue["500"],
    "color.status.info.subtle": f"{tokens.blue['500']}26",
}
