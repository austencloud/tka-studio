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
import {
  PUBLIC_FIREBASE_API_KEY,
  PUBLIC_FIREBASE_AUTH_DOMAIN,
  PUBLIC_FIREBASE_PROJECT_ID,
  PUBLIC_FIREBASE_STORAGE_BUCKET,
  PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  PUBLIC_FIREBASE_APP_ID,
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
 */
const firebaseConfig = {
  apiKey: PUBLIC_FIREBASE_API_KEY,
  authDomain: PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: PUBLIC_FIREBASE_APP_ID,
};

/**
 * Initialize Firebase App
 * Prevents multiple initializations in development with HMR
 */
let app: FirebaseApp;

if (!getApps().length) {
  app = initializeApp(firebaseConfig);
} else {
  app = getApps()[0];
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
