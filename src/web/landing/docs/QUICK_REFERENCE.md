# Quick Reference Guide - Home Page Layout

## Grid System Overview

### Feature Cards Layout

```css
/* Desktop/Tablet: 2x2 Grid */
.features-grid {
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
}

/* Mobile: Single Column */
@media (max-width: 768px) {
  .features-grid {
    grid-template-columns: 1fr;
    grid-template-rows: repeat(4, auto);
  }
}
```

## Dark Mode Implementation

### Key CSS Variables

```css
/* Light Mode */
--surface-color: #ffffff;
--border-color: #e0e0e0;

/* Dark Mode (automatic via prefers-color-scheme) */
--surface-color: #2d2d2d;
--border-color: #404040;
```

### Feature Card Dark Mode

```css
.feature-card {
  background: var(--surface-color); /* Not white! */
  border: 1px solid var(--border-color);
}
```

## Responsive Breakpoints

| Screen Size  | Layout  | Grid               |
| ------------ | ------- | ------------------ |
| ≤768px       | Mobile  | 1 column × 4 rows  |
| 769px-1024px | Tablet  | 2 columns × 2 rows |
| >1024px      | Desktop | 2 columns × 2 rows |

## Background Image

### File Location

- **Path**: `/static/hero-bg.svg`
- **Format**: SVG (scalable, ~3KB)
- **Theme**: Flow arts patterns (poi, staff movements)

### CSS Implementation

```css
.hero-background {
  background-image: url("/hero-bg.svg");
  background-size: cover;
  background-position: center center;
}
```

## Accessibility Features

### ARIA Labels

```html
<div
  class="hero-background"
  role="img"
  aria-label="Abstract flow arts background showing poi and staff movement patterns"
></div>
```

### User Preferences

```css
/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .hero-background {
    transition: none;
  }
}

/* High contrast */
@media (prefers-contrast: high) {
  .feature-card {
    border: 2px solid var(--text-color);
  }
}
```

## Common Modifications

### Changing Background Image

1. Replace `/static/hero-bg.svg` with new image
2. Update `aria-label` to describe new image
3. Test loading performance

### Adjusting Grid Layout

```css
/* For 3-column layout */
.features-grid {
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: auto;
}
```

### Modifying Spacing

```css
/* Increase card spacing */
.features-grid {
  gap: var(--spacing-2xl); /* Instead of var(--spacing-xl) */
}
```

## Troubleshooting

### Common Issues

1. **Cards not equal height**: Ensure `align-items: stretch` on grid
2. **Dark mode not working**: Check CSS custom properties usage
3. **Mobile layout broken**: Verify media query syntax
4. **Background not loading**: Check file path and SVG validity

### Debug Tools

```css
/* Temporary grid visualization */
.features-grid {
  border: 2px solid red;
}
.feature-card {
  border: 1px solid blue;
}
```
