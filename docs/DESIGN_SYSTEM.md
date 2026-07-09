# Traveler LLM Design System (2026 Specification)

> [!NOTE]
> This document is the authoritative design specification for the Traveler LLM platform. It defines the visual identity, tokens, component architectures, patterns, and principles required to build a scalable, accessible, and premium AI SaaS experience.

---

## 1. Design Philosophy & Foundations

Our interface is built on a "Dark-first, Content-first" philosophy. The aesthetic is strictly professional, minimizing visual noise to maximize information density.

### 1.1 Design Goals
- **Professional Enterprise SaaS**: The UI must feel robust, trustworthy, and precise.
- **AI-Native**: Built from the ground up to display generative text, active streams, and complex multi-modal analytics effortlessly.
- **Invisible UI**: The interface should recede; the user's workflow and the AI's output are the heroes.
- **Glass-Free, Flat Surfaces**: Rely on deep, rich, solid colors and subtle elevation layers rather than aggressive blurs or translucent glassmorphism.

### 1.2 Accessibility Principles (WCAG 2.2 AA)
- **Contrast Compliance**: All text must meet a minimum 4.5:1 contrast ratio against its background. Non-text interactive elements must meet 3:1.
- **Interaction Targets**: Minimum target size for interactive elements is 44x44px (except in compact density views).
- **Keyboard Navigation**: All interactive elements must be fully keyboard accessible with defined `Skip Navigation` anchors.
- **Screen Reader Labels**: Icons and visual states must have `aria-labels` or visually hidden `.sr-only` text.
- **Reduced Transparency**: Ensure opacities can be bypassed if reduced transparency is requested.
- **High Contrast**: Enforce `#000000` backgrounds and `#FFFFFF` text boundaries when high contrast is active.

### 1.3 Consistency Rules
- Never introduce one-off hex codes. All values must map to the Semantic Token Hierarchy.
- Prefer semantic layout primitives over raw CSS grids in component logic.

---

## 2. Token Architecture Hierarchy

The token architecture is divided into three distinct layers to ensure scalability and maintainability:

1. **Foundation Tokens**: Raw values (Hex codes, pixel measurements, ms durations).
2. **Semantic Tokens**: Contextual definitions (Primary, Surface, Success, Border).
3. **Component Tokens**: Element-specific mappings (`button-bg`, `card-radius`).

### 2.1 Foundation Tokens

**Theme Palette**
- Primary: `#BAF2FF`, `#00E0FF`, `#A5EEFF`, `#00DAF8`
- Surface (Dark): `#0B1326`, `#31394D`, `#060E20`, `#131B2E`, `#171F33`, `#222A3D`, `#2D3449`
- Secondary: `#BCC7DE`, `#3E495D`, `#D8E3FB`
- Tertiary: `#FFE6B6`, `#FEC42E`, `#FFDF9D`
- Semantic: `#FFB4AB`, `#93000A`, `#81C995`, `#FDD663`
- Outlines: `#859397`, `#3B494C`

**Typography Scale (Responsive)**
| Role | Font | Size (Desk/Mob) | Weight | Line Height | Tracking |
|---|---|---|---|---|---|
| **Display** | Space Grotesk | 48px / 32px | 700 | 1.1 | 0em |
| **Headline** | Geist | 24px / 20px | 600 | 1.2 | -0.01em |
| **Title** | Geist | 20px / 18px | 600 | 1.4 | 0em |
| **Body** | Geist | 16px / 16px | 400 | 1.6 | 0em |
| **Label** | Geist | 12px / 12px | 500 | 1.4 | 0.05em |
| **Code** | JetBrains Mono | 13px / 13px | 400 | 1.5 | 0em |

**Spacing Grid (4px Baseline)**
- `space-base`: 4px | `space-xs`: 4px | `space-sm`: 8px | `space-md`: 16px | `space-lg`: 24px | `space-xl`: 40px | `space-2xl`: 64px

