# Instagram Integration Setup Guide

Complete guide to setting up Instagram OAuth and Graph API integration for posting carousel content from The Kinetic Alphabet app.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Facebook App Setup](#facebook-app-setup)
3. [Instagram Business Account Setup](#instagram-business-account-setup)
4. [Environment Configuration](#environment-configuration)
5. [Testing the Integration](#testing-the-integration)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts

1. **Facebook Developer Account**
   - Sign up at [developers.facebook.com](https://developers.facebook.com/)
   - Verify your account (email + phone number)

2. **Facebook Page**
   - Create a Facebook Page if you don't have one
   - You need Admin access to this page

3. **Instagram Business/Creator Account**
   - Convert your Instagram account to Business or Creator
   - Connect it to your Facebook Page

### Account Limitations

⚠️ **IMPORTANT**: Instagram Graph API only works with:
- Instagram Business accounts
- Instagram Creator accounts
- Accounts connected to a Facebook Page

❌ Personal Instagram accounts **cannot** use the API for posting.

---

## Facebook App Setup

### Step 1: Create a Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click **"My Apps"** → **"Create App"**
3. Choose app type: **"Business"**
4. Fill in app details:
   - **App Name**: "The Kinetic Alphabet" (or your preferred name)
   - **Contact Email**: Your email
   - **App Purpose**: Select appropriate category

### Step 2: Add Instagram Graph API

1. In your app dashboard, click **"Add Product"**
2. Find **"Instagram Graph API"** and click **"Set Up"**
3. Accept the terms of service

### Step 3: Configure OAuth Settings

1. Go to **Settings** → **Basic**
2. Add **App Domains**:
   - For local: `localhost`
   - For production: `yourdomain.com`

3. Add your **App Icon** and **Privacy Policy URL** (required for public apps)

4. Go to **Instagram Graph API** → **Settings**
5. Add **Valid OAuth Redirect URIs**:
   ```
   http://localhost:5173/auth/instagram/callback
   https://yourdomain.com/auth/instagram/callback
   ```

### Step 4: Get App Credentials

1. Go to **Settings** → **Basic**
2. Copy your **App ID**
3. Click **Show** next to **App Secret** and copy it
4. **⚠️ Keep the App Secret secure!** Never commit it to version control

---

## Instagram Business Account Setup

### Step 1: Convert Instagram to Business Account

1. Open **Instagram mobile app**
2. Go to **Settings** → **Account**
3. Tap **Switch to Professional Account**
4. Choose account type:
   - **Business**: For brands/companies
   - **Creator**: For influencers/content creators
5. Follow the setup wizard

### Step 2: Connect to Facebook Page

1. In Instagram app, go to **Settings** → **Account**
2. Tap **Linked Accounts** → **Facebook**
3. Choose the Facebook Page to connect
4. Grant necessary permissions

### Step 3: Verify Connection

1. Go to your **Facebook Page**
2. Click **Settings** → **Instagram**
3. Verify your Instagram account is connected
4. You should see your Instagram handle listed

---

## Environment Configuration

### Step 1: Copy Environment Template

```bash
cp .env.instagram.example .env.local
```

### Step 2: Configure Environment Variables

Edit `.env.local` and add your credentials:

```env
# Facebook App ID (from Step 4 above)
VITE_FACEBOOK_APP_ID=1234567890123456

# Facebook App Secret (from Step 4 above)
VITE_FACEBOOK_APP_SECRET=your_secret_here_keep_this_safe

# OAuth Redirect URI (must match Facebook App settings)
VITE_INSTAGRAM_OAUTH_REDIRECT_URI=http://localhost:5173/auth/instagram/callback
```

### Step 3: Update .gitignore

Ensure `.env.local` is in your `.gitignore`:

```gitignore
.env.local
.env.*.local
```

---

## Testing the Integration

### Step 1: Start Development Server

```bash
npm run dev
```

### Step 2: Connect Instagram Account

1. Navigate to your app at `http://localhost:5173`
2. Log in to your TKA account
3. Go to **Profile** → **Settings** → **Connected Accounts**
4. Click **"Connect Instagram"**
5. You'll be redirected to Facebook OAuth
6. Grant the requested permissions
7. You'll be redirected back to your app

### Step 3: Test Carousel Posting

1. Go to **Create** module
2. Create or select a sequence
3. Click **Share** button
4. In the Share panel:
   - Select a **video** from your device
   - The **sequence image** will be auto-included
   - The **animated GIF** will be auto-included
5. Arrange carousel order (drag-to-reorder)
6. Add a caption
7. Click **"Post to Instagram"**
8. Monitor the upload progress
9. Once complete, you'll get a link to view your post

---

## Troubleshooting

### "No Facebook Pages Found" Error

**Problem**: OAuth callback fails with "No Facebook Pages found"

**Solution**:
1. Ensure you have a Facebook Page created
2. Verify you're an Admin of the page
3. Check that your Instagram account is connected to this page
4. Try disconnecting and reconnecting Instagram to the page

### "No Instagram Business Account Connected" Error

**Problem**: Facebook Page doesn't have an Instagram account linked

**Solution**:
1. Go to Facebook Page → Settings → Instagram
2. Click "Connect Account"
3. Log in to your Instagram Business account
4. Grant permissions

### "Access Token Expired" Error

**Problem**: Instagram token has expired (tokens last 60 days)

**Solution**:
1. The app automatically refreshes tokens when needed
2. If refresh fails, disconnect and reconnect your Instagram account
3. Go to Profile → Connected Accounts → Disconnect Instagram
4. Then reconnect following the OAuth flow again

### "Invalid OAuth Redirect URI" Error

**Problem**: Redirect URI doesn't match Facebook App settings

**Solution**:
1. Check your `.env.local` file
2. Ensure `VITE_INSTAGRAM_OAUTH_REDIRECT_URI` exactly matches the URI in Facebook App settings
3. Don't forget the `/auth/instagram/callback` path
4. Protocol must match (http vs https)
5. No trailing slashes

### API Rate Limits

Instagram Graph API has rate limits:

- **200 requests** per hour per user
- **200 media uploads** per hour per user

If you hit rate limits:
1. Wait for the limit window to reset (60 minutes)
2. Implement request caching where possible
3. For high-volume usage, apply for higher limits from Facebook

### App Review Required

For production use, you may need Facebook App Review for certain permissions:

1. Go to **App Review** in Facebook Developer dashboard
2. Submit your app for review
3. Provide screen recordings showing how you use each permission
4. Explain your use case clearly
5. Wait for approval (typically 1-2 weeks)

**Permissions requiring review:**
- `instagram_content_publish` (required for posting)
- `instagram_manage_insights` (optional, for analytics)

---

## Additional Resources

- [Instagram Graph API Documentation](https://developers.facebook.com/docs/instagram-api)
- [Instagram Basic Display API vs Graph API](https://developers.facebook.com/docs/instagram-basic-display-api#instagram-graph-api)
- [Facebook Login for Instagram](https://developers.facebook.com/docs/facebook-login)
- [Instagram Content Publishing](https://developers.facebook.com/docs/instagram-api/guides/content-publishing)
- [Instagram Carousel Posts](https://developers.facebook.com/docs/instagram-api/guides/content-publishing#carousel-posts)

---

## Security Best Practices

1. **Never commit secrets**: Keep `.env.local` in `.gitignore`
2. **Use environment variables**: Never hardcode credentials
3. **Rotate secrets regularly**: Change App Secret periodically
4. **Implement CSRF protection**: The state parameter is included
5. **Validate tokens**: Always check token expiration before API calls
6. **Store tokens securely**: Use Firestore with proper security rules
7. **HTTPS only in production**: Never use HTTP for OAuth in production

---

## Support

If you encounter issues not covered in this guide:

1. Check the [Instagram Graph API Changelog](https://developers.facebook.com/docs/instagram-api/changelog)
2. Review [Instagram Platform Terms](https://developers.facebook.com/terms/instagram_platform)
3. Visit [Facebook Developers Community](https://developers.facebook.com/community/)
4. Submit an issue on our GitHub repository

---

## License & Attribution

This integration uses:
- Facebook Graph API v18.0
- Instagram Graph API
- Firebase Authentication & Firestore

Please ensure compliance with:
- [Instagram Platform Terms](https://www.instagram.com/about/legal/terms/api/)
- [Facebook Platform Terms](https://developers.facebook.com/terms/)
- Your app's privacy policy must disclose Instagram data usage
