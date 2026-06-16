# Image2 Prompting

Use image2 prompts for PPT image drafts. Write prompts as design direction for a complete slide image, not as generic art prompts.

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

## Chinese Output

When the final slide copy is Chinese, keep prompt instructions in English if image generation performs better, but specify:

```text
Do not render Chinese body text inside the image unless explicitly requested; leave clean space for text overlay.
```

## Conversion Warning

Strong visual pages with complex backgrounds, glow, 3D elements, gradients, and layered compositions usually work best as image-based slides. They may convert poorly to fully editable PPT objects.