**Border Radius**
- `radius-sm`: 2px | `radius-md`: 4px | `radius-lg`: 8px | `radius-full`: 12px | `radius-pill`: 9999px

**Opacity**
- `opacity-hover`: `0.08` | `opacity-focus`: `0.12` | `opacity-disabled`: `0.38` | `opacity-scrim`: `0.60`

**Motion**
- `duration-fast`: `150ms` | `duration-normal`: `200ms` | `duration-slow`: `300ms` (Max duration for standard transitions)
- `ease-standard`: `cubic-bezier(0.2, 0.0, 0, 1.0)` | `ease-enter`: `cubic-bezier(0.0, 0.0, 0.2, 1)` | `ease-exit`: `cubic-bezier(0.4, 0.0, 1, 1)`

### 2.2 Semantic Tokens

**Action & Brand**
- `color-primary`: Brand text, active links.
- `color-primary-container`: Primary buttons, active selections.
- `color-surface-tint`: Focused glow origins.

**Surface Elevation Hierarchy**
- `color-bg-base`: Absolute root background.
- `color-layer-lowest`: Underlays, sidebars.
- `color-layer-base`: Standard cards and widgets.
- `color-layer-highest`: Tooltips, snackbars.

**Feedback & Status**
- `color-error`: Validation text, destructive actions.
- `color-success`: Completed states, online indicators.
- `color-warning`: Pending states.

**Data Visualization Tokens (Charts & Graphs)**
- `chart-1`: `#00E0FF` (Primary metric)
- `chart-2`: `#FEC42E` (Secondary metric)
- `chart-3`: `#BCC7DE` (Tertiary metric)
- `chart-success`: `#81C995`
- `chart-warning`: `#FDD663`
- `chart-error`: `#FFB4AB`
- `chart-grid-line`: `color-outline-variant` (Opacity 0.3)
- `chart-axis-text`: `color-secondary`
- `chart-tooltip-bg`: `color-layer-highest`

**Focus & Borders**
- `--t-focus-ring`: `0 0 0 2px color-bg-base, 0 0 0 4px color-primary-container` (Universally applied to ALL interactive elements on `:focus-visible`).
- `color-outline`: High contrast boundaries.
- `color-outline-variant`: Subtle dividers.

### 2.3 Interaction Elevation Rules
Elevation is strictly mapped to interaction context to avoid arbitrary shadow usage.
- **Level 0 (Background)**: `color-bg-base`, no shadow. (App background)
- **Level 1 (Card)**: `color-layer-base`, `shadow-sm`. (Default cards)
- **Level 2 (Hover)**: Translate Y `-2px`, `shadow-md`. (Interactive cards, active buttons)
- **Level 3 (Overlay)**: `color-layer-high`, `shadow-lg`. (Dropdowns, Popovers)
- **Level 4 (Modal)**: `color-layer-highest`, `shadow-xl`, requires `opacity-scrim`. (Drawers, Dialogs)

---

## 3. Structural Systems

### 3.1 Density Modes
AI dashboards require flexible data density.
- **Compact**: `padding` halves, row heights collapse (Useful for massive analytics tables).
- **Comfortable** (Default): Adheres exactly to standard `space-*` tokens.
- **Spacious**: `padding` doubles, ideal for focus modes or single-task workflows.

### 3.2 Responsive & Layout Tokens
- **Max Sidebar Width**: `280px`
- **Collapsed Sidebar Width**: `64px`
- **Max Content Width**: `1440px` (Dashboard grids)
- **Reading Width**: `720px` (Optimal line length for AI generations and documentation)

### 3.3 Scrollbars
- **Track**: `transparent` or `color-layer-lowest`.
- **Thumb**: `color-outline-variant`, `radius-pill`.
- **Hover**: Thumb shifts to `color-outline`.

### 3.4 Icon Rules (Material Symbols Outlined)
- **18px**: Inline text context, compact table actions.
- **20px**: Standard buttons, default UI actions.
- **24px**: Main sidebar navigation, empty states, prominent toggles.
- **32px**: Hero section icons, major empty state graphics.

