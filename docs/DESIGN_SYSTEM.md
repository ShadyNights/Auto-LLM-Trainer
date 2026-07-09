# Traveler LLM Design System (v1.0.0)

> [!NOTE]
> The single source of truth for the Traveler LLM interface architecture. This design system ensures visual consistency, accessibility by default, and a scalable hierarchy for a professional 2026 AI SaaS product.

---

## 1. Philosophy
**Minimal, Calm, Intelligent Interfaces.**

AI interfaces often overwhelm users with complexity, animations, and dense data. Our design system exists to ground the experience. We believe that an interface should get out of the way, allowing the AI's intelligence to take center stage.

## 2. Principles
Every UI decision must be vetted against these core principles:
1. **Content over decoration:** Remove unnecessary borders, extreme glassmorphism, or purely decorative shadows.
2. **Information over effects:** Gradients and heavy animations distract. Use them sparingly for Primary CTAs or Hero moments.
3. **Motion supports interaction:** Animation must serve a purpose (e.g., feedback, state changes), never just to "look cool."
4. **Accessibility by default:** Contrast, focus rings, and screen reader support are non-negotiable baselines, not afterthoughts.
5. **One visual language:** A card in the Analytics dashboard must share the same genetic makeup as an AI message card.
6. **Progressive disclosure:** Show only what is necessary right now. Expand on demand.
7. **Consistent rhythm:** Rely strictly on the 8-pt spacing grid.
8. **Performance first:** Heavy CSS calculations and complex DOM structures degrade the perceived speed of the AI. Keep it lightweight.

---

## 3. Tokens & Hierarchy
We prevent duplicate tokens and conflicting rules by adhering to a strict, four-tier inheritance model. *Components never hardcode Hex values.*

**Architecture Flow:**
`Primitive` ➔ `Semantic` ➔ `Theme` ➔ `Component`

**Example:**
`color.gray.900` ➔ `color.surface.primary` ➔ `Theme (Dark)` ➔ `Card Background`

### Naming Convention
Standardized dot-notation for all design tokens:
- Colors: `color.surface.primary`, `color.text.secondary`, `color.status.success`
- Spacing: `space.1` (4px), `space.4` (16px)
- Typography: `type.heading`, `type.body`
- Elevation: `elevation.surface`, `elevation.raised`
- Motion: `motion.entrance`, `motion.hover`
- Z-Index: `z.overlay`, `z.dropdown`

---

## 4. Themes
Themes apply the Semantic tokens to the primitive scale. We define themes interchangeably without hardcoding them into components.

**Core Palette (Dark Theme Default):**
- **Background:** Deep charcoal (`#0B0F14` – `#111827`)
- **Surface:** Neutral dark with subtle elevation adjustments.
- **Primary Accent:** Indigo (`#6366F1`)
- **Success:** Green (`#10B981`)
- **Warning:** Amber (`#F59E0B`)
- **Error:** Red (`#EF4444`)
- **Information:** Cyan/Blue (`#3B82F6`)
- **Borders:** Low-contrast neutral (`#1F2937`)

---

## 5. Layout
- **Spacing System:** Strict 8-pt grid base (`space.1` = 4px, `space.2` = 8px, `space.4` = 16px).
- **Responsive Breakpoints:** 
  - Mobile: `sm` (640px)
  - Tablet: `md` (768px)
  - Desktop: `lg` (1024px)
  - Large Desktop: `xl` (1280px)

---

## 6. Components
We think in UI primitives, not ad-hoc widgets. Every component is inherited from a primitive.

**Component Inheritance Example:**
`Surface` ➔ `Card` ➔ `Metric Card` ➔ `Analytics Card`

---

## 7. AI Components
An AI interaction system sharing a unified visual language:
1. **Conversation Context:** The parent boundary.
2. **Prompt (User):** Right-aligned, distinct background (`color.surface.secondary`).
3. **Response (AI):** Left-aligned, transparent background (`color.bg.base`).
4. **Thinking Indicator:** Minimal pulsing dot layout. No heavy spinners.
5. **Citation:** Small badge format, clickable, clearly linking context to sources.
6. **Feedback:** Thumbs up/down, integrated into the bottom of the Response component.
7. **History:** Navigational sidebar element tracking past Conversations.

---

## 8. Analytics Components
Analytics must follow a strict informational hierarchy:
1. **Overview:** High-level executive summary container.
2. **Metrics:** Atomic number representations (uses `Metric Card`).
3. **Charts:** Time-series visual data.
4. **Timeline:** Chronological event logs.
5. **Logs:** Raw data tables for deep debugging.

---

## 9. Accessibility
Accessibility is a structural requirement.
- **WCAG 2.2 AA Contrast:** All text must meet a minimum 4.5:1 ratio against its background.
- **Minimum Touch Target:** `44x44 px` for all interactive elements (buttons, inputs).
- **Visible Keyboard Focus:** Use `color.accent.primary` with a 2px offset for all focus rings.
- **Semantic Headings:** Strict `h1` through `h6` hierarchy per page.
- **Landmark Regions:** Proper `<nav>`, `<main>`, `<aside>` tagging.
- **Reduced Motion:** Respect `prefers-reduced-motion` by snapping animations to 0ms.
- **Non-color Status Indicators:** Do not rely on red/green alone; use icons alongside color.

---

## 10. Motion
Motion is standardized into precise interaction states. Components do not invent custom animations.
- **Entrance:** Fade in, slight slide up.
- **Exit:** Fade out, slight slide down.
- **Hover:** Slight scale up or border highlight (e.g., Cards).
- **Focus:** Instant ring appearance.
- **Loading:** Subtle opacity pulse.
- **Success:** Quick micro-bounce.

---

## 11. Content Guidelines
The application's voice must reflect the visual calm.
- **Tone:** Professional, Clear, Brief, Helpful, Non-alarming, Actionable.
- **Button Labels:** Verb-first (e.g., "Generate Itinerary", not "Go").
- **Error Messaging:** Explain *what* happened and *how* to fix it. Never blame the user.
- **Empty States:** Provide an action. An empty state without a CTA is a dead end.

---

## 12. Versioning
We track the Design System independently of the Application backend to prevent breaking UI changes.
- **Application Version:** e.g., `v1.5.0`
- **Design System Version:** e.g., `v1.0.0`

---

## 13. Do's & Don'ts

**Do:**
- Use the 8-pt grid for all padding and margins.
- Ensure every interactive element has a `:hover`, `:focus`, and `:active` state.
- Keep gradients reserved for primary CTAs or empty-state illustrations.

**Don't:**
- Introduce a new hex code into `styles.py`. Map it to a Primitive token first.
- Use shadow elevation for pure decoration; use it to signify Z-axis depth (e.g., Modals float above Surfaces).
- Mix naming conventions (e.g., `--card-bg` and `color.surface.card`).

---

## 14. Migration Guide (Legacy to v1.0.0)
When refactoring legacy code (`styles.py` from v0.x):
1. **Delete all hardcoded hex values** in component classes.
2. **Replace variables**: 
   - `--bg-base` ➔ `var(--color-bg-base)`
   - `--accent-primary` ➔ `var(--color-accent-primary)`
3. **Flatten Typography**: Remove custom font sizes on standard widgets; use the 5-level scale (Display, Heading, Title, Body, Caption).
