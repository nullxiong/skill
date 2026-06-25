# Image Generation Prompting

Use image generation prompts for PPT image drafts, preferring the built-in `image_gen` tool when image creation is available. Write prompts as design direction for a complete slide image, not as generic art prompts.

## Prompt Components

Include:

- Slide purpose and title placement.
- Visual style and mood.
- Composition and hierarchy.
- Background and main visual elements.
- Color palette, lighting, depth, and material texture.
- Text-safe area and empty space for later text overlay.
- Constraints and avoid list.

## Prompt Pattern

```text
Create a 16:9 presentation slide image for [page purpose].
Style: [material-specific visual style].
Composition: [layout, focal point, balance, safe text area].
Background: [scene/texture/space].
Main elements: [objects, diagrams, abstract forms].
Color and lighting: [palette, contrast, glow/shadow].
Text area: leave clean readable space at [position] for title and bullets.
Avoid: small unreadable text, random logos, clutter, distorted UI, excessive decoration.
```

## Five-Style Preview Flow

Before generating all PPT slide images, create 5 style preview images with `image_gen` and ask the user to choose one direction.

Use one representative page for the preview. Prefer the cover, a chapter divider, or the page with the strongest visual metaphor. The 5 previews should share the same topic and copy constraints, but vary the style direction:

1. High-impact cinematic.
2. Premium clean technology.
3. Data/architecture focused.
4. Storytelling and metaphor driven.
5. Minimal executive polish.

After generating the previews, present them as Option 1-5 with concise notes about visual tone, composition, color/lighting, and best-fit use case. Do not generate the full deck images until the user confirms one option or asks for adjustments.

## Chinese Output

When the final slide copy is Chinese, keep prompt instructions in English if image generation performs better, but specify:

```text
Do not render Chinese body text inside the image unless explicitly requested; leave clean space for text overlay.
```

## Conversion Warning

Strong visual pages with complex backgrounds, glow, 3D elements, gradients, and layered compositions usually work best as image-based slides. They may convert poorly to fully editable PPT objects.