---

## 4. Component Specifications

*Note: Components are classified by Maturity: Stable, Beta, Experimental.*

### 4.1 Buttons [Stable]
- **Primary**: Background `color-primary-container`, Text `color-bg-base`. 
- **Interaction**: Scales to `0.98` on `:active`. Universally receives `--t-focus-ring` on focus.

### 4.2 Tables [Stable]
- **Header**: Sticky `top-0`, Background `color-layer-low`, typography `Label`.
- **Rows**: Apply `opacity-hover` on row `:hover`.
- **Zebra Striping**: Disabled by default for cleaner data view.
- **Selected**: Background `color-primary-fixed` (10% opacity).

### 4.3 Code Blocks [Stable]
- **Background**: `color-layer-lowest`.
- **Typography**: JetBrains Mono `13px`.
- **Features**: Must include a sticky "Copy" ghost button top-right. Line wrapping defaults to disabled (horizontal scroll enabled) to preserve formatting.

### 4.4 AI-Specific Components [Beta]
- **Streaming Response**: Content fades in with `ease-enter`. Ends with `anim-blink` text cursor `▌`.
- **Reasoning Indicator**: Collapsible accordion. Title pulses `anim-pulse` during generation.
- **Citation Badge**: Tiny pill badge (`radius-pill`), `color-surface-bright`.
- **Confidence Badge**: Green/Yellow/Red indicator alongside AI generation scores.
- **Processing State**: Skeleton loaders strictly matching the resulting text geometry.
- **Provider Badge**: Distinct visual tag identifying the active LLM (e.g., Groq, LLaMA).

### 4.5 AI Transparency [Mandatory]
Generated content must permanently display its lineage:
- **Generated By**: Identifies the AI agent.
- **Timestamp**: Exact generation time.
- **Provider**: The underlying model.
- **Version**: The Prompt/System Config version used.

### 4.6 Empty & Error States [Stable]
**Empty States** must always include:
1. `24px+` Icon
2. `Title` typography
3. `Body` description explaining *why* it's empty
4. Primary Action Button
5. (Optional) Ghost Secondary Action

**Error States** are strictly differentiated:
- **Recoverable**: Clear CTA to retry/fix (e.g., "Reload Data").
- **System**: Fatal errors. Displayed in full-screen modals.
- **Validation**: Inline red borders on form inputs.
- **Permission**: "Access Denied" with `color-warning` iconography.
- **Network**: Toast notification indicating offline status.

---

## 5. File Structure Architecture

Regardless of the underlying framework (Streamlit, React, HTML), the CSS architecture maps to this official structure:
```text
styles/
├── tokens.css       # Foundation & Semantic variable definitions
├── base.css         # Reset, Typography, Accessibility rules, Scrollbars
├── layout.css       # Grid systems, Density modes, Containers
├── components/
│   ├── button.css
│   ├── card.css
│   ├── form.css
│   ├── table.css
│   └── sidebar.css
└── utilities.css    # Single-purpose helpers (e.g., .sr-only, .text-center)
```

---

## 6. Design QA Checklist

Before merging any UI changes, developers must verify:
- [ ] **Spacing**: Exclusively uses 4px baseline `space-*` tokens.
- [ ] **Contrast**: Text passes WCAG 2.2 AA (4.5:1).
- [ ] **Focus**: Every interactive element uses `--t-focus-ring`.
- [ ] **Responsive**: Layout scales correctly on Mobile, Tablet, and Desktop.
- [ ] **Overflow**: No horizontal layout shifting or clipped text. Scrollbars styled correctly.
- [ ] **Colors**: Absolutely zero hardcoded hex values in the component.

---

> [!IMPORTANT]
> **Freeze the Design Language**
> The visual identity, semantic token architecture, typography system, spacing scale, elevation model, motion language, and component behavior defined in this specification constitute the baseline design language of Traveler LLM. Future iterations should extend this system through additive, versioned changes rather than introducing parallel styles, duplicate tokens, or conflicting interaction patterns.
