/**
 * Firebase Configuration and Initialization
 *
 * Sets up Firebase app and exports auth instance for use throughout the application.
 * Uses environment variables for configuration.
 */

import { initializeApp, getApps, type FirebaseApp } from "firebase/app";
import {
  getAuth,
  type Auth,
  browserLocalPersistence,
  indexedDBLocalPersistence,
  setPersistence,
} from "firebase/auth";
import {
  getFirestore,
  type Firestore,
  enableIndexedDbPersistence,
  enableMultiTabIndexedDbPersistence,
} from "firebase/firestore";
import { getAnalytics, type Analytics, isSupported } from "firebase/analytics";
import {
  PUBLIC_FIREBASE_API_KEY,
  PUBLIC_FIREBASE_AUTH_DOMAIN,
  PUBLIC_FIREBASE_PROJECT_ID,
  PUBLIC_FIREBASE_STORAGE_BUCKET,
  PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  PUBLIC_FIREBASE_APP_ID,
  PUBLIC_FIREBASE_MEASUREMENT_ID,
} from "$env/static/public";

// Validate environment variables
if (
  !PUBLIC_FIREBASE_API_KEY ||
  !PUBLIC_FIREBASE_AUTH_DOMAIN ||
  !PUBLIC_FIREBASE_PROJECT_ID
) {
  console.warn(
    "Missing Firebase environment variables. Authentication features will be disabled."
  );
}

/**
 * Firebase configuration object
 * TEMPORARY: Hardcoded to bypass Vite env loading issue
 */
const firebaseConfig = {
  apiKey: "AIzaSyDKUM9pf0e_KgFjW1OBKChvrU75SnR12v4",
  authDomain: "the-kinetic-alphabet.firebaseapp.com",
  projectId: "the-kinetic-alphabet",
  storageBucket: "the-kinetic-alphabet.firebasestorage.app",
  messagingSenderId: "664225703033",
  appId: "1:664225703033:web:62e6c1eebe4fff3ef760a8",
  measurementId: "G-CQH94GGM6B",
};

// DEBUG: Log the Firebase configuration being used
console.log("🔧 [Firebase Config Debug] HARDCODED CONFIG", {
  projectId: firebaseConfig.projectId,
  authDomain: firebaseConfig.authDomain,
  apiKey: firebaseConfig.apiKey?.substring(0, 20) + '...',
});

/**
 * Initialize Firebase App
 * Prevents multiple initializations in development with HMR
 */
let app: FirebaseApp;

if (!getApps().length) {
  app = initializeApp(firebaseConfig);
} else {
  app = getApps()[0]!; // Safe because we check length above
}

/**
 * Firebase Auth instance
 * Use this throughout the app for authentication operations
 */
export const auth: Auth = getAuth(app);

/**
 * Firestore instance
 * Use this for all database operations (gamification, user data, etc.)
 */
export const firestore: Firestore = getFirestore(app);

/**
 * Firebase Analytics instance
 * Only initialized in browser environments where analytics is supported
 */
let analytics: Analytics | null = null;

if (typeof window !== "undefined") {
  isSupported()
    .then((supported) => {
      if (supported) {
        analytics = getAnalytics(app);
        console.log("✅ [Firebase] Analytics initialized");
      } else {
        console.warn("⚠️ [Firebase] Analytics not supported in this environment");
      }
    })
    .catch((error) => {
      console.error("❌ [Firebase] Failed to initialize analytics:", error);
    });
}

export { analytics };

/**
 * Configure Firebase Auth persistence
 * Try IndexedDB first (most reliable), fallback to localStorage
 * This provides the best resilience against storage clearing during redirects
 */
if (typeof window !== "undefined") {
  setPersistence(auth, indexedDBLocalPersistence)
    .catch((indexedDBError) => {
      console.warn("⚠️ [Firebase] IndexedDB persistence failed, using localStorage fallback:", indexedDBError);
      return setPersistence(auth, browserLocalPersistence);
    })
    .catch((error) => {
      console.error("❌ [Firebase] Failed to set any persistence:", error);
    });

  // Enable Firestore offline persistence
  // Try multi-tab first (best for PWA), fallback to single-tab
  enableMultiTabIndexedDbPersistence(firestore)
    .then(() => {
      console.log("✅ [Firestore] Multi-tab offline persistence enabled");
    })
    .catch((error) => {
      if (error.code === "failed-precondition") {
        // Multiple tabs open, fallback to single-tab
        console.warn("⚠️ [Firestore] Multiple tabs detected, using single-tab persistence");
        return enableIndexedDbPersistence(firestore);
      } else if (error.code === "unimplemented") {
        console.warn("⚠️ [Firestore] Offline persistence not supported in this browser");
      } else {
        console.error("❌ [Firestore] Failed to enable offline persistence:", error);
      }
    })
    .catch((error) => {
      console.error("❌ [Firestore] Failed to enable any persistence:", error);
    });
}

/**
 * Export the app instance if needed for other Firebase services
 */
export { app };
