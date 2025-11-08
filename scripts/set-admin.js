/**
 * Set Admin Script
 *
 * Run this script to grant admin privileges to a user.
 * Usage: node scripts/set-admin.js <user-email>
 */

import { initializeApp } from "firebase/app";
import { getFirestore, doc, setDoc, getDoc } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyDKUM9pf0e_KgFjW1OBKChvrU75SnR12v4",
  authDomain: "the-kinetic-alphabet.firebaseapp.com",
  projectId: "the-kinetic-alphabet",
  storageBucket: "the-kinetic-alphabet.firebasestorage.app",
  messagingSenderId: "664225703033",
  appId: "1:664225703033:web:62e6c1eebe4fff3ef760a8",
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

async function setAdmin(userId) {
  try {
    const userRef = doc(db, `users/${userId}`);

    // Check if user document exists
    const userDoc = await getDoc(userRef);

    if (userDoc.exists()) {
      // Update existing document
      await setDoc(userRef, { isAdmin: true }, { merge: true });
      console.log(`✅ Successfully set admin privileges for user: ${userId}`);
    } else {
      // Create new document with isAdmin
      await setDoc(userRef, { isAdmin: true });
      console.log(
        `✅ Created user document and set admin privileges for: ${userId}`
      );
    }

    process.exit(0);
  } catch (error) {
    console.error("❌ Error setting admin:", error);
    process.exit(1);
  }
}

// Get user ID from command line
const userId = process.argv[2];

if (!userId) {
  console.error("❌ Please provide a user ID");
  console.log("Usage: node scripts/set-admin.js <user-id>");
  process.exit(1);
}

console.log(`🔧 Setting admin privileges for user: ${userId}`);
setAdmin(userId);
