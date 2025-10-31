# TKA Persistence Layer with Dexie.js

This document explains how the TKA app uses Dexie.js for robust, enterprise-grade data persistence.

## 🎯 What is Dexie?

**Dexie.js** is the industry-standard wrapper for IndexedDB. It's used by companies like:

- **Notion** (for offline document storage)
- **WhatsApp Web** (for message persistence)
- **Discord** (for chat history)
- **1.5+ million weekly downloads** on npm

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Svelte Components                   │
├─────────────────────────────────────────────────────────────┤
│                  IPersistenceService                        │
│                 (Service Interface)                         │
├─────────────────────────────────────────────────────────────┤
│               DexiePersistenceService                       │
│                (Business Logic)                             │
├─────────────────────────────────────────────────────────────┤
│                   TKADatabase                               │
│                 (Dexie Schema)                              │
├─────────────────────────────────────────────────────────────┤
│                    IndexedDB                                │
│                 (Browser Database)                          │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Database Schema

Your TKA database has these tables:

### **sequences** - Your sequence data

- **Primary Key**: `id` (string)
- **Indexes**: `name`, `word`, `author`, `dateAdded`, `level`, `isFavorite`, `difficultyLevel`, `tags`
- **Data**: Complete `SequenceData` objects

### **pictographs** - Pictograph library

- **Primary Key**: `id` (string)
- **Indexes**: `letter`, `startPosition`, `endPosition`
- **Data**: Complete `PictographData` objects

### **userWork** - Tab states and work-in-progress

- **Primary Key**: `id` (auto-increment)
- **Indexes**: `type`, `tabId`, `userId`, `lastModified`
- **Data**: Flexible storage for any tab state

### **userProjects** - User project collections

- **Primary Key**: `id` (auto-increment)
- **Indexes**: `name`, `userId`, `createdAt`, `lastModified`, `isPublic`, `tags`
- **Data**: Project metadata and sequence references

### **settings** - App settings

- **Primary Key**: `id` (string)
- **Data**: Complete `AppSettings` objects

## 🚀 How to Use in Your Components

### **1. Basic Service Injection**

```typescript
// In any Svelte component
import { resolve, TYPES } from "$shared";
import type { IPersistenceService } from "$shared";

const persistenceService = resolve(
  TYPES.IPersistenceService
) as IPersistenceService;
```

### **2. Save/Load Sequences**

```typescript
// Save a sequence
await persistenceService.saveSequence(mySequence);

// Load a sequence
const sequence = await persistenceService.loadSequence("sequence-id");

// Get all sequences
const allSequences = await persistenceService.getAllSequences();

// Search sequences
const results = await persistenceService.searchSequences("dance");
```

### **3. Tab State Persistence**

```typescript
// Save current tab
await persistenceService.saveActiveTab("browse");

// Restore last tab
const lastTab = await persistenceService.getActiveTab();

// Save tab-specific state
await persistenceService.saveTabState("browse", {
  filter: "difficulty",
  sortBy: "name",
  scrollPosition: 1250,
});

// Load tab state
const browseState = await persistenceService.loadTabState("browse");
```

### **4. Explore State (Complex Example)**

```typescript
// Save complete Explore state
const ExploreState: CompleteExploreState = {
  filter: { startingLetter: "A", difficulty: "beginner" },
  sort: { method: "name_asc", direction: "asc", appliedAt: new Date() },
  view: { mode: "grid", itemsPerPage: 20 },
  scroll: { position: 1250, lastScrollTime: new Date() },
  selection: { selectedSequenceId: "seq-123" },
  lastUpdated: new Date(),
  version: 1,
};

await persistenceService.saveExploreState(ExploreState);

// Load it back
const restored = await persistenceService.loadExploreState();
```

## 🔧 Initialization

### **App Startup**

Add this to your main app initialization:

```typescript
// In your main app component or initialization
import { resolve, TYPES } from "$shared";
import type { IPersistenceInitializationService } from "$shared";

const initService = resolve(TYPES.IPersistenceInitializationService);

onMount(async () => {
  try {
    await initService.initialize();
    console.log("✅ Persistence ready");
  } catch (error) {
    console.error("❌ Persistence failed:", error);
  }
});
```

## 🛠️ Advanced Features

### **Filtering and Queries**

```typescript
// Get sequences by specific criteria
const favoriteSequences = await persistenceService.getAllSequences({
  isFavorite: true,
});

const beginnerSequences = await persistenceService.getAllSequences({
  level: 1,
});

const authorSequences = await persistenceService.getAllSequences({
  author: "John Doe",
});
```

### **Backup and Export**

```typescript
// Export all data for backup
const backup = await persistenceService.exportAllData();

// Save to file
const blob = new Blob([JSON.stringify(backup, null, 2)], {
  type: "application/json",
});
const url = URL.createObjectURL(blob);
// ... download logic
```

### **Storage Information**

```typescript
// Get storage statistics
const info = await persistenceService.getStorageInfo();
console.log(`You have ${info.sequences} sequences stored`);
```

## 🔍 Debugging

### **Database Inspector**

Open browser DevTools → Application → Storage → IndexedDB → TKADatabase

You can see all your tables and data directly in the browser.

### **Console Commands**

```javascript
// In browser console
import { db } from "/src/lib/shared/persistence/database/TKADatabase.js";

// See all sequences
await db.sequences.toArray();

// Count records
await db.sequences.count();

// Clear everything (careful!)
await db.delete();
```

## 🚨 Important Notes

### **Transaction Safety**

Dexie automatically handles transactions. Don't worry about database locking or corruption.

### **Offline First**

IndexedDB works completely offline. Your app will work without internet.

### **Storage Limits**

- **Chrome**: ~80% of available disk space
- **Firefox**: ~50% of available disk space
- **Safari**: ~1GB limit

### **Data Migration**

When you need to change the database schema:

```typescript
// In TKADatabase.ts
this.version(2)
  .stores({
    // New schema
  })
  .upgrade((tx) => {
    // Migration logic
  });
```

## 📚 Next Steps

1. **Start Simple**: Use tab persistence first
2. **Add Sequences**: Save/load your sequence data
3. **Complex State**: Add Explore state persistence
4. **User Projects**: Implement project collections
5. **Backup/Sync**: Add export/import features

## 🆘 Troubleshooting

**"Database not initialized"**

- Make sure you call `initService.initialize()` on app startup

**"Service not found"**

- Check that `DexiePersistenceService` is bound in your InversifyJS container

**"Data not persisting"**

- Check browser DevTools → Console for errors
- Verify IndexedDB is enabled in browser settings

**"Performance issues"**

- Use indexes for frequently queried fields
- Avoid storing huge objects (>1MB per record)

---

**🎉 You now have enterprise-grade persistence in your TKA app!**
