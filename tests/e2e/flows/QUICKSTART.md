# 🎯 TKA Flows - Quick Start

All 7 critical user flows have been recorded as automated Playwright tests!

## 🚀 Run Flows Instantly

### Using NPM Scripts (Recommended)

```bash
# Run all flows
npm run flows

# Run all flows with visual UI
npm run flows:ui

# Run specific flow
npm run flow:construct
npm run flow:generate
npm run flow:share
npm run flow:advanced
npm run flow:drills
npm run flow:library
npm run flow:pwa
```

### Using the Runner Script

```bash
# Run any flow by name
node flows/run-flow.js construct
node flows/run-flow.js generate
node flows/run-flow.js all

# Add Playwright flags
node flows/run-flow.js construct --headed
node flows/run-flow.js all --debug
```

### Direct Playwright Commands

```bash
npx playwright test flows/1-construct-flow.spec.ts
npx playwright test flows/ --headed
npx playwright test flows/ --ui
```

## 🗣️ Voice Commands for AI Agents

Just tell me (or any AI agent):

- **"Run the construct flow"** → Tests manual sequence building
- **"Run the generate flow"** → Tests auto-generation
- **"Run all flows"** → Full test suite
- **"Run flows in UI mode"** → Watch tests execute visually

## 📋 What's Recorded

| #   | Flow Name             | Description              | File                                     |
| --- | --------------------- | ------------------------ | ---------------------------------------- |
| 1   | **Construct Flow**    | Manual sequence building | `1-construct-flow.spec.ts`               |
| 2   | **Generate Flow**     | Auto-create sequences    | `2-generate-flow.spec.ts`                |
| 3   | **Share/Export Flow** | GIF export functionality | `3-share-export-flow.spec.ts`            |
| 4   | **Advanced Picker**   | All 16 start positions   | `4-advanced-start-position-flow.spec.ts` |
| 5   | **Learn Drills**      | Educational flashcards   | `5-learn-drills-flow.spec.ts`            |
| 6   | **Library Save/Load** | Sequence persistence     | `6-library-save-reload-flow.spec.ts`     |
| 7   | **PWA Install**       | Mobile install prompt    | `7-mobile-pwa-install-flow.spec.ts`      |

## ⚡ Prerequisites

1. **Start your dev server:**

   ```bash
   npm run dev
   ```

   App must be running on `http://localhost:5173`

2. **Playwright already installed** ✅ (already in your package.json)

## 🎬 Next Steps

### 1. Test a Single Flow Right Now

```bash
npm run flow:construct -- --headed
```

This will open a browser and you'll watch the test run!

### 2. Run All Flows to Verify

```bash
npm run flows
```

### 3. Customize Flows

Each `.spec.ts` file is editable. Update selectors if your UI changes:

```typescript
// In any flow file, find and update selectors like:
await page.click('[data-testid="construct-tab"]');
```

### 4. Add to CI/CD

Add to your GitHub Actions or CI pipeline:

```yaml
- name: Run User Flows
  run: npm run flows
```

## 🐛 Troubleshooting

**"Element not found" errors?**

- UI may have changed - update the `data-testid` selectors
- Add `await page.waitForTimeout(1000)` for slower interactions

**App not loading?**

- Verify `npm run dev` is running on port 5173
- Check `http://localhost:5173` in your browser first

**Download tests failing?**

- Downloads work in headed mode: `--headed`
- Check browser permissions

## 💡 Pro Tips

1. **Watch tests run:** Always use `--headed` when developing flows

   ```bash
   npm run flows:headed
   ```

2. **Debug mode:** Step through tests interactively

   ```bash
   npx playwright test flows/1-construct-flow.spec.ts --debug
   ```

3. **Update screenshots:** Flows can capture screenshots for documentation
   ```typescript
   await page.screenshot({ path: "flow-step-1.png" });
   ```

---

**You're all set!** 🎉

These flows now live in your codebase and can be run anytime with simple commands or voice instructions to AI agents.

Generated with ❤️ by Claude Code
