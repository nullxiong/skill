# HTML Output

Use HTML output when the material should be browsed, scrolled, interacted with, shared as a web page, or presented as an interactive briefing.

## Outline Design

Structure by section/screen, not by slide page. A section may contain more detail than a slide and can use scrolling, expansion, or interaction.

Use:

| Section | Screen position | Title | Core message | Content form | Interaction/motion | Notes |
|---|---|---|---|---|---|---|

For immersive, interactive, or 3D HTML, use the semantic outline instead:

| Section | Screen position | Title | Core message | Audience should understand | Visual semantic model | 3D role | Interaction | Notes |
|---|---|---|---|---|---|---|---|---|

The `Visual semantic model` must describe the relationship being shown, not the mood. Good entries include customer network, industry star map, resource funnel, AI XDR capability core, operating map, decision chain, regulatory leverage network, case replay path, risk matrix, and roadmap stack.

Use `3D role` only when depth, spatial grouping, orbiting, layering, or motion clarifies the message. If removing the 3D would not reduce understanding, mark `3D role` as none and use 2D layout instead.

## Drafting Design

For each section, specify both copy and implementation direction:

- Heading and body copy.
- Cards, labels, buttons, chart labels, or navigation text.
- Layout, component structure, visual system, interaction/motion, responsive behavior.
- For semantic 3D sections: the exact entities, labels, data, stages, or relationships the 3D scene must carry.
- For non-3D sections: the reason 2D, charts, or text are clearer.

## Five-Style Composite Preview Flow

Before implementing HTML when visual direction matters, create 5 composite preview boards with `image_gen` and ask the user to choose one direction.

Each option should be one combined preview image containing 5-6 key screen thumbnails. Use the confirmed outline to choose the screens, such as:

- Hero or opening screen.
- Core narrative or problem framing.
- KPI/dashboard/report section.
- Solution architecture or operating model.
- Case/timeline/roadmap section.
- Closing or decision screen.

The 5 boards should share the same topic, outline, and content constraints, but vary the design system:

1. Immersive cinematic story.
2. Premium clean technology briefing.
3. Dense executive dashboard/report.
4. Interactive solution/product narrative.
5. Minimal professional consulting style.

Present the boards as Option 1-5 with concise notes about visual tone, layout system, information density, motion implication, and best-fit use case. Do not implement the HTML until the user confirms one option or asks for adjustments.

## Semantic 3D Rule

Do not start with "cool 3D" as the concept. Start with the business relationship the audience must understand:

- Network: customers, products, regulators, executives, owners, or support roles are connected.
- Cluster/star map: customers or opportunities are grouped by industry, value, stage, or maturity.
- Funnel/flow: resources, attention, or opportunities move from one state to another.
- Core/orbit: a platform or strategy anchors surrounding capabilities.
- Sandbox/map: regions, industries, accounts, or operating territories are spatially arranged.
- Operating map: one account is decomposed into fields such as relationship, spend, share, product status, opportunity, owner, and next action.
- Case path: a customer case moves from trigger, action, proof, and result into reusable method.

Every 3D scene should have visible labels or interactions tied to the material's actual language. Avoid unlabeled particles, generic globes, abstract shapes, and decorative HUD frames unless they support a named semantic model.

## Tool Choices

- Static HTML/CSS/JS: compact pages with simple interaction.
- React: component-heavy, reusable sections, stateful interactions, or more complex UI.
- Chart.js/ECharts/Recharts: internal reports, dashboards, metrics, trend charts.
- Three.js/WebGL: immersive internal sharing or high-impact customer demos where 3D supports the story.
- Animation libraries: use when transitions are part of the communication rhythm.

For 3D-heavy HTML, prefer an app structure such as Vite + React + Three.js or React Three Fiber when the project needs multiple scenes, stateful interactions, scroll-linked camera moves, reusable components, or ongoing iteration. Single-file HTML is acceptable for compact prototypes, but avoid using it as the final shape for complex semantic 3D experiences.

## Optional Three-Stage Visual Enhancement

Recommend, but do not automatically use, this workflow when the user explicitly wants a cool, cinematic, high-impact, technology-oriented, or motion-rich result:

| Stage | Optional skill | Purpose |
|---|---|---|
| Visual direction | `imagegen-frontend-web` | Generate reference frames and align on composition, color, atmosphere, and visual language before implementation. |
| HTML implementation | `gpt-taste` | Build with stronger layout variance, typography, spacing, GSAP-style motion direction, and anti-template constraints. |
| Design review | `impeccable` | Critique, audit, and polish hierarchy, layout, type, color, motion, responsiveness, and common AI-design anti-patterns. |

Before using it:

- State that it may consume additional model tokens and image-generation quota.
- Ask the user whether to use the full workflow or selected stages.
- Treat silence or no confirmation as a decision to stay with the standard HTML workflow.
- Never install a missing skill without a separate explicit installation request.

## Material Differences

Internal sharing HTML:

- Immersive scroll story.
- Bold visual sections and strong transitions.
- Optional full-bleed generated images or 3D scenes.

Internal reporting HTML:

- Dashboard/report structure.
- KPI cards, tables, risk matrices, decision panels.
- Dense but organized scanning.

Customer briefing HTML:

- Interactive proposal or briefing site.
- Clean navigation, solution flow, cases, architecture, roadmap.
- Professional technology cues, not excessive spectacle.
