# Phase 2: User-Generated Content & Social Features

Now that authentication is set up, here's the roadmap for maximizing user engagement through personalized content, favorites, collections, and social features.

## Overview

Transform TKA from a sequence explorer into a **social platform** where users can:

- Save favorite sequences
- Create personal collections
- Rate and review sequences
- Build public profiles
- Share their work
- Discover content from other users

## Architecture Overview

### Data Structure (Firestore)

```
firestore/
├── users/
│   └── {userId}/
│       ├── profile (document)
│       │   ├── displayName
│       │   ├── photoURL
│       │   ├── bio
│       │   ├── createdAt
│       │   ├── stats { sequences, favorites, followers }
│       │   └── isPublic
│       │
│       ├── favorites/ (subcollection)
│       │   └── {sequenceId}/
│       │       ├── sequenceId
│       │       ├── savedAt
│       │       └── notes (optional)
│       │
│       ├── collections/ (subcollection)
│       │   └── {collectionId}/
│       │       ├── name
│       │       ├── description
│       │       ├── isPublic
│       │       ├── createdAt
│       │       ├── updatedAt
│       │       └── sequenceIds[]
│       │
│       └── sequences/ (subcollection)
│           └── {sequenceId}/
│               ├── sequenceData
│               ├── createdAt
│               ├── isPublic
│               ├── views
│               └── likes
│
├── sequences/
│   └── {sequenceId}/
│       ├── authorId
│       ├── authorName
│       ├── metadata (from PNG)
│       ├── stats { views, favorites, rating }
│       ├── createdAt
│       └── isPublic
│
├── ratings/
│   └── {sequenceId}/
│       └── {userId}/
│           ├── rating (1-5)
│           ├── review (optional)
│           └── createdAt
│
└── social/
    └── followers/
        └── {userId}/
            └── {followerId}/ (document)
                └── followedAt
```

## Phase 2A: Favorites System (Week 1-2)

### Features

1. **Heart Button** on each sequence
2. **My Favorites** section in Explore
3. **Quick access** to saved sequences
4. **Sync across devices**

### Implementation

```typescript
// src/lib/shared/user-content/services/FavoritesService.ts
import {
  doc,
  setDoc,
  deleteDoc,
  collection,
  query,
  where,
} from "firebase/firestore";
import { db } from "$shared/auth";

export class FavoritesService {
  async addFavorite(userId: string, sequenceId: string) {
    const favoriteRef = doc(db, `users/${userId}/favorites/${sequenceId}`);
    await setDoc(favoriteRef, {
      sequenceId,
      savedAt: new Date().toISOString(),
    });
  }

  async removeFavorite(userId: string, sequenceId: string) {
    const favoriteRef = doc(db, `users/${userId}/favorites/${sequenceId}`);
    await deleteDoc(favoriteRef);
  }

  async getFavorites(userId: string) {
    const favoritesRef = collection(db, `users/${userId}/favorites`);
    const snapshot = await getDocs(favoritesRef);
    return snapshot.docs.map((doc) => doc.data());
  }

  async isFavorited(userId: string, sequenceId: string) {
    const favoriteRef = doc(db, `users/${userId}/favorites/${sequenceId}`);
    const snapshot = await getDoc(favoriteRef);
    return snapshot.exists();
  }
}
```

### UI Component

```svelte
<!-- FavoriteButton.svelte -->
<script lang="ts">
  import { user } from "$shared/auth";
  import { favoritesService } from "$shared/user-content";

  let { sequenceId }: { sequenceId: string } = $props();

  let isFavorited = $state(false);
  let loading = $state(false);

  async function toggleFavorite() {
    if (!$user) {
      goto("/auth/login");
      return;
    }

    loading = true;

    try {
      if (isFavorited) {
        await favoritesService.removeFavorite($user.uid, sequenceId);
        isFavorited = false;
      } else {
        await favoritesService.addFavorite($user.uid, sequenceId);
        isFavorited = true;
      }
    } catch (error) {
      console.error("Favorite error:", error);
    } finally {
      loading = false;
    }
  }

  // Check if favorited on mount
  $effect(() => {
    if ($user) {
      favoritesService
        .isFavorited($user.uid, sequenceId)
        .then((result) => (isFavorited = result));
    }
  });
</script>

<button
  onclick={toggleFavorite}
  disabled={loading}
  class="favorite-button"
  class:active={isFavorited}
  aria-label={isFavorited ? "Remove from favorites" : "Add to favorites"}
>
  <svg><!-- Heart icon --></svg>
</button>
```

