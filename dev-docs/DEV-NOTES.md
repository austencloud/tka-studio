# TKA Development Notes

## Quick Commands

```bash
# Development
npm run dev                    # Start dev server
npm run dev:clean              # Clean build and restart
npm run dev:debug              # Dev server with Node debugger
npm run dev:turbo              # Force rebuild everything

# Testing
npm run test                   # Run unit tests
npm run flows                  # Run E2E flow tests
npm run flows:ui               # E2E tests with UI

# Code Quality
npm run lint                   # Check code style
npm run lint:fix               # Fix code style issues
npm run type-check             # Quick TypeScript check
npm run check                  # Full Svelte + TS check

# Analysis
npm run size                   # Visualize bundle size
npm run update:deps            # Interactive dependency updates

# Build & Deploy
npm run build                  # Production build
npm run preview                # Preview production build
```

## Development Tips

### HMR (Hot Module Replacement)
- **CSS changes**: Instant hot reload with state preservation
- **Component changes**: Fast hot reload (~100-200ms)
- **State file changes**: Full page reload (necessary for stability)

**Known HMR Limitations (Svelte 5):**
- Event handler changes (adding/removing `ontouchstart`, etc.) may require manual reload
- Import removals (removing `import` statements) may not HMR properly
- Binding changes (`bind:this` target changes) can break HMR
- Structural template changes (major DOM restructuring) need reload

**Quick Reload Shortcuts:**
- `Ctrl+Shift+R` - Force hard reload (custom shortcut)
- `window.__TKA_RELOAD()` - Force reload from console
- Standard browser reload also works

### Debugging
1. Use `$inspect(value)` in Svelte components to auto-log reactive changes
2. Press F5 in VS Code to start debugging with Chrome
3. Use Svelte DevTools browser extension for component inspection

### Performance
- Use `npm run size` to check bundle size before committing
- Check browser Performance tab for rendering bottlenecks
- Use `$derived` instead of `$:` for reactive computations in Svelte 5

### Common Issues

**Problem: HMR not working after code changes**
```bash
# Quick fix: Press Ctrl+Shift+R in browser
# Or in browser console:
window.__TKA_RELOAD()

# If that doesn't help, force Vite rebuild:
npm run dev:turbo
```

**Problem: TypeScript errors in editor**
```
Ctrl+Shift+P → "Svelte: Restart Language Server"
```

**Problem: Build artifacts causing issues**
```bash
npm run dev:clean  # Clean everything and restart
```

## Architecture Notes

### Module Structure
- `$lib/modules/build/` - Build module (construct, edit, share)
- `$lib/modules/learn/` - Learn module (drills, tutorials)
- `$lib/modules/explore/` - Explore module (browse, discover)
- `$lib/shared/` - Shared utilities and components

### State Management
- Using Svelte 5 runes (`$state`, `$derived`, `$effect`)
- Critical state files trigger full page reload on change
- Component-local state preferred over global when possible

## VS Code Tips
- Install recommended extensions (Ctrl+Shift+X → "Show Recommended Extensions")
- Use GitLens for powerful Git integration
- `pretty-ts-errors` makes TypeScript errors readable
- `import-cost` shows bundle impact of imports

---

Last updated: $(date)
