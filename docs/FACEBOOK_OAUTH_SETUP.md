# Facebook OAuth Setup Guide

This guide walks you through setting up Facebook Login for your TKA application using Firebase Authentication.

## Prerequisites

- ✅ Completed [Firebase Setup](./FIREBASE_SETUP.md)
- ✅ A Facebook account
- ✅ Your app running on a domain (localhost works for development)

## Part 1: Create Facebook App

### Step 1: Go to Facebook Developers

1. Visit [Facebook Developers](https://developers.facebook.com/)
2. Log in with your Facebook account
3. Click **"My Apps"** in the top-right corner
4. Click **"Create App"**

### Step 2: Choose App Type

1. Select **"Consumer"** (for user authentication)
2. Click **"Next"**

### Step 3: Add App Details

1. **Display Name**: Enter your app name (e.g., "TKA Web App")
2. **App Contact Email**: Enter your email address
3. **Business Account**: Leave blank (optional)
4. Click **"Create App"**
5. Complete any security checks (CAPTCHA, etc.)

### Step 4: Add Facebook Login Product

1. In your app dashboard, find **"Add a Product"** section
2. Find **"Facebook Login"** in the list
3. Click **"Set Up"** on the Facebook Login card
4. Select **"Web"** as your platform
5. Enter your Site URL:
   - Development: `http://localhost:5173`
   - Production: `https://yourdomain.com`
6. Click **"Save"**

## Part 2: Configure OAuth Settings

### Step 5: Configure Redirect URIs

This is the most important step!

1. In the left sidebar, go to: **Facebook Login > Settings**

2. Under **"Valid OAuth Redirect URIs"**, add your Firebase callback URL:

   ```
   https://YOUR-PROJECT-ID.firebaseapp.com/__/auth/handler
   ```

   **Where to find this:**
   - Go to Firebase Console
   - Open your project
   - Go to Authentication > Sign-in method
   - Enable Facebook provider (see Part 3)
   - Copy the "Callback URL" shown at the bottom

3. Click **"Save Changes"**

### Step 6: Configure Allowed Domains (Optional but Recommended)

1. Still in **Facebook Login > Settings**
2. Scroll to **"Allowed Domains for the JavaScript SDK"**
3. Add:
   ```
   localhost
   yourdomain.com
   your-project-id.firebaseapp.com
   ```
4. Click **"Save Changes"**

## Part 3: Get App Credentials

### Step 7: Get Your App ID and Secret

1. In the left sidebar, click **Settings > Basic**
2. You'll see:
   - **App ID**: Copy this (e.g., `123456789012345`)
   - **App Secret**: Click **"Show"** and copy it (keep this SECRET!)

**⚠️ Security Warning**: Never share your App Secret or commit it to version control!

## Part 4: Enable Facebook Login in Firebase

### Step 8: Configure Facebook Provider in Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to **Authentication > Sign-in method**
4. Find **"Facebook"** in the providers list
5. Click on it
6. Toggle **"Enable"**
7. Enter your credentials:
   - **App ID**: Paste your Facebook App ID
   - **App Secret**: Paste your Facebook App Secret
8. Copy the **"Callback URL"** shown (you'll need this for Step 5 if you haven't done it)
9. Click **"Save"**

### Step 9: Update Facebook Redirect URI (if needed)

If you haven't added the Firebase callback URL to Facebook:

1. Go back to Facebook Developers
2. Go to **Facebook Login > Settings**
3. Add the Firebase callback URL from Step 8
4. Click **"Save Changes"**

## Part 5: Test Your Integration

### Step 10: Test Login

1. Start your development server:
   ```bash
   npm run dev
   ```

2. Go to: `http://localhost:5173/auth/login`

3. Click **"Continue with Facebook"**

4. You should see a Facebook login popup

5. After logging in, you'll be asked to authorize your app

6. You should be redirected back to your app, logged in!

### Troubleshooting Test Issues

**"App Not Set Up: This app is still in development..."**
- This is normal! Your app is in Development mode
- You can test with your Facebook account
- Add test users (see Step 13) to let others test

**"URL Blocked: This redirect failed..."**
- Check that your redirect URI in Facebook matches Firebase callback URL exactly
- Make sure it starts with `https://` (not `http://`)
- No trailing slashes

**"Invalid OAuth Redirect URI"**
- Double-check the callback URL in Facebook Login > Settings
- Make sure you clicked "Save Changes" in Facebook

## Part 6: Prepare for Production

### Step 11: Add Required Policy URLs

Facebook requires these pages before you can make your app public:

1. Create these pages in your app:
   - **Privacy Policy** (`/privacy`)
   - **Terms of Service** (`/terms`)
   - **Data Deletion Instructions** (`/data-deletion`)

2. In Facebook App, go to **Settings > Basic**

3. Add your URLs:
   - **Privacy Policy URL**: `https://yourdomain.com/privacy`
   - **Terms of Service URL**: `https://yourdomain.com/terms`
   - **User Data Deletion**: `https://yourdomain.com/data-deletion`

4. Click **"Save Changes"**

### Step 12: Choose App Category and Icon

1. Still in **Settings > Basic**
2. **Category**: Choose appropriate category (e.g., "Entertainment", "Productivity")
3. **App Icon**: Upload a 1024x1024px icon (PNG)
4. Click **"Save Changes"**

### Step 13: Add Test Users (Development Mode)

To let friends test your app before it's public:

1. In the left sidebar, go to **Roles > Test Users**
2. Click **"Add"** to create test users
3. Or click **"Add Testers"** to add existing Facebook users by their Facebook User ID

### Step 14: Request Advanced Access (for Production)

Before making your app live, you need to request access for permissions:

1. Go to **App Review > Permissions and Features**

2. Find these permissions:
   - `email` - Already approved
   - `public_profile` - Already approved

3. If you need additional permissions (like posting to Facebook), request them here

4. Click **"Request Advanced Access"** for each permission

5. Fill out the form:
   - Explain how you use each permission
   - Provide screencasts showing the feature
   - This usually takes 1-2 weeks for review

### Step 15: Make Your App Live

⚠️ **Only do this when you're ready for production!**

1. Go to **Settings > Basic**
2. At the top of the page, find **"App Mode"**
3. Switch the toggle from **"Development"** to **"Live"**
4. Confirm the switch

Now anyone with a Facebook account can log in to your app!

## Advanced Configuration

### Enable Instagram Login (Future)

Instagram login requires Facebook Login to be set up first. See [Instagram OAuth Setup](./INSTAGRAM_OAUTH_SETUP.md) for details.

### Request User Permissions

If you need more than basic profile data:

```typescript
import { FacebookAuthProvider } from "firebase/auth";

const provider = new FacebookAuthProvider();
provider.addScope('user_birthday');
provider.addScope('user_location');
// Add more scopes as needed
```

Available scopes: [Facebook Permissions Reference](https://developers.facebook.com/docs/permissions/reference)

### Custom OAuth Parameters

```typescript
provider.setCustomParameters({
  'display': 'popup' // or 'page'
});
```

## Common Issues & Solutions

### Development Mode Issues

**Issue**: Friends can't log in to test
- **Solution**: Add them as Test Users or Developers in Roles section

**Issue**: "This app is not available"
- **Solution**: Your app is in Development mode. Either add user as tester or make app Live

### Production Issues

**Issue**: Users can't log in after making app Live
- **Solution**:
  - Check that all Policy URLs are accessible
  - Verify App Category is set
  - Make sure app icon is uploaded

**Issue**: "Permissions Error"
- **Solution**: Some permissions require App Review. Check App Review > Permissions

### General Issues

**Issue**: "Can't Load URL: The domain of this URL isn't included..."
- **Solution**: Add your domain to App Domains in Settings > Basic

**Issue**: Login works on desktop but not mobile
- **Solution**:
  - Check that your OAuth redirect URIs include your mobile-accessible domain
  - Ensure your site uses HTTPS in production

## Security Best Practices

1. **Never expose your App Secret**
   - Keep it in `.env` file (which is gitignored)
   - Never log it or send it to the client

2. **Use HTTPS in production**
   - Required by Facebook
   - Netlify provides this automatically

3. **Verify tokens server-side**
   - Firebase handles this automatically
   - Never trust client-side claims alone

4. **Implement rate limiting**
   - Protect your login endpoint
   - Firebase has built-in protection

5. **Monitor for suspicious activity**
   - Check Firebase Authentication logs
   - Set up alerts in Firebase Console

## Data Privacy & Compliance

### What Data Facebook Provides

With basic permissions, you get:
- Name
- Email (if user granted permission)
- Profile picture
- Facebook User ID

### GDPR Compliance

You must:
- Provide a Privacy Policy
- Explain what data you collect
- Allow users to delete their data
- Get explicit consent for data usage

### Data Deletion Callback

Facebook requires a Data Deletion endpoint:

```typescript
// src/routes/auth/facebook/deletion/+server.ts
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
  const { signed_request } = await request.json();

  // Verify and decode the signed request
  // Delete user data from your database
  // Return confirmation URL

  return new Response(JSON.stringify({
    url: 'https://yourdomain.com/deletion-confirmed',
    confirmation_code: 'unique-code'
  }));
};
```

Add this endpoint URL to Facebook App Settings > Basic > User Data Deletion.

## Testing Checklist

- [ ] Login popup appears
- [ ] Can authenticate with Facebook
- [ ] Redirected back to app after login
- [ ] User data is accessible (name, email, photo)
- [ ] Logout works correctly
- [ ] Login state persists after page refresh
- [ ] Test on different browsers
- [ ] Test on mobile devices

## Production Checklist

- [ ] App has icon and category set
- [ ] Privacy Policy URL is accessible
- [ ] Terms of Service URL is accessible
- [ ] Data Deletion URL is functional
- [ ] Production domain added to Authorized domains
- [ ] Firebase callback URL added to Facebook OAuth settings
- [ ] App Review completed (if using additional permissions)
- [ ] App Mode switched to "Live"
- [ ] Tested with non-developer Facebook account

## Next Steps

- [Instagram OAuth Setup](./INSTAGRAM_OAUTH_SETUP.md) - Add Instagram login
- [Implementation Guide](./IMPLEMENTATION_GUIDE.md) - Integrate auth into your app

## Resources

- [Facebook Login Documentation](https://developers.facebook.com/docs/facebook-login)
- [Firebase Facebook Auth](https://firebase.google.com/docs/auth/web/facebook-login)
- [Facebook App Review](https://developers.facebook.com/docs/app-review)
- [Facebook Permissions Reference](https://developers.facebook.com/docs/permissions/reference)
