# Firebase Authentication Setup - Complete Guide

Welcome! This guide will help you add Facebook and Google authentication to your TKA Studio application using Firebase.

## What's Been Built

Your app now has a complete authentication system with:

✅ **Firebase Integration** - Modern, reliable auth backend
✅ **Facebook Login** - Let users sign in with Facebook
✅ **Google Login** - Let users sign in with Google
✅ **User Profile Page** - View account information
✅ **Reactive Auth State** - Auth status updates automatically everywhere
✅ **Protected Routes** - Easy route protection
✅ **Pre-built UI Components** - Beautiful login buttons and user menus

## Quick Start

### 1. Set Up Firebase (15 minutes)

Follow [Firebase Setup Guide](./FIREBASE_SETUP.md):

- Create Firebase project
- Get your configuration keys
- Add them to `.env` file
- Enable authentication providers

### 2. Set Up Facebook Login (20 minutes)

Follow [Facebook OAuth Setup Guide](./FACEBOOK_OAUTH_SETUP.md):

- Create Facebook App
- Configure OAuth settings
- Connect to Firebase
- Test login

### 3. Start Using Auth (5 minutes)

Follow [Implementation Guide](./IMPLEMENTATION_GUIDE.md):

- Use auth in your components
- Protect routes
- Customize UI

**Total time: ~40 minutes** ⏱️

## File Structure

Here's what was added to your project:

```
src/lib/shared/auth/
├── firebase.ts                    # Firebase initialization
├── stores/
│   └── authStore.ts              # Auth state management
├── components/
│   ├── SocialAuthButton.svelte   # Login buttons
│   ├── UserMenu.svelte           # User dropdown menu
│   └── index.ts                  # Component exports
└── index.ts                      # Main auth exports

src/routes/
├── auth/
│   └── login/
│       └── +page.svelte          # Login page
└── profile/
    └── +page.svelte              # User profile page

docs/
├── AUTH_README.md                # This file
├── FIREBASE_SETUP.md             # Firebase setup guide
├── FACEBOOK_OAUTH_SETUP.md       # Facebook OAuth guide
└── IMPLEMENTATION_GUIDE.md       # How to use auth in your app

.env                              # Firebase config (gitignored)
.env.example                      # Template for config
```

## Environment Variables

Your `.env` file needs these Firebase configuration values:

```env
PUBLIC_FIREBASE_API_KEY=your-api-key
PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
PUBLIC_FIREBASE_PROJECT_ID=your-project-id
PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
PUBLIC_FIREBASE_APP_ID=your-app-id
```

Get these from your Firebase Console: **Project Settings > General > Your apps > SDK setup and configuration**

## Using Authentication

### Check If User Is Logged In

```svelte
<script lang="ts">
  import { user, isAuthenticated } from "$shared/auth";
</script>

{#if $isAuthenticated}
  <p>Welcome, {$user?.displayName}!</p>
{:else}
  <a href="/auth/login">Sign In</a>
{/if}
```

### Add Login Button to Navigation

```svelte
<script lang="ts">
  import { isAuthenticated } from "$shared/auth";
  import { UserMenu } from "$shared/auth/components";
</script>

<nav>
  <a href="/">Home</a>

  {#if $isAuthenticated}
    <UserMenu />
  {:else}
    <a href="/auth/login">Sign In</a>
  {/if}
</nav>
```

### Protect a Route

```svelte
<script lang="ts">
  import { isAuthenticated, isLoading } from "$shared/auth";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  onMount(() => {
    const unsubscribe = isAuthenticated.subscribe((authenticated) => {
      if (!authenticated && !$isLoading) {
        goto("/auth/login");
      }
    });

    return unsubscribe;
  });
</script>

{#if $isAuthenticated}
  <!-- Your protected content -->
{/if}
```

For more examples, see the [Implementation Guide](./IMPLEMENTATION_GUIDE.md).

## Available Routes

Once set up, these routes work out of the box:

- `/auth/login` - Login page with social auth buttons
- `/profile` - User profile page (requires login)

## Available Components

Import and use these pre-built components:

```typescript
import {
  SocialAuthButton, // Branded login buttons
  UserMenu, // User avatar + dropdown
} from "$shared/auth/components";
```

## Available Stores

Use these reactive stores anywhere:

```typescript
import {
  user, // Current user object
  isAuthenticated, // true/false
  isLoading, // true while checking auth
  authStore, // Full store with methods
} from "$shared/auth";
```

## Documentation

1. **[Firebase Setup](./FIREBASE_SETUP.md)** - Set up Firebase project
2. **[Facebook OAuth Setup](./FACEBOOK_OAUTH_SETUP.md)** - Enable Facebook login
3. **[Implementation Guide](./IMPLEMENTATION_GUIDE.md)** - Use auth in your app

## Features

### What Works Now

✅ Facebook Login
✅ Google Login
✅ Auto sign-in on page refresh
✅ Logout functionality
✅ User profile display
✅ Protected routes
✅ Reactive auth state
✅ Mobile responsive
✅ Dark mode support
✅ Accessible (WCAG 2.1)

