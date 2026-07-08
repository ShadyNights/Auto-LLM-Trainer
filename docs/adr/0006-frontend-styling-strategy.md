# ADR 0006: Native Streamlit Styling Strategy

## Context
The platform required a comprehensive UI/UX overhaul to achieve a premium, production-grade SaaS aesthetic featuring dark themes, refined spacing, and professional interactive states. Streamlit's default styling is highly rigid, which historically forces engineering teams to either abandon the framework entirely (for React/Vue) or pollute the codebase with fragmented, unmaintainable inline styling hacks.

## Decision
**Implement a Centralized CSS Design System via HTML Injection.**
We elected to retain Streamlit's pure-Python deployment simplicity while completely subverting its default aesthetic through strict abstraction:
1. **`src/ui/styles.py`**: A centralized CSS architecture defining strict design tokens (colors, spacing, shadows). We target *stable* Streamlit selectors (e.g., `[data-testid="stSidebar"]`, `.stButton`) rather than fragile auto-generated emotion classes.
2. **`src/ui/components.py`**: Pure Python wrappers that output sanitized HTML mapped perfectly to our custom CSS utility classes.
3. **`app.py`**: Acts exclusively as a layout orchestrator, devoid of any raw CSS or HTML logic.

## Alternatives Considered
- **Custom Node.js Streamlit Components**: *Rejected*. Introducing a React/Node.js build step destroys the "pure Python" operational simplicity and drastically inflates maintenance overhead.
- **External CSS Frameworks (Tailwind)**: *Rejected* to prevent dependency bloat and complex build pipelines.
- **Scattered `st.markdown` Inline Styles**: *Rejected* as an egregious anti-pattern that guarantees technical debt.

## Consequences
> [!TIP] 
> **Positive Outcomes**
> - **SaaS Aesthetic**: Achieved an enterprise-grade, responsive UI while maintaining 100% Python backend orchestration.
> - **Design Scalability**: Adjusting brand colors, spacing, or radius variables requires only a single-line change in the token file.

> [!WARNING]
> **Negative Outcomes**
> - **Selector Fragility**: Relying on CSS injection means our styles could break if Streamlit fundamentally alters their DOM hierarchy in major version updates. We mitigated this by targeting the most stable selectors available.
