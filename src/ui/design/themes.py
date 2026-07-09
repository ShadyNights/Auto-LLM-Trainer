"""
Semantic Design Tokens (Themes).
Maps primitive tokens to meaningful semantic roles.
"""

from src.ui.design import tokens

# Default Dark Theme
dark_theme = {
    # Backgrounds
    "color.bg.base": tokens.gray["950"],
    "color.bg.surface": tokens.gray["900"],
    "color.bg.surface.raised": tokens.gray["800"],
    
    # Text
    "color.text.primary": tokens.gray["50"],
    "color.text.secondary": tokens.gray["400"],
    "color.text.muted": tokens.gray["500"],
    
    # Borders
    "color.border.default": tokens.gray["800"],
    "color.border.hover": tokens.gray["700"],
    
    # Primary Accent (Indigo)
    "color.accent.primary": tokens.indigo["500"],
    "color.accent.hover": tokens.indigo["600"],
    "color.accent.active": tokens.indigo["700"],
    "color.accent.subtle": f"{tokens.indigo['500']}26", # 15% opacity hex
    
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
