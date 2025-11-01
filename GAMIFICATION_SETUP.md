# 🎮 TKA Gamification System - Setup Guide

Welcome! You now have a **complete, production-ready gamification system** with Firebase/Firestore integration! 🚀

## 🌟 What You Got

### ✅ Complete Backend Services
- **AchievementService** - XP tracking, achievement unlocking, progress monitoring
- **DailyChallengeService** - Algorithmic challenge generation with difficulty tiers
- **StreakService** - Daily login tracking with streak calculations
- **NotificationService** - Toast notifications for unlocks and milestones

### ✅ Beautiful UI Components
- **GamificationButton** - Animated XP progress ring in the header
- **AchievementsPanel** - Full-screen modal with stats, challenges, and achievements
- **AchievementNotificationToast** - Animated toast notifications
- **Svelte 5 Runes State** - Reactive state management

### ✅ Firebase/Firestore Integration
- Firestore collections for persistent data
- Offline support with IndexedDB caching
- Multi-device sync
- Optimistic updates for instant UI feedback

### ✅ 25+ Achievements Across 5 Categories
- 🎨 Creator (building sequences)
- 📚 Scholar (learning concepts)
- 💪 Practitioner (daily streaks)
- 🔍 Explorer (browsing gallery)
- 🎥 Performer (future: video submissions)

---

## 🚀 Quick Start

### 1. Add Gamification Button to Navigation

Edit `src/lib/shared/navigation/components/NavigationBar.svelte`:

```svelte
<script lang="ts">
  import GamificationButton from "../../gamification/components/GamificationButton.svelte";
  import AchievementsPanel from "../../gamification/components/AchievementsPanel.svelte";

  let showAchievementsPanel = $state(false);
</script>

<nav class="app-navigation-bar">
  <!-- Left: Hamburger Menu + Gamification Button -->
  <div class="nav-left">
    <ModuleMenuSection ... />

    <!-- 🎮 NEW: Gamification Button -->
    <GamificationButton onclick={() => showAchievementsPanel = true} />
  </div>

  ...
</nav>

<!-- 🎮 NEW: Achievements Panel -->
<AchievementsPanel
  isOpen={showAchievementsPanel}
  onClose={() => showAchievementsPanel = false}
/>
```

### 2. Add Notification Toast to Main App

Edit `src/lib/shared/application/components/MainApplication.svelte`:

```svelte
<script lang="ts">
  import AchievementNotificationToast from "../../gamification/components/AchievementNotificationToast.svelte";
</script>

<div class="main-interface">
  <!-- Your existing layout -->
  ...

  <!-- 🎮 NEW: Achievement Notifications -->
  <AchievementNotificationToast />
</div>
```

### 3. Track XP in Your Modules

#### Build Module (Sequence Creation)
```typescript
import { resolve, TYPES } from "$shared/inversify";
import type { IAchievementService } from "$shared/gamification/services/contracts";

// In your sequence creation function:
async function handleSequenceCreated(sequence: SequenceData) {
  // Your existing logic...

  // Track XP
  const achievementService = await resolve<IAchievementService>(TYPES.IAchievementService);
  await achievementService.trackAction("sequence_created", {
    beatCount: sequence.beats.length,
    letters: sequence.word.split('')
  });
}
```

#### Learn Module (Concept Completion)
```typescript
async function handleConceptCompleted(conceptId: string) {
  // Your existing logic...

  // Track XP
  const achievementService = await resolve<IAchievementService>(TYPES.IAchievementService);
  await achievementService.trackAction("concept_learned", {
    conceptId
  });
}
```

#### Explore Module (Sequence Viewed)
```typescript
async function handleSequenceViewed(sequenceId: string) {
  // Your existing logic...

  // Track XP
  const achievementService = await resolve<IAchievementService>(TYPES.IAchievementService);
  await achievementService.trackAction("sequence_explored", {
    sequenceId
  });
}
```

### 4. Initialize Gamification on App Start

Add to your app initialization (`src/lib/shared/application/state/app-state.svelte.ts` or similar):

