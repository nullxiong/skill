# Outline and Checkpoints

## Requirement Questions

Ask only the questions needed to start. Prefer one compact checklist:

- Material type: internal sharing, internal reporting, customer briefing, or other.
- Output format: PPT image draft, HTML, editable PPT, or text only.
- Audience and usage scene.
- Expected length: page/screen count and presentation duration.
- Source material and facts that must be included.
- Style preference and any forbidden styles.
- Confidentiality, brand, or compliance limits.

If the user already provided an answer, do not ask again.

## Outline Confirmation

The outline is a decision artifact. It should show enough structure for the user to approve direction without reading full copy.

For PPT image drafts, include page type examples:

- Cover
- Chapter divider
- Big idea
- Problem
- Data/evidence
- Diagram/architecture
- Roadmap
- Risk/decision
- Summary

For HTML, include content form examples:

- Hero
- Narrative section
- KPI band
- Case cards
- Architecture block
- Timeline
- Dashboard/report block
- Closing CTA

## Confirmation Prompt

After the table, ask:

```text
请确认这个大纲是否可以进入逐页/逐屏撰写。也可以直接告诉我想调整的部分：章节顺序、页数、重点、风格强度、受众侧重点或输出格式。
```

Do not continue into full drafting until the user confirms.

## PPT Image Preview Confirmation

After the page-by-page copy and visual prompts are drafted for a PPT image draft, create 5 style preview images with `image_gen` before generating the full set.

Ask:

```text
我先基于你的风格要求生成 5 种视觉预览方向。请确认选择哪一种作为整套 PPT 图片稿的统一风格，也可以告诉我要混合、加强或弱化的地方。
```

Do not generate all page images until the user confirms the preview direction.