### What You Can Add Next

- Email/password authentication
- Email verification
- Password reset
- Multi-factor authentication
- User data in Firestore
- Profile photo upload
- Account deletion
- Link multiple accounts

## Common Tasks

### Add Another Social Provider

1. Go to Firebase Console > Authentication > Sign-in method
2. Enable the provider (Twitter, GitHub, etc.)
3. Add credentials if required
4. Use in your code:

```svelte
<SocialAuthButton provider="github">Sign in with GitHub</SocialAuthButton>
```

### Customize the Login Page

Edit `src/routes/auth/login/+page.svelte`:

- Change colors
- Add/remove providers
- Modify layout
- Add branding

### Store User Data

Example using Firestore:

```typescript
import { doc, setDoc } from "firebase/firestore";
import { db } from "$shared/firebase"; // You'll need to export this

async function saveUserData(userId: string, data: any) {
  await setDoc(doc(db, "users", userId), data);
}
```

## Testing

### Development

Test with your own accounts:

1. Start dev server: `npm run dev`
2. Go to `/auth/login`
3. Click "Continue with Facebook" or "Continue with Google"
4. Authorize the app
5. You'll be logged in!

### Testing with Others

**Facebook** (while in Development mode):

1. Go to Facebook App > Roles > Test Users
2. Add testers by Facebook User ID
3. They can now test login

**Google**: Works for anyone immediately

### Production Testing

After making your Facebook app Live, anyone can log in.

## Troubleshooting

### "Firebase: Error (auth/unauthorized-domain)"

**Fix**: Add your domain to Firebase Console > Authentication > Settings > Authorized domains

### "URL Blocked: This redirect failed"

**Fix**: Check Facebook App > Facebook Login > Settings > Valid OAuth Redirect URIs

### "Popup was blocked"

**Fix**: User needs to allow popups. Consider adding a message:

```svelte
{#if error?.includes("popup-blocked")}
  <p>Please allow popups for this site</p>
{/if}
```

### Login works but user data is null

**Fix**: Wait a moment for auth state to initialize:

```svelte
{#if $isLoading}
  <p>Loading...</p>
{:else if $user}
  <p>Welcome, {$user.displayName}!</p>
{/if}
```

More troubleshooting in [Firebase Setup](./FIREBASE_SETUP.md#common-issues) and [Facebook OAuth Setup](./FACEBOOK_OAUTH_SETUP.md#common-issues--solutions).

## Security

### Best Practices

✅ **Environment variables** - Never commit `.env` to git
✅ **HTTPS in production** - Firebase requires it (Netlify provides this)
✅ **Authorized domains** - Only allow your domains
✅ **User input validation** - Always validate on server-side
✅ **Rate limiting** - Firebase has built-in protection

### What's Protected

Firebase handles:

- Token validation
- Session management
- XSS protection
- CSRF protection

You handle:

- Authorization (what users can access)
- Data validation
- Business logic

## Production Checklist

Before going live:

### Firebase

- [ ] Authorized domains configured
- [ ] Security rules set (if using Firestore/Storage)
- [ ] App Check enabled (optional but recommended)
- [ ] Monitoring enabled

### Facebook App

- [ ] Privacy Policy published and linked
- [ ] Terms of Service published and linked
- [ ] Data Deletion endpoint working
- [ ] App icon and category set
- [ ] OAuth redirect URIs correct
- [ ] App Mode set to "Live"

### Your App

- [ ] `.env` values are correct for production
- [ ] Error handling implemented
- [ ] Loading states look good
- [ ] Mobile testing complete
- [ ] Works in all major browsers

## Support & Resources

### Official Documentation

- [Firebase Auth Docs](https://firebase.google.com/docs/auth)
- [Facebook Login Docs](https://developers.facebook.com/docs/facebook-login)
- [SvelteKit Docs](https://kit.svelte.dev/)

### Your Project Docs

- [Firebase Setup](./FIREBASE_SETUP.md)
- [Facebook OAuth Setup](./FACEBOOK_OAUTH_SETUP.md)
- [Implementation Guide](./IMPLEMENTATION_GUIDE.md)

### Example Code

Look at the working examples:

- [src/routes/auth/login/+page.svelte](../src/routes/auth/login/+page.svelte) - Login page
- [src/routes/profile/+page.svelte](../src/routes/profile/+page.svelte) - Profile page
- [src/lib/shared/auth/](../src/lib/shared/auth/) - Auth system

## What's Next?

1. **Follow [Firebase Setup](./FIREBASE_SETUP.md)** to create your project
2. **Follow [Facebook OAuth Setup](./FACEBOOK_OAUTH_SETUP.md)** to enable login
3. **Read [Implementation Guide](./IMPLEMENTATION_GUIDE.md)** to use auth in your app
4. **Customize** the UI to match your brand
5. **Deploy** and test in production

Good luck! 🚀

---

**Questions?** Check the troubleshooting sections in each guide or review the example code in the project.
