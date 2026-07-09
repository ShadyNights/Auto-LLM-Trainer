# Design System

## 1. Design Philosophy
- Modern AI SaaS Dashboard
- Enterprise-first
- Dark-first design
- Minimal visual noise
- High information density
- Content-focused
- Card-based architecture
- Material 3 foundations
- Professional developer tooling aesthetics

## 2. Design Principles
**Visual**
- Consistent spacing
- Strong hierarchy
- Large display typography
- Soft rounded corners
- Elevated surfaces instead of heavy borders
- Low contrast backgrounds
- High contrast content
- Minimal accent color usage

**UX**
- Progressive disclosure
- Clear navigation hierarchy
- Immediate visual feedback
- Persistent navigation
- Accessible interaction states
- Responsive-first

## 3. Color System

**Primary**
| Token | Value |
|---|---|
| Primary | `#BAF2FF` |
| Primary Container | `#00E0FF` |
| Primary Fixed | `#A5EEFF` |
| Primary Fixed Dim | `#00DAF8` |
| Surface Tint | `#00DAF8` |

**Background**
| Token | Value |
|---|---|
| Background | `#0B1326` |
| Surface | `#0B1326` |
| Surface Bright | `#31394D` |
| Surface Dim | `#0B1326` |

**Surface Layers**
| Token | Value |
|---|---|
| Lowest | `#060E20` |
| Low | `#131B2E` |
| Base | `#171F33` |
| High | `#222A3D` |
| Highest | `#2D3449` |

**Secondary**
| Token | Value |
|---|---|
| Secondary | `#BCC7DE` |
| Secondary Container | `#3E495D` |
| Secondary Fixed | `#D8E3FB` |
| Secondary Fixed Dim | `#BCC7DE` |

**Tertiary**
| Token | Value |
|---|---|
| Tertiary | `#FFE6B6` |
| Tertiary Container | `#FEC42E` |
| Tertiary Fixed | `#FFDF9D` |

**Semantic Error**
| Token | Value |
|---|---|
| Error | `#FFB4AB` |
| Error Container | `#93000A` |

**Outline**
| Token | Value |
|---|---|
| Outline | `#859397` |
| Outline Variant | `#3B494C` |

## 4. Typography
**Display Large**
- Font: Space Grotesk
- Weight: 700
- Size: 48px
- Line Height: 1.1

**Mobile Display**
- Size: 32px
- Weight: 700

**Headline**
- Font: Geist
- Size: 24px
- Weight: 600

**Body**
- Font: Geist
- Size: 16px
- Weight: 400
- Line Height: 1.6

**Label**
- Font: Geist
- Size: 12px
- Weight: 500
- Letter Spacing: 0.05em

**Code**
- Font: JetBrains Mono
- Size: 13px
- Weight: 400

## 5. Font Stack
- Primary: Geist
- Display: Space Grotesk
- Monospace: JetBrains Mono

## 6. Spacing System
Uses a 4px baseline grid.
| Token | Value |
|---|---|
| Base | 4px |
| XS | 4px |
| SM | 8px |
| MD | 16px |
| LG | 24px |
| XL | 40px |

Container Width: 1440px

## 7. Border Radius
| Token | Radius |
|---|---|
| Default | 2px |
| LG | 4px |
| XL | 8px |
| Full | 12px |

## 8. Elevation
Uses extremely subtle elevation.

**Levels**
- Border only
- Border + Shadow
- Glow Shadow
- Accent Glow

**Examples**
- `shadow-sm`
- `shadow-md`
- `0 0 15px rgba(0,224,255,.2)`

## 9. Component Library

**Navigation**
- Sidebar
- Mobile Navigation
- Top App Bar
- Bottom Navigation
- Navigation Groups
- Navigation Item
- Active Navigation Item

**Buttons**
- Primary Button
- Secondary Button
- Ghost Button
- Icon Button
- Toggle Button
- CTA Button

**Cards**
- Metric Card
- Status Card
- Information Card
- Analytics Card
- Hero Card
- AI Suggestion Card
- Timeline Card

**Inputs**
- Text Field
- Tag Input
- Segmented Control
- Form Group
- Search Input

**Badges**
- Status Badge
- Provider Badge
- Version Badge
- Pipeline Badge
- AI Badge

