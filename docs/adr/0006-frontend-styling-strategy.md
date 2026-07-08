# ADR 0006: Native Streamlit Styling Strategy (Frontend Redesign)

## Context
The application required a major UI/UX overhaul to achieve a premium, production-grade SaaS aesthetic (dark themes, refined spacing, professional hover states, metrics cards). Streamlit's default styling is notoriously rigid and difficult to customize, which often leads teams to abandon Streamlit for full frontend rewrites (React/Vue) or resort to messy, scattered inline CSS and JavaScript hacks.

## Decision
We decided to retain Streamlit for full-stack Python simplicity, but implement a **Centralized CSS Design System** via HTML injection.
1. `src/ui/styles.py`: Contains a singular, robust CSS block defining variables (tokens) for colors, spacing, radius, and shadows. It targets stable Streamlit selectors (`data-testid`, `.stButton`) rather than fragile auto-generated emotion classes.
2. `src/ui/components.py`: Contains pure Python functions that return sanitized HTML blocks mapped to our custom CSS utility classes (e.g., `<div class="card card--raised">`).
3. `app.py`: Acts strictly as a layout orchestrator without any embedded HTML or CSS logic.

## Alternatives Considered
- **Custom Streamlit Components**: Building a Node.js/React bridge component for the UI elements. Rejected because it introduces a JavaScript build step, breaks the "pure Python" deployment simplicity, and creates unnecessary maintenance overhead.
- **Tailwind CSS / External Frameworks**: Rejected to avoid external dependency bloat and complex build pipelines. A lightweight custom CSS file is sufficient.
- **Scattered `st.markdown(unsafe_allow_html=True)` inline styles**: Rejected as an anti-pattern that creates duplicated technical debt and makes cohesive redesigns impossible.

## Consequences
- **Positive**: We achieved a stunning, responsive, enterprise-grade dark UI while maintaining 100% Python orchestration. Changing the brand color or spacing grid is now a single-line change in the CSS tokens.
- **Negative**: Relying on CSS injection in Streamlit is not officially supported by Streamlit's rendering engine. If Streamlit heavily alters their DOM hierarchy in future major versions, our CSS selectors may require updates. We mitigated this by targeting the most stable selectors available.
