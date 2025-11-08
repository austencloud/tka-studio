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

/**
 * Firebase configuration object
 * Uses hardcoded values for reliable deployment across environments
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
    .catch(() => {
      return setPersistence(auth, browserLocalPersistence);
    })
    .catch((error) => {
      console.error("❌ [Firebase] Failed to set persistence:", error);
    });

  // Enable Firestore offline persistence
  // Try multi-tab first (best for PWA), fallback to single-tab
  enableMultiTabIndexedDbPersistence(firestore)
    .then(() => undefined)
    .catch((error) => {
      if (error.code === "failed-precondition") {
        // Multiple tabs open, fallback to single-tab
        return enableIndexedDbPersistence(firestore);
      } else if (error.code === "unimplemented") {
        return undefined;
      } else {
        console.error(
          "❌ [Firestore] Failed to enable offline persistence:",
          error
        );
        return undefined;
      }
    })
    .catch((error) => {
      console.error("❌ [Firestore] Failed to enable persistence:", error);
    });
}

/**
 * Export the app instance if needed for other Firebase services
 */
export { app };