### Integration Points

- Add to: `OptimizedGalleryGrid.svelte`
- Add to: `SequenceDisplayPanel.svelte`
- New route: `/gallery/favorites`

## Phase 2B: User Profiles (Week 3-4)

### Features

1. **Public profile pages** (`/users/{username}`)
2. **Profile editing** (`/settings/profile`)
3. **User statistics** (sequences created, favorites, etc.)
4. **Profile pictures** (from social login or upload)
5. **Bio and links**

### User Profile Schema

```typescript
export interface UserProfile {
  userId: string;
  username: string; // Unique username for URLs
  displayName: string;
  photoURL: string | null;
  bio: string;
  website: string | null;
  location: string | null;

  stats: {
    sequencesCreated: number;
    favoriteCount: number;
    followerCount: number;
    followingCount: number;
  };

  preferences: {
    profileVisibility: "public" | "private";
    showFavorites: boolean;
    showCollections: boolean;
  };

  createdAt: string;
  updatedAt: string;
}
```

### Implementation

```typescript
// UserProfileService.ts
export class UserProfileService {
  async createProfile(userId: string, data: Partial<UserProfile>) {
    const profileRef = doc(db, `users/${userId}/profile/main`);
    await setDoc(profileRef, {
      userId,
      ...data,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    });
  }

  async getProfile(userId: string): Promise<UserProfile | null> {
    const profileRef = doc(db, `users/${userId}/profile/main`);
    const snapshot = await getDoc(profileRef);
    return snapshot.exists() ? (snapshot.data() as UserProfile) : null;
  }

  async updateProfile(userId: string, updates: Partial<UserProfile>) {
    const profileRef = doc(db, `users/${userId}/profile/main`);
    await updateDoc(profileRef, {
      ...updates,
      updatedAt: new Date().toISOString(),
    });
  }

  async getUserByUsername(username: string): Promise<UserProfile | null> {
    const usersRef = collection(db, "users");
    const q = query(usersRef, where("username", "==", username));
    const snapshot = await getDocs(q);

    if (snapshot.empty) return null;
    return snapshot.docs[0].data() as UserProfile;
  }
}
```

### UI Components

**Profile Page** (`/users/[username]/+page.svelte`):

```svelte
<script lang="ts">
  import { page } from "$app/stores";
  import { userProfileService } from "$shared/user-content";

  let profile = $state<UserProfile | null>(null);
  let loading = $state(true);

  $effect(() => {
    const username = $page.params.username;
    userProfileService.getUserByUsername(username).then((data) => {
      profile = data;
      loading = false;
    });
  });
</script>

{#if loading}
  <div class="loading">Loading profile...</div>
{:else if profile}
  <div class="profile-page">
    <div class="profile-header">
      <img src={profile.photoURL} alt={profile.displayName} />
      <h1>{profile.displayName}</h1>
      <p class="username">@{profile.username}</p>
      <p class="bio">{profile.bio}</p>
    </div>

    <div class="profile-stats">
      <div class="stat">
        <span class="stat-value">{profile.stats.sequencesCreated}</span>
        <span class="stat-label">Sequences</span>
      </div>
      <div class="stat">
        <span class="stat-value">{profile.stats.favoriteCount}</span>
        <span class="stat-label">Favorites</span>
      </div>
      <div class="stat">
        <span class="stat-value">{profile.stats.followerCount}</span>
        <span class="stat-label">Followers</span>
      </div>
    </div>

    <!-- User's sequences, favorites, collections tabs -->
  </div>
{/if}
```

## Phase 2C: Collections (Week 5-6)

### Features

1. **Create collections** of sequences
2. **Organize favorites** into collections
3. **Share collections** with others
4. **Public/private** collections

### Collection Schema

```typescript
export interface Collection {
  id: string;
  userId: string;
  name: string;
  description: string;
  sequenceIds: string[];

  metadata: {
    coverImage: string; // First sequence thumbnail
    sequenceCount: number;
  };

  visibility: "public" | "private" | "unlisted";

  createdAt: string;
  updatedAt: string;
}
```

### UI Flow

1. **In Explore**: "Add to Collection" button on each sequence
2. **Collections Page**: Grid of user's collections
3. **Collection Detail**: View all sequences in a collection
4. **Collection Editor**: Drag-and-drop reordering

