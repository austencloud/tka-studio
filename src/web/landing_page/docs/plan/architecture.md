# 🏗️ Architecture & Directory Structure

## 📁 **V2 Directory Structure**

```
the-kinetic-constructor-web/
├── v1/                                    # Existing app (preserved)
├── v2/                                    # New clean implementation
├── 📁 launcher/                           # Independent version launcher
│   ├── src/
│   │   ├── routes/
│   │   │   ├── +page.svelte              # Launcher dashboard
│   │   │   └── +layout.svelte            # Launcher layout
│   │   ├── lib/
│   │   │   ├── components/
│   │   │   │   ├── VersionCard.svelte
│   │   │   │   ├── VersionManager.svelte
│   │   │   │   ├── DevServerController.svelte
│   │   │   │   ├── VersionComparison.svelte
│   │   │   │   └── PerformanceMonitor.svelte
│   │   │   ├── stores/
│   │   │   │   └── launcher.svelte.ts
│   │   │   ├── services/
│   │   │   │   ├── version-detector.ts
│   │   │   │   ├── dev-server-manager.ts
│   │   │   │   └── port-manager.ts
│   │   │   └── types/
│   │   │       └── launcher.types.ts
│   │   └── app.html
│   ├── package.json
│   ├── vite.config.ts
│   └── README.md
│
├── 📁 v2/core/                            # Main V2 application
│   │   ├── src/
│   │   │   ├── 📁 app/                    # App shell & routing
│   │   │   │   ├── routes/
│   │   │   │   │   ├── +layout.svelte
│   │   │   │   │   ├── +page.svelte
│   │   │   │   │   └── (dashboard)/
│   │   │   │   ├── app.html
│   │   │   │   └── error.html
│   │   │   │
│   │   │   ├── 📁 lib/
│   │   │   │   ├── 📁 core/               # Core business logic
│   │   │   │   │   ├── 📁 pictograph/
│   │   │   │   │   │   ├── engine.svelte.ts
│   │   │   │   │   │   ├── types.ts
│   │   │   │   │   │   └── operations.ts
│   │   │   │   │   ├── 📁 sequence/
│   │   │   │   │   │   ├── manager.svelte.ts
│   │   │   │   │   │   ├── timeline.svelte.ts
│   │   │   │   │   │   └── export.ts
│   │   │   │   │   ├── 📁 canvas/
│   │   │   │   │   │   ├── renderer.svelte.ts
│   │   │   │   │   │   ├── animations.svelte.ts
│   │   │   │   │   │   └── performance.svelte.ts
│   │   │   │   │   └── 📁 settings/
│   │   │   │   │       ├── app-config.svelte.ts
│   │   │   │   │       └── user-prefs.svelte.ts
│   │   │   │   │
│   │   │   │   ├── 📁 ui/                 # UI Components
│   │   │   │   │   ├── 📁 layout/
│   │   │   │   │   │   ├── AppShell.svelte
│   │   │   │   │   │   ├── MainLayout.svelte
│   │   │   │   │   │   └── PanelSystem.svelte
│   │   │   │   │   ├── 📁 workspace/
│   │   │   │   │   │   ├── Canvas.svelte
│   │   │   │   │   │   ├── Timeline.svelte
│   │   │   │   │   │   ├── Toolbox.svelte
│   │   │   │   │   │   └── Properties.svelte
│   │   │   │   │   ├── 📁 backgrounds/
│   │   │   │   │   │   ├── SnowfallCanvas.svelte
│   │   │   │   │   │   ├── NightSkyCanvas.svelte
│   │   │   │   │   │   └── BackgroundEngine.svelte
│   │   │   │   │   ├── 📁 dialogs/
│   │   │   │   │   │   ├── ExportDialog.svelte
│   │   │   │   │   │   ├── SettingsDialog.svelte
│   │   │   │   │   │   └── FirstTimeSetup.svelte
│   │   │   │   │   └── 📁 common/
│   │   │   │   │       ├── Button.svelte
│   │   │   │   │       ├── Modal.svelte
│   │   │   │   │       ├── Loading.svelte
│   │   │   │   │       └── Toast.svelte
│   │   │   │   │
│   │   │   │   ├── 📁 state/              # Pure Runes State
│   │   │   │   │   ├── app.svelte.ts      # Global app state
│   │   │   │   │   ├── workspace.svelte.ts # Workspace state
│   │   │   │   │   ├── canvas.svelte.ts   # Canvas state
│   │   │   │   │   ├── timeline.svelte.ts # Timeline state
│   │   │   │   │   └── ui.svelte.ts       # UI state
│   │   │   │   │
│   │   │   │   ├── 📁 services/           # External integrations
│   │   │   │   │   ├── export-service.ts
│   │   │   │   │   ├── persistence.ts
│   │   │   │   │   ├── analytics.ts
│   │   │   │   │   └── haptics.ts
│   │   │   │   │
│   │   │   │   ├── 📁 utils/              # Pure utilities
│   │   │   │   │   ├── math.ts
│   │   │   │   │   ├── color.ts
│   │   │   │   │   ├── animation.ts
│   │   │   │   │   ├── dom.ts
│   │   │   │   │   └── performance.ts
│   │   │   │   │
│   │   │   │   └── 📁 types/              # TypeScript definitions
│   │   │   │       ├── pictograph.ts
│   │   │   │       ├── sequence.ts
│   │   │   │       ├── canvas.ts
│   │   │   │       ├── ui.ts
│   │   │   │       └── global.d.ts
│   │   │   │
│   │   │   └── tests/                     # Testing
│   │   │       ├── unit/
│   │   │       ├── integration/
│   │   │       └── e2e/
│   │   │
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   ├── tailwind.config.ts
│   │   ├── tsconfig.json
│   │   └── playwright.config.ts
│   │
│   ├── 📁 shared/                         # Shared utilities
│   │   ├── types/
│   │   ├── constants/
│   │   └── utils/
│   │
│   └── 📁 docs/                           # Documentation
│       ├── architecture.md
│       ├── state-management.md
│       ├── component-guide.md
│       └── migration-guide.md
```

