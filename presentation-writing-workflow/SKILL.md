---
name: presentation-writing-workflow
description: Material planning and drafting workflow for internal sharing, internal reporting, and customer-facing briefings. Use when Codex needs to create, plan, or refine presentation-like materials as PPT image drafts, HTML briefings, editable PPT candidates, or text-only outlines; includes requirement clarification, outline confirmation, slide/screen copywriting, visual prompt writing, image-generation-oriented page guidance with 5-style preview selection, and optional handoff to an image-to-editable-PPT skill.
---

# Presentation Writing Workflow

## Core Rule

Treat every task as a two-axis routing problem:

1. Material type determines strategy, tone, information density, and narrative shape.
2. Output format determines structure, implementation path, and tool choice.
3. For interactive or 3D HTML, visual semantics must be planned in the outline before style or implementation.

Do not treat HTML as a long PPT. Do not treat PPT as a paginated web page.
Do not add 3D as decoration. Use 3D only when it helps the audience understand a relationship, path, hierarchy, change, causality, spatial distribution, system, or operating model.

## Mandatory Human Checkpoints

Pause for user input at these checkpoints:

1. Before writing: confirm material type, output format, audience, scenario, page/screen count, duration, source material, confidentiality limits, preferred style, and whether HTML should be static, interactive, dashboard-like, or immersive/3D.
2. After outline: present a table outline and ask the user to confirm or revise it before drafting pages/screens.
3. Before generating full PPT image drafts: use `image_gen` to create 5 style preview images based on the confirmed material type, user style requirements, and one representative page. Ask the user to choose one preview or request adjustments before generating the full page set.
4. Before editable PPT conversion: if the output is PPTX or editable PPT, explain that complex image backgrounds, light effects, 3D compositions, gradients, and layered visual pages may convert poorly. Ask whether to keep image-based slides or call an existing image-to-PPT skill.

Never generate full page/screen content before the outline is confirmed.

## Routing

First classify material type:

- Internal sharing: story-led, immersive, memorable, visually bold.
- Internal reporting: conclusion-first, clear, structured, decision-oriented.
- Customer briefing: professional, clean, credible, moderately technological.

Then classify output format:

- PPT image draft: write page-by-page content and visual prompts for image generation. Do not use Codex's built-in presentation-writing or PPT-generation skill for final creation.
- HTML: write screen/section content and implementation-oriented visual prompts for a web briefing or interactive report.
- Editable PPT: first plan as PPT image draft or text structure, then ask whether to convert through an image-to-editable-PPT skill.
- Text only: produce outline, page/screen copy, speaker notes if requested, and no generation handoff.

Output formats explicitly supported by this skill:

- PPT image draft
- HTML static briefing
- HTML interactive report/dashboard
- HTML immersive scroll story
- HTML 3D/semantic visualization experience
- Editable PPT
- Text only

Use this route table:

| Material type | PPT image draft | HTML |
|---|---|---|
| Internal sharing | Cinematic visual storytelling, strong chapter breaks, generated-image pages | Immersive scroll story, bold motion, optional 3D/animation |
| Internal reporting | Clear executive pages, metrics, risks, roadmap | Report page/dashboard, charts, tables, decision panels |
| Customer briefing | Premium proposal visuals, clean tech style, credibility | Interactive proposal site, solution flow, cases, architecture |

## Outline Stage

If output is PPT image draft or editable PPT, use a page-based table:

| Page | Chapter | Page title | Core message | Page type | Visual intensity | Notes |
|---|---|---|---|---|---|---|

If output is HTML, use a section-based table:

| Section | Screen position | Title | Core message | Content form | Interaction/motion | Notes |
|---|---|---|---|---|---|---|

If output is interactive HTML or 3D HTML, add visual-semantics columns at outline stage:

| Section | Screen position | Title | Core message | Audience should understand | Visual semantic model | 3D role | Interaction | Notes |
|---|---|---|---|---|---|---|---|---|

Use the visual semantic model column to name the actual relationship being represented, such as network, funnel, star map, hierarchy, orbit/core, map, sandbox, timeline, decision chain, operating map, or case path. Mark `3D role` as `none` when 3D would not improve understanding.