## Phase 2D: Ratings & Reviews (Week 7)

### Features

1. **5-star rating** system
2. **Written reviews** (optional)
3. **Average rating** display
4. **Filter by rating** in Explore

### Schema

```typescript
export interface SequenceRating {
  sequenceId: string;
  userId: string;
  rating: 1 | 2 | 3 | 4 | 5;
  review?: string;
  createdAt: string;
  updatedAt: string;
}

export interface SequenceStats {
  sequenceId: string;
  averageRating: number;
  ratingCount: number;
  ratingDistribution: {
    5: number;
    4: number;
    3: number;
    2: number;
    1: number;
  };
}
```

### Implementation

```typescript
// RatingService.ts
export class RatingService {
  async rateSequence(
    sequenceId: string,
    userId: string,
    rating: number,
    review?: string
  ) {
    const ratingRef = doc(db, `ratings/${sequenceId}/${userId}`);

    await setDoc(ratingRef, {
      rating,
      review,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    });

    // Update sequence stats
    await this.updateSequenceStats(sequenceId);
  }

  async updateSequenceStats(sequenceId: string) {
    const ratingsRef = collection(db, `ratings/${sequenceId}`);
    const snapshot = await getDocs(ratingsRef);

    const ratings = snapshot.docs.map((doc) => doc.data().rating);
    const average = ratings.reduce((a, b) => a + b, 0) / ratings.length;

    const distribution = {
      5: ratings.filter((r) => r === 5).length,
      4: ratings.filter((r) => r === 4).length,
      3: ratings.filter((r) => r === 3).length,
      2: ratings.filter((r) => r === 2).length,
      1: ratings.filter((r) => r === 1).length,
    };

    const statsRef = doc(db, `sequences/${sequenceId}/stats`);
    await setDoc(statsRef, {
      averageRating: average,
      ratingCount: ratings.length,
      ratingDistribution: distribution,
    });
  }
}
```

## Phase 2E: Social Features (Week 8-9)

### Features

1. **Follow users**
2. **Activity feed** (following tab)
3. **Comments** on sequences
4. **Share** functionality

### Follow System

```typescript
export class SocialService {
  async followUser(followerId: string, followedId: string) {
    const followRef = doc(db, `social/followers/${followedId}/${followerId}`);
    await setDoc(followRef, {
      followedAt: new Date().toISOString(),
    });

    // Update stats
    await this.incrementFollowerCount(followedId);
    await this.incrementFollowingCount(followerId);
  }

  async unfollowUser(followerId: string, followedId: string) {
    const followRef = doc(db, `social/followers/${followedId}/${followerId}`);
    await deleteDoc(followRef);

    await this.decrementFollowerCount(followedId);
    await this.decrementFollowingCount(followerId);
  }

  async getFollowers(userId: string) {
    const followersRef = collection(db, `social/followers/${userId}`);
    const snapshot = await getDocs(followersRef);
    return snapshot.docs.map((doc) => doc.id);
  }
}
```

## Integration with Existing Explore Module

### Updates Needed

1. **OptimizedGalleryGrid.svelte**
   - Add `<FavoriteButton>` to each sequence card
   - Add `<RatingDisplay>` showing average rating
   - Add "By @username" attribution

2. **SequenceDisplayPanel.svelte**
   - Add favorite button
   - Add rating component
   - Add "View author profile" link
   - Add "Add to collection" button

3. **FilterPanel.svelte**
   - Add "My Favorites" filter
   - Add "My Collections" filter
   - Add "Rating" filter (4+ stars, 3+ stars, etc.)
   - Add "By User" filter

4. **New Components**
   ```
   src/lib/modules/explore/user-content/
   ├── components/
   │   ├── FavoriteButton.svelte
   │   ├── RatingWidget.svelte
   │   ├── CollectionButton.svelte
   │   ├── UserCard.svelte
   │   └── ShareButton.svelte
   ├── services/
   │   ├── FavoritesService.ts
   │   ├── CollectionsService.ts
   │   ├── RatingService.ts
   │   └── SocialService.ts
   └── state/
       ├── user-content-state.svelte.ts
       └── social-state.svelte.ts
   ```

## Firestore Security Rules