**Indicators**
- Online Indicator
- Loading Indicator
- Skeleton Loader
- Blinking Cursor
- Pulse Animation

**Timeline**
- Day Timeline
- Activity Card
- AI Recommendation Card

**Tabs**
- Primary Tabs
- Analytics Tabs
- Feedback Tabs

**Metrics**
- KPI Cards
- Statistics
- Trend Indicators

## 10. Iconography
- Uses: Material Symbols Outlined
- Variants: Outline, Filled
- Size: 18px, 20px, 24px, 32px

## 11. Motion
**Animations**
- Pulse: 2s infinite
- Blink: 1s infinite
- Hover: 200–500ms

**Transitions**
- transition-all
- transition-colors
- transition-shadow
- transition-transform

## 12. Layout System
**Desktop**
- Sidebar + Top Content + Responsive Grid

**Grid**
- 12-column responsive

**Sections**
- Hero
- Metrics
- Main Workspace
- Sidebar Panels
- Footer Navigation

## 13. Responsive Breakpoints
**Primary**
- Mobile
- Tablet
- Desktop

**Tailwind**
- md
- lg

**Mobile Features**
- Bottom Navigation
- Compact Header
- Single Column Layout

**Desktop**
- Sidebar Navigation
- Multi-column Dashboard
- 3-column Workspace

## 14. Interaction States
**Buttons**
- Default
- Hover
- Focus
- Active

**Inputs**
- Default
- Focus
- Filled
- Disabled

**Cards**
- Hover Elevation
- Active Glow

**Navigation**
- Active
- Hover
- Selected

## 15. Visual Style
- Cyber Professional
- AI Dashboard
- Material 3
- Glass-free
- Minimal gradients
- Flat surfaces
- Cyan accent glow
- High readability
- Developer-oriented aesthetic
- Enterprise SaaS appearance

## 16. Design Tokens Summary
- Colors: 40+ semantic color tokens
- Typography: 5 text styles across 3 font families
- Spacing: 4px-based spacing scale
- Border Radius: 4 radius tokens
- Elevation: 4 shadow/glow levels
- Motion: Pulse, blink, hover, transitions
- Components: 20+ reusable UI components
- Icons: Material Symbols
- Layout: Responsive dashboard with sidebar, grids, cards, and mobile navigation
- Accessibility: High-contrast dark theme, semantic colors, clear typography hierarchy, and focus states

## 17. Version 1.0 Freeze Rules (Single Source of Truth)

**Visual Identity Restrictions**
- Material Design 3 inspired
- Glass-free
- Cyan accent
- Minimal gradients
- Flat surfaces
- Developer tooling aesthetics
- Professional appearance
- **Prohibited Effects**: Glassmorphism, Aurora backgrounds, Mesh gradients, Floating cards, Neumorphism, Animated particles, Excessive blur, Multiple accent colors, Random CSS frameworks.

**Strict CSS Value Constraints**
- **Colors**: Use only the semantic tokens defined above (`--c-primary`, `--c-background`, etc). Never use raw hex colors inside components.
- **Typography**: Space Grotesk, Geist, JetBrains Mono ONLY.
- **Spacing**: Strictly 4, 8, 16, 24, 40px. No arbitrary spacing (7px, 13px, etc).
- **Radius**: Strictly 2, 4, 8, 12px. Avoid pill shapes unless explicitly defined.
- **Shadows**: Border, Border+Shadow, Glow, Accent Glow. No heavy floating effects.
- **Motion**: Hover, Focus, Pulse, Blink, Transition. No page-wide animations, floating motion, or decorative movement.

**Implementation Philosophy**
- `Design Tokens -> Theme -> Base Components -> Reusable UI Components -> Pages`
- **Prohibited**: `Page -> Inline CSS -> Random Styles`

**Enforced File Architecture**
The Streamlit application frontend must be structured EXACTLY as follows:
```
src/ui/
├── styles.py          # Theme + CSS injection
├── tokens.py          # Design tokens
├── layout.py          # Page layout helpers
├── components.py      # Cards, metrics, badges, buttons
├── icons.py           # Material Symbols helpers
├── animations.py      # Motion utilities
└── theme.py           # Theme configuration
```
app.py should only assemble the interface using these reusable helpers, not contain styling logic. Every UI change must use existing tokens, follow typography/spacing/component systems, and remain compatible with native Streamlit.
