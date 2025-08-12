# 🤖 AI Assistant Context

## 🎯 **CRITICAL: WORKING DIRECTORIES**

When working on different parts of the project, **ALWAYS** specify the exact path:

### 🚀 Launcher Development

- **Path:** `apps/launcher/`
- **Files:** `apps/launcher/src/lib/`
- **Commands:** `cd apps/launcher && npm run dev`
- **Port:** 5175

### 📦 V1 Legacy App

- **Path:** `apps/v1-legacy/`
- **Files:** `apps/v1-legacy/src/lib/`
- **Commands:** `cd apps/v1-legacy && npm run dev`
- **Port:** 5173

### ⚡ V2 Modern App (when created)

- **Path:** `apps/v2-modern/`
- **Files:** `apps/v2-modern/src/lib/`
- **Commands:** `cd apps/v2-modern && npm run dev`
- **Port:** 5174

---

## ❌ **NEVER CREATE FILES IN ROOT**

**DON'T CREATE:**

- `/src/` ❌
- `/lib/` ❌
- `/components/` ❌
- `/stores/` ❌
- `/services/` ❌

**ALWAYS CREATE:**

- `apps/[app-name]/src/lib/components/` ✅
- `apps/[app-name]/src/lib/stores/` ✅
- `apps/[app-name]/src/lib/services/` ✅

---

## 🏗️ **PROJECT STRUCTURE**

```
kinetic-constructor-workspace/
├── apps/
│   ├── launcher/           # Version management dashboard
│   ├── v1-legacy/         # Original app (XState + Redux)
│   └── v2-modern/         # Modern rebuild (Pure Svelte 5)
├── packages/              # Shared packages (future)
├── docs/                  # Documentation
├── package.json           # Workspace root
└── AI_CONTEXT.md         # This file
```

---

## 🎮 **COMMON COMMANDS**

### Start Individual Apps

```bash
npm run launcher    # Start launcher on :5175
npm run v1         # Start V1 legacy on :5173
npm run v2         # Start V2 modern on :5174
```

### Development Workflows

```bash
npm run dev:all        # Start launcher + V1
npm run dev:compare    # Start V1 + V2 for comparison
npm run install:all    # Install deps for all apps
npm run clean         # Clean all node_modules
```

### App-Specific Commands

```bash
cd apps/launcher && npm run dev
cd apps/v1-legacy && npm run dev
cd apps/v2-modern && npm run dev
```

---

## 🎯 **ARCHITECTURE PRINCIPLES**

### 🚀 **Launcher App**

- **Purpose:** Version management dashboard
- **Tech:** Pure Svelte 5 runes, SvelteKit, TypeScript
- **Features:** Start/stop versions, performance monitoring, comparison
- **Independence:** No dependencies on V1 or V2

### 📦 **V1 Legacy**

- **Purpose:** Original app preservation
- **Tech:** Svelte 5 + XState + Redux (technical debt)
- **Status:** Frozen - no new features, bug fixes only
- **Migration:** Projects can be migrated to V2

### ⚡ **V2 Modern**

- **Purpose:** Clean rebuild with zero technical debt
- **Tech:** Pure Svelte 5 runes, modern patterns
- **Features:** All V1 features + new capabilities
- **Performance:** 60fps target, optimized bundle

---

## 🔧 **DEVELOPMENT GUIDELINES**

### When Working on Launcher:

1. Always use `cd apps/launcher`
2. Files go in `apps/launcher/src/lib/`
3. Use pure Svelte 5 runes (no stores)
4. TypeScript strict mode

### When Working on V1:

1. Always use `cd apps/v1-legacy`
2. Files go in `apps/v1-legacy/src/lib/`
3. Preserve existing patterns (XState/Redux)
4. Bug fixes only, no new features

### When Working on V2:

1. Always use `cd apps/v2-modern`
2. Files go in `apps/v2-modern/src/lib/`
3. Pure Svelte 5 runes only
4. Modern TypeScript patterns

---

## 🚨 **SPATIAL CONFUSION PREVENTION**

### Before Creating Files:

1. **Check current directory:** `pwd`
2. **Navigate to correct app:** `cd apps/[app-name]`
3. **Verify structure:** `ls -la src/lib/`
4. **Create files in correct location**

### File Creation Examples:

```bash
# ✅ CORRECT
apps/launcher/src/lib/components/VersionCard.svelte
apps/v1-legacy/src/lib/stores/pictograph.store.ts
apps/v2-modern/src/lib/services/animation.service.ts

# ❌ WRONG
src/lib/components/VersionCard.svelte
lib/stores/pictograph.store.ts
components/VersionCard.svelte
```

---

## 📋 **CURRENT STATUS**

### ✅ **Completed**

- [x] Clean workspace structure created
- [x] Launcher app functional on :5175
- [x] V1 legacy preserved in apps/v1-legacy
- [x] Root package.json with workspace commands
- [x] AI guidance documentation

### 🔄 **In Progress**

- [ ] V2 modern app creation
- [ ] Enhanced launcher features
- [ ] Version comparison tools

### 📅 **Next Steps**

1. Create V2 modern app structure
2. Implement launcher version detection
3. Add performance monitoring
4. Build comparison dashboard

---

## 🎯 **SUCCESS METRICS**

### Immediate Goals:

- ✅ No more AI spatial confusion
- ✅ Clean separation between versions
- ✅ One-command version switching
- ✅ Professional development setup

### Long-term Vision:

- 🚀 Side-by-side version comparison
- 📊 Real-time performance monitoring
- 🔄 Seamless project migration V1→V2
- ⚡ 60fps V2 performance target

---

**Remember: When in doubt, check `pwd` and navigate to the correct `apps/[app-name]/` directory!** 🎯
