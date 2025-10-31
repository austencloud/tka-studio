# Firebase Setup Guide

This guide walks you through setting up a Firebase project for your TKA application.

## Step 1: Create a Firebase Project

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" (or "Create a project" if this is your first)
3. Enter your project name (e.g., "TKA Web App")
4. Click "Continue"

## Step 2: Configure Google Analytics (Optional)

1. Choose whether to enable Google Analytics
   - **Recommended**: Enable it for user insights
   - You can always add it later
2. If enabled, select or create a Google Analytics account
3. Click "Create project"
4. Wait for Firebase to provision your project (usually takes 30-60 seconds)

## Step 3: Register Your Web App

1. In your Firebase project dashboard, click the **Web icon** (`</>`) to add a web app
2. Register your app:
   - **App nickname**: "TKA Web App" (or any name you prefer)
   - **Firebase Hosting**: ☑ Check this if you plan to use Firebase Hosting (optional)
3. Click "Register app"

## Step 4: Get Your Firebase Configuration

After registering, you'll see your Firebase configuration. It looks like this:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef1234567890",
};
```

**Copy these values** - you'll need them in the next step.

## Step 5: Add Configuration to Your Project

1. Open your `.env` file in the project root
2. Replace the placeholder values with your Firebase config:

```env
PUBLIC_FIREBASE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
PUBLIC_FIREBASE_PROJECT_ID=your-project-id
PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789012
PUBLIC_FIREBASE_APP_ID=1:123456789012:web:abcdef1234567890
```

3. Save the file

**Important**: Never commit your actual `.env` file to version control. The `.env.example` file is safe to commit.

## Step 6: Enable Authentication

1. In the Firebase Console, go to your project
2. In the left sidebar, click **"Build" > "Authentication"**
3. Click **"Get started"**
4. You'll see the "Sign-in method" tab

## Step 7: Configure Authorized Domains

Before enabling providers, add your domain:

1. In Authentication, go to the **"Settings"** tab
2. Scroll to **"Authorized domains"**
3. Add your domains:
   - `localhost` (already added for development)
   - Your production domain (e.g., `yourdomain.com`)
   - Your Netlify domain (e.g., `your-app.netlify.app`)
4. Click "Add domain" for each

## Step 8: Set Up Authentication Providers

Now you're ready to enable social login providers. See the provider-specific guides:

- [Facebook OAuth Setup](./FACEBOOK_OAUTH_SETUP.md) - For Facebook and Instagram login
- Google OAuth Setup - Built into Firebase, just enable it in the console

### Quick: Enable Google Sign-In

Since you're using Firebase, Google auth is super easy:

1. In **"Sign-in method"** tab, find **"Google"**
2. Click on it
3. Toggle **"Enable"**
4. Select a **"Project support email"** (your email)
5. Click **"Save"**

That's it! Google login is now working.

## Step 9: Test Your Setup

1. Start your development server:

   ```bash
   npm run dev
   ```

2. Navigate to `http://localhost:5173/auth/login`

3. Try signing in with Google (if you enabled it)

4. Check the browser console for any errors

5. If successful, you should be redirected to the home page

## Firestore Database (Optional)

If you want to store user data:

1. In Firebase Console, go to **"Build" > "Firestore Database"**
2. Click **"Create database"**
3. Choose a location (usually closest to your users)
4. Start in **"Test mode"** for development (you'll add security rules later)
5. Click "Enable"

### Example Security Rules (for later):

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

## Firebase Storage (Optional)

If you need to store user-uploaded files:

1. In Firebase Console, go to **"Build" > "Storage"**
2. Click **"Get started"**
3. Start in **"Test mode"** for development
4. Click "Next" and "Done"

## Common Issues

### "Firebase: Error (auth/unauthorized-domain)"

- Solution: Add your domain to Authorized domains in Authentication > Settings

### "Firebase: Error (auth/configuration-not-found)"

- Solution: Make sure you've enabled the authentication provider in Firebase Console

### Environment Variables Not Loading

- Solution: Restart your dev server after changing `.env`
- Make sure variable names start with `PUBLIC_`

### "Invalid API key"

- Solution: Double-check your API key in `.env` matches Firebase Console
- Make sure there are no extra spaces or quotes

## Production Checklist

Before deploying to production:

- [ ] Set up proper Firestore security rules (if using Firestore)
- [ ] Set up proper Storage security rules (if using Storage)
- [ ] Add production domain to Authorized domains
- [ ] Enable "Email enumeration protection" in Authentication > Settings
- [ ] Set up Firebase App Check (protects against abuse)
- [ ] Review usage quotas and upgrade plan if needed
- [ ] Set up monitoring and alerts

## Next Steps

Now that Firebase is set up, continue with:

1. [Facebook OAuth Setup](./FACEBOOK_OAUTH_SETUP.md) - Enable Facebook/Instagram login
2. [Instagram OAuth Setup](./INSTAGRAM_OAUTH_SETUP.md) - Add Instagram-specific features

## Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firebase Authentication Docs](https://firebase.google.com/docs/auth)
- [SvelteKit + Firebase Guide](https://firebase.google.com/docs/web/setup)
- [Firebase Pricing](https://firebase.google.com/pricing)

## Free Tier Limits

Firebase offers a generous free tier:

- **Authentication**: Unlimited users
- **Firestore**: 50,000 reads/day, 20,000 writes/day
- **Storage**: 1 GB storage, 10 GB/month transfer
- **Hosting**: 10 GB/month, 360 MB/day

These limits should be more than enough for development and small to medium apps.