Critical for protecting user data:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Helper functions
    function isSignedIn() {
      return request.auth != null;
    }

    function isOwner(userId) {
      return isSignedIn() && request.auth.uid == userId;
    }

    // User profiles
    match /users/{userId}/profile/{document} {
      allow read: if true;  // Public profiles
      allow write: if isOwner(userId);
    }

    // User favorites (private)
    match /users/{userId}/favorites/{favoriteId} {
      allow read, write: if isOwner(userId);
    }

    // User collections
    match /users/{userId}/collections/{collectionId} {
      allow read: if resource.data.isPublic || isOwner(userId);
      allow write: if isOwner(userId);
    }

    // Ratings
    match /ratings/{sequenceId}/{userId} {
      allow read: if true;
      allow write: if isOwner(userId);
    }

    // Sequences
    match /sequences/{sequenceId} {
      allow read: if true;
      allow create: if isSignedIn();
      allow update, delete: if isOwner(resource.data.authorId);
    }

    // Social - followers
    match /social/followers/{userId}/{followerId} {
      allow read: if true;
      allow write: if isOwner(followerId);
    }
  }
}
```

## Performance Considerations

### Caching Strategy

1. **User favorites**: Cache in localStorage for instant UI
2. **Ratings**: Cache aggregated stats, update periodically
3. **Collections**: Paginate large collections
4. **Profiles**: Cache viewed profiles

### Optimization

```typescript
// Cache favorites in local state
export class CachedFavoritesService {
  private cache = new Map<string, Set<string>>();

  async getFavorites(userId: string): Promise<string[]> {
    // Check cache first
    if (this.cache.has(userId)) {
      return Array.from(this.cache.get(userId)!);
    }

    // Fetch from Firestore
    const favorites = await this.fetchFromFirestore(userId);
    this.cache.set(userId, new Set(favorites));

    return favorites;
  }

  // Optimistic updates
  async addFavorite(userId: string, sequenceId: string) {
    // Update cache immediately
    if (!this.cache.has(userId)) {
      this.cache.set(userId, new Set());
    }
    this.cache.get(userId)!.add(sequenceId);

    // Update Firestore in background
    try {
      await this.saveToFirestore(userId, sequenceId);
    } catch (error) {
      // Rollback on error
      this.cache.get(userId)!.delete(sequenceId);
      throw error;
    }
  }
}
```

## Implementation Order (Recommended)

### Sprint 1: Foundation (Week 1-2)

- [ ] Set up Firestore
- [ ] Create base services (Favorites, UserProfile)
- [ ] Add Firestore to DI container
- [ ] Implement FavoriteButton component
- [ ] Add "My Favorites" page in Explore

### Sprint 2: Profiles (Week 3-4)

- [ ] User profile schema & service
- [ ] Profile page UI
- [ ] Profile settings page
- [ ] Username system (unique usernames)
- [ ] Profile picture upload (optional)

### Sprint 3: Collections (Week 5-6)

- [ ] Collections service
- [ ] Collection creation UI
- [ ] Collection detail page
- [ ] Add to collection workflow
- [ ] Drag-and-drop reordering

### Sprint 4: Ratings (Week 7)

- [ ] Rating service
- [ ] Rating widget component
- [ ] Display average ratings
- [ ] Filter by rating
- [ ] Review system

### Sprint 5: Social (Week 8-9)

- [ ] Follow system
- [ ] Activity feed
- [ ] Comments (optional)
- [ ] Share functionality
- [ ] Notifications (optional)

## Estimated Development Time

- **Phase 2A (Favorites)**: 2 weeks
- **Phase 2B (Profiles)**: 2 weeks
- **Phase 2C (Collections)**: 2 weeks
- **Phase 2D (Ratings)**: 1 week
- **Phase 2E (Social)**: 2 weeks

**Total**: ~9 weeks for complete implementation

## Quick Wins (Can Start Immediately)

1. **Add Favorite Button** - 2-3 days
   - Simple UI addition
   - Firestore setup
   - Instant user value

2. **My Favorites Page** - 1-2 days
   - Filter existing sequences
   - Show user's favorites

3. **User Attribution** - 1 day
   - Show "Created by @username" on sequences
   - Link to profile (even if profile page isn't done yet)

## Next Steps

1. **Complete Firebase/Facebook setup** (follow the guides)
2. **Test authentication** (make sure login works)
3. **Set up Firestore** in Firebase Console
4. **Start with Favorites** (quick win!)
5. **Build incrementally** (each feature adds value)

---

This roadmap transforms TKA into a social platform while maintaining clean architecture and performance. Each phase builds on the previous one, allowing you to ship features incrementally.

Ready to get started? Let me know which feature you want to tackle first!