```typescript
import { resolve, TYPES } from "$shared/inversify";
import type {
  IAchievementService,
  IDailyChallengeService,
  IStreakService,
} from "$shared/gamification/services/contracts";

export async function initializeGamificationSystem(): Promise<void> {
  try {
    const [achievementService, challengeService, streakService] = await Promise.all([
      resolve<IAchievementService>(TYPES.IAchievementService),
      resolve<IDailyChallengeService>(TYPES.IDailyChallengeService),
      resolve<IStreakService>(TYPES.IStreakService),
    ]);

    // Initialize services
    await Promise.all([
      achievementService.initialize(),
      challengeService.initialize(),
      streakService.initialize(),
    ]);

    // Record daily activity (for streaks)
    await streakService.recordDailyActivity();

    console.log("✅ Gamification system initialized");
  } catch (error) {
    console.error("❌ Gamification initialization failed:", error);
    // Don't block app if gamification fails
  }
}
```

---

## 🔥 Firestore Setup

### 1. Deploy Security Rules

Create `firestore.rules` in your project root:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // User data - users can only access their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;

      // Achievements
      match /achievements/{achievementId} {
        allow read, write: if request.auth != null && request.auth.uid == userId;
      }

      // XP
      match /xp/{xpId} {
        allow read, write: if request.auth != null && request.auth.uid == userId;
      }

      // XP Events
      match /xpEvents/{eventId} {
        allow read, write: if request.auth != null && request.auth.uid == userId;
      }

      // Challenge Progress
      match /challengeProgress/{progressId} {
        allow read, write: if request.auth != null && request.auth.uid == userId;
      }

      // Streak
      match /streak/{streakId} {
        allow read, write: if request.auth != null && request.auth.uid == userId;
      }

      // Notifications
      match /notifications/{notificationId} {
        allow read, write: if request.auth != null && request.auth.uid == userId;
      }
    }

    // Daily Challenges - global, read-only
    match /dailyChallenges/{challengeId} {
      allow read: if request.auth != null;
      allow write: if false; // Server-side only
    }
  }
}
```

Deploy to Firebase:
```bash
firebase deploy --only firestore:rules
```

### 2. Create Firestore Indexes

The app will auto-create these, but you can manually create them for better performance:

```bash
# In Firebase Console > Firestore > Indexes, create:

Collection: users/{userId}/achievements
Fields: isCompleted (Ascending), unlockedAt (Descending)

Collection: users/{userId}/notifications
Fields: isRead (Ascending), timestamp (Descending)