---

## 🏗️ **Why Independent Launcher Architecture?**

### **🎯 Clean Separation of Concerns**

```
the-kinetic-constructor-web/
├── v1/           # Legacy (preserved exactly as-is)
├── v2/           # Modern rebuild
├── launcher/     # Version orchestrator
└── shared/       # Common utilities (optional)
```

### **🚀 Key Advantages:**

**1. Future-Proof Scalability**

- ✅ Add V3, V4, experimental branches easily
- ✅ Each version is self-contained
- ✅ Launcher evolves independently

**2. Development Workflow**

- ✅ Build launcher first (Week 1) - immediate value
- ✅ Test launcher with existing V1 right away
- ✅ V2 development doesn't block launcher features
- ✅ Can compare any versions, not just V1 vs V2

**3. Deployment Flexibility**

- ✅ Deploy launcher separately from versions
- ✅ Version-specific deployments and rollbacks
- ✅ A/B testing between versions
- ✅ Independent scaling and optimization

**4. Team Collaboration**

- ✅ Different teams can work on different versions
- ✅ Launcher team can focus on developer experience
- ✅ No cross-version dependencies or conflicts

**5. Maintenance & Updates**

- ✅ Update launcher without touching versions
- ✅ Maintain legacy versions independently
- ✅ Clear ownership boundaries

## 🎯 **Launcher Capabilities (Independent)**

```typescript
interface VersionConfig {
  id: string;
  name: string;
  path: string;
  port: number;
  packageManager: "npm" | "pnpm" | "yarn";
  startCommand: string;
  buildCommand?: string;
  healthCheck: string;
}

export const SUPPORTED_VERSIONS: VersionConfig[] = [
  {
    id: "v1",
    name: "Legacy Version",
    path: "../v1",
    port: 5173,
    packageManager: "npm",
    startCommand: "dev",
    healthCheck: "/api/health",
  },
  {
    id: "v2-core",
    name: "Modern Rebuild",
    path: "../v2/core",
    port: 5174,
    packageManager: "npm",
    startCommand: "dev",
    healthCheck: "/",
  },
];
```

This structure transforms the launcher from a V2 feature into a **development platform** that grows with your project! 🚀

_Last updated: June 11, 2025_