After the table, ask for confirmation. Offer specific revision handles such as page count, chapter order, key messages, visual intensity, audience focus, or output format.

## Drafting Stage

After outline confirmation, draft in the format matching the output.

For PPT image drafts:

```text
Page X | Title
Copy:
- Main headline:
- Supporting line:
- Key points:

Visual prompt:
- Style:
- Composition:
- Background:
- Main elements:
- Color and lighting:
- Text-safe areas:
- Avoid:
```

For HTML:

```text
Section X | Title
Copy:
- Heading:
- Body:
- Cards/buttons/labels:

Visual prompt:
- Layout:
- Components:
- Background and visual system:
- Visual semantic model:
- 3D role, if any:
- Interaction/motion:
- Responsive behavior:
- Avoid:
```

## PPT Image Preview Stage

For PPT image drafts, do not generate the full deck images immediately after page drafting. First create 5 visual style previews with the built-in `image_gen` tool:

- Use a representative page, preferably the cover, a chapter divider, or the most visually important page.
- Keep the user's style requirements and material type visible in all 5 options.
- Vary only meaningful visual directions: cinematic intensity, professional cleanliness, technology feel, layout density, color/lighting, and metaphor system.
- Label the previews as Option 1-5 in the response and summarize the design difference in one short line each.
- Ask the user which option to use, or whether to combine/adjust options.

Only after the user confirms a preview direction should you generate the full page image draft set. Apply the chosen direction consistently across all pages while still adapting composition to each page's content.

## Reference Selection

Read only the references needed for the current route:

- For internal sharing: `references/internal-sharing.md`
- For internal reporting: `references/internal-report.md`
- For customer briefings: `references/customer-briefing.md`
- For outline and checkpoint behavior: `references/outline-and-checkpoints.md`
- For style routing and page/screen patterns: `references/visual-styles.md`
- For image generation visual prompts: `references/image-generation-prompting.md`
- For HTML output: `references/html-output.md`

## Tool Guidance

For PPT image drafts, prepare image-generation-ready prompts per page. When image generation is available, prefer the built-in `image_gen` tool to create slide images. If `image_gen` is unavailable or blocked, ask before using another image-generation route.

For HTML, implement with the simplest frontend stack that satisfies the experience:

- Static HTML/CSS/JS for compact materials.
- React or a local app structure when interaction, state, routing, or component reuse matters.
- Chart libraries for report/dashboard pages.
- Three.js or animation libraries only when the material type and story justify the complexity.

### Optional High-Impact HTML Enhancement

When the user asks for a more cinematic, visually striking, technology-oriented, or motion-rich HTML experience, recommend this optional three-stage workflow:

1. `imagegen-frontend-web`: explore and confirm the visual direction with reference images.
2. `gpt-taste`: implement the HTML with stronger layout variance, typography, spacing, and purposeful motion.
3. `impeccable`: critique, audit, and polish the implemented page.

This is a recommendation, not the default execution path:

- Do not load, invoke, install, or hand off to these skills automatically.
- Briefly explain the expected visual benefit and additional token/tool cost.
- Ask for explicit user confirmation before using any stage.
- Allow the user to choose one stage, selected stages, or the complete workflow.
- If the user does not confirm, continue with this skill's standard HTML workflow.
- Do not block HTML creation when any recommended skill is unavailable.

For semantic 3D HTML:

- Start from the outline's `Audience should understand` and `Visual semantic model`, not from a style preset.
- Use 3D for relationships that benefit from space, depth, motion, or interaction: customer networks, industry clusters, operating maps, capability cores, decision chains, case paths, or layered roadmaps.
- Avoid decorative 3D backgrounds that can be removed without changing audience understanding.
- Bind each 3D scene to visible copy, labels, data, and interactions. The model should carry terms from the material, such as customer groups, products, owners, stages, risks, or case results.
- Use 2D cards, charts, or text for sections where 3D does not add semantic clarity.

For editable PPT, ask before using an image-to-editable-PPT skill. Prefer image-based slides when visual fidelity matters more than editability.