Collection: dailyChallenges
Fields: date (Ascending), expiresAt (Ascending)
```

---

## 🎯 Daily Challenge System

### How it Works

1. **Algorithmic Generation**: Challenges are deterministically generated based on the date (same challenge for all users on a given day)
2. **Difficulty Tiers**: Beginner, Intermediate, Advanced
3. **Auto-Progress Tracking**: Progress updates automatically as users complete actions
4. **XP Rewards**: Completing challenges awards bonus XP

### Challenge Types

- **build_sequence**: Create X sequences
- **sequence_length**: Create sequence with X+ beats
- **use_letters**: Create sequence with specific letters
- **complete_concept**: Complete X concepts
- **explore_gallery**: View X sequences
- **generation_challenge**: Generate X sequences

### Adding Custom Challenges

Edit `src/lib/shared/gamification/services/implementations/DailyChallengeService.ts`:

```typescript
const CHALLENGE_TEMPLATES: Array<{...}> = [
  {
    type: "use_letters",
    difficulty: "intermediate",
    title: "Spell HELLO",
    description: "Create a sequence using H-E-L-L-O",
    xpReward: 125,
    target: 1,
    metadata: { requiredLetters: ["H", "E", "L", "L", "O"] },
  },
  // Add your custom challenges here!
];
```

---

## 🏆 Achievement System

### Categories & Icons

- 🎨 **Creator**: Sequence building achievements
- 📚 **Scholar**: Learning achievements
- 💪 **Practitioner**: Streak achievements
- 🔍 **Explorer**: Gallery exploration achievements
- 🎥 **Performer**: Video submission achievements (Phase 3)

### Tiers & Rewards

- 🥉 **Bronze**: 25-75 XP
- 🥈 **Silver**: 50-150 XP
- 🥇 **Gold**: 100-300 XP
- 💎 **Platinum**: 250-1000 XP

### Adding Custom Achievements

Edit `src/lib/shared/gamification/domain/constants/achievement-definitions.ts`:

```typescript
const CREATOR_ACHIEVEMENTS: Achievement[] = [
  // Add your custom achievement here
  {
    id: "my_custom_achievement",
    title: "My Achievement",
    description: "Do something awesome!",
    category: "creator",
    tier: "gold",
    xpReward: 200,
    icon: "🎉",
    requirement: {
      type: "sequence_count",
      target: 100,
    },
  },
];
```

---

## 📊 XP & Leveling System

### XP Formula

- **Level 1 → 2**: 100 XP
- **Level 2 → 3**: 150 XP
- **Level 3 → 4**: 210 XP
- **Level 10**: ~750 XP
- **Level 20**: ~2000 XP
- **Formula**: `baseXP * (level ^ 1.5)`

### Milestone Levels

- **Level 5**: Beginner Flow Artist 🌱
- **Level 10**: Intermediate Practitioner 🌿
- **Level 20**: Advanced Flow Artist 🌳
- **Level 30**: Expert Choreographer 🎯
- **Level 50**: Master of Movement 👑
- **Level 100**: TKA Grandmaster 💎

### XP Rewards by Action

```typescript
SEQUENCE_CREATED: 10 XP
SEQUENCE_GENERATED: 5 XP
CONCEPT_LEARNED: 20 XP
DRILL_COMPLETED: 5 XP
SEQUENCE_EXPLORED: 2 XP
DAILY_LOGIN: 15 XP
DAILY_CHALLENGE_COMPLETED: 50 XP
ACHIEVEMENT_UNLOCKED: 25-250 XP (varies by tier)
```

---

## 🔧 Testing & Debugging

### Manual XP Award (for testing)
```typescript
const achievementService = await resolve<IAchievementService>(TYPES.IAchievementService);
await achievementService.awardXP(1000, "Testing XP system");
```

### Check Gamification Stats
```typescript
const stats = await achievementService.getStats();
console.log(stats);
// { totalXP, currentLevel, achievementsUnlocked, totalAchievements, completionPercentage }
```

### Database Info
```typescript
import { getDatabaseInfo } from "$shared/persistence/database/TKADatabase";
const info = await getDatabaseInfo();
console.log(info); // Shows counts for all tables including gamification
```

---

## 🎨 Customization

### Changing Colors/Themes

Edit the gradient in `GamificationButton.svelte`:
```svelte
<linearGradient id="xp-gradient">
  <stop offset="0%" style="stop-color:#YOUR_COLOR_1" />
  <stop offset="100%" style="stop-color:#YOUR_COLOR_2" />
</linearGradient>
```

### Changing Animation Durations

Edit transition timing in components:
```css
.gamification-button {
  transition: all 0.3s ease; /* Adjust this */
}
```

---

## 🚨 Troubleshooting

### "Container not initialized" Error
Make sure gamification services are initialized after the DI container:
```typescript
await ensureContainerInitialized();
await initializeGamificationSystem();
```

### No XP Tracking
Check that:
1. User is authenticated (`auth.currentUser` exists)
2. Services are initialized
3. You're calling `trackAction()` with correct action types

### Notifications Not Showing
1. Check that `AchievementNotificationToast` is mounted in MainApplication
2. Verify notification state is properly imported
3. Check console for errors

### Firestore Permission Denied
1. Deploy security rules: `firebase deploy --only firestore:rules`
2. Ensure user is authenticated
3. Check userId matches `request.auth.uid`

---

## 📦 What's Next?

### Phase 2: Enhanced Challenges
- [ ] User-selectable challenge difficulty
- [ ] Challenge streaks
- [ ] Weekly challenge rotation
- [ ] Leaderboards

### Phase 3: Social Features
- [ ] Video submissions
- [ ] Community challenges
- [ ] User profiles
- [ ] Achievement sharing

### Phase 4: Advanced Gamification
- [ ] XP multipliers (weekend bonus, streak bonus)
- [ ] Seasonal events
- [ ] Limited-time achievements
- [ ] Achievement badges/flair

---

## 🎉 You're Done!

Your gamification system is **fully operational**! Users can now:

✅ Earn XP from all activities
✅ Unlock 25+ achievements
✅ Complete daily challenges
✅ Build daily streaks
✅ Level up with milestones
✅ See beautiful notifications
✅ Track progress across devices

**Enjoy the engagement boost!** 🚀🎮

---

## 📞 Support

If you have questions or run into issues:
1. Check the console for detailed error messages
2. Verify Firebase configuration in `.env`
3. Check Firestore security rules
4. Review service initialization order

**Happy gamifying!** 🎮✨
