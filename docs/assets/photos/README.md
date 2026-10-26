# Public Website Photos

Store public images for your homepage, profile, semester milestones, and research showcase in this folder.

### Recommended Dimensions & Formats
- **Profile Photo**: 400x400 to 800x800 square (`.jpg` or `.png`)
- **Semester & Showcase Images**: 16:9 or 4:3 aspect ratio (e.g. 800x450 or 800x600)
- **Max file size**: Under 2 MB per image for fast loading.

### How to use in `docs/index.md`
```html
<img src="{{ '/assets/photos/your-image.png' | relative_url }}" alt="Description">
```

> **Privacy reminder**: Only place images here that are approved for public viewing on GitHub Pages. Private meeting figures belong in `meetings/assets/` (outside `docs/`).
