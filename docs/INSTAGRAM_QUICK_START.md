# Instagram Integration - Quick Start Guide

**5-Minute Setup Guide** for developers

---

## ✅ Prerequisites

- Facebook Developer Account
- Instagram Business/Creator Account
- Facebook Page connected to Instagram
- Node.js & npm installed

---

## 🚀 Setup (5 Minutes)

### Step 1: Facebook App (2 minutes)

1. Go to https://developers.facebook.com/apps
2. Click "Create App" → Choose "Business"
3. Add product: **Instagram Graph API**
4. Settings → Basic:
   - Copy **App ID**
   - Copy **App Secret**
5. Instagram Graph API → Settings:
   - Add OAuth Redirect URI: `http://localhost:5173/auth/instagram/callback`

### Step 2: Environment Variables (1 minute)

```bash
# Copy template
cp .env.instagram.example .env.local

# Edit .env.local
VITE_FACEBOOK_APP_ID=your_app_id_here
VITE_FACEBOOK_APP_SECRET=your_app_secret_here
VITE_INSTAGRAM_OAUTH_REDIRECT_URI=http://localhost:5173/auth/instagram/callback
```

### Step 3: Start Dev Server (30 seconds)

```bash
npm run dev
```

### Step 4: Connect Instagram (1 minute)

1. Navigate to `http://localhost:5173`
2. Log in to your TKA account
3. Go to **Profile** → **Settings** → **Connected Accounts**
4. Click **"Connect Instagram"**
5. Log in with Facebook
6. Grant permissions
7. Done! ✅

---

## 📁 Key Files

### Services
- `src/lib/modules/create/share/services/implementations/InstagramAuthService.ts` - OAuth
- `src/lib/modules/create/share/services/implementations/InstagramGraphApiService.ts` - API
- `src/lib/modules/create/share/services/implementations/MediaBundlerService.ts` - Media

### Components
- `src/lib/shared/navigation/components/profile-settings/ConnectedAccounts.svelte` - Connection UI
- `src/lib/modules/create/share/components/InstagramPostProgress.svelte` - Progress
- `src/routes/auth/instagram/callback/+page.svelte` - OAuth callback

### Domain Models
- `src/lib/modules/create/share/domain/models/InstagramAuth.ts` - Types

### API Endpoints
- `src/routes/api/instagram/upload-media/+server.ts` - Media upload

---

## 🧪 Testing

### Test OAuth Flow

```typescript
import { resolve, TYPES } from '$shared';
import { INSTAGRAM_PERMISSIONS } from '$create/share/domain';

const authService = resolve<IInstagramAuthService>(TYPES.IInstagramAuthService);
await authService.initiateOAuthFlow([INSTAGRAM_PERMISSIONS.CONTENT_PUBLISH]);
```

### Test Media Bundling

```typescript
const bundler = resolve<IMediaBundlerService>(TYPES.IMediaBundlerService);
const items = await bundler.createCarouselBundle(
  sequence,
  videoFile,
  shareOptions
);
console.log('Bundled items:', items);
```

### Test Carousel Posting

```typescript
const graphApi = resolve<IInstagramGraphApiService>(TYPES.IInstagramGraphApiService);
const token = await authService.getToken(userId);

const post: InstagramCarouselPost = {
  items,
  caption: "My sequence! #kinetic #alphabet",
  hashtags: ["kinetic", "alphabet"],
  shareToFacebook: false,
  sequenceId: sequence.id,
};

const result = await graphApi.postCarousel(token, post, (status) => {
  console.log(`${status.status}: ${status.progress}%`);
});

console.log('Posted!', result.permalink);
```

---

## 🐛 Common Issues

### "No Facebook Pages Found"

**Fix**: Ensure you have a Facebook Page and you're an admin. Go to facebook.com/pages to create one.

### "No Instagram Business Account"

**Fix**: Convert your Instagram to Business:
1. Instagram app → Settings → Account
2. Switch to Professional Account → Business
3. Connect to your Facebook Page

### "Invalid OAuth Redirect URI"

**Fix**: Ensure `.env.local` URI exactly matches Facebook App settings:
- `http://localhost:5173/auth/instagram/callback` (no trailing slash)

### "Token Expired"

**Fix**: Disconnect and reconnect Instagram in Profile → Connected Accounts

---

## 📖 Full Documentation

- **Setup Guide**: `docs/INSTAGRAM_SETUP_GUIDE.md` (detailed)
- **Implementation Status**: `docs/INSTAGRAM_INTEGRATION_STATUS.md`
- **Completion Summary**: `INSTAGRAM_INTEGRATION_COMPLETE.md`

---

## ✨ What's Built

✅ OAuth 2.0 flow
✅ Token management (60-day tokens)
✅ Media bundling (video + image + GIF)
✅ Firebase Storage upload
✅ Instagram Graph API integration
✅ Progress tracking UI
✅ Connection management UI

---

## 🎯 Next Steps

1. **Build Carousel Composer** (main posting UI)
2. **Integrate into SharePanel**
3. **Test end-to-end**
4. **Deploy!**

---

**Estimated time to MVP from here**: 8-12 hours (mostly UI work)

**Questions?** See full docs in `/docs` folder.

---

🎉 **You're all set!** The hard parts (OAuth, API, services) are done. Just need the UI integration now!
