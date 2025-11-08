/**
 * User Explore Service Implementation
 *
 * Fetches user data from Firebase Firestore for the Explore module.
 */

import { injectable } from "inversify";
import {
  collection,
  getDocs,
  doc,
  getDoc,
  query,
  where,
  orderBy,
  limit,
  onSnapshot,
} from "firebase/firestore";
import { firestore } from "$shared/auth/firebase";
import type {
  IUserExploreService,
  UserProfile,
} from "../contracts/IUserExploreService";

@injectable()
export class UserExploreService implements IUserExploreService {
  private readonly USERS_COLLECTION = "users";

  /**
   * Fetch all users from Firestore (one-time fetch)
   * Limited to 100 users for performance
   */
  async getAllUsers(): Promise<UserProfile[]> {
    try {
      console.log(
        "🔍 [UserExploreService] Fetching all users from Firestore..."
      );

      const usersRef = collection(firestore, this.USERS_COLLECTION);
      const q = query(usersRef, limit(100));
      const querySnapshot = await getDocs(q);

      const users: UserProfile[] = [];

      for (const docSnap of querySnapshot.docs) {
        const data = docSnap.data();
        const user = await this.mapFirestoreToUserProfile(docSnap.id, data);
        if (user) {
          users.push(user);
        }
      }

      console.log(`✅ [UserExploreService] Fetched ${users.length} users`);
      return users;
    } catch (error) {
      console.error("❌ [UserExploreService] Error fetching users:", error);
      // Re-throw the original error to preserve the error message
      throw error;
    }
  }

  /**
   * Subscribe to real-time user updates
   * Returns an unsubscribe function to stop listening
   */
  subscribeToUsers(callback: (users: UserProfile[]) => void): () => void {
    console.log(
      "🔔 [UserExploreService] Setting up real-time user subscription..."
    );

    const usersRef = collection(firestore, this.USERS_COLLECTION);
    const q = query(usersRef, limit(100));

    const unsubscribe = onSnapshot(
      q,
      async (querySnapshot) => {
        console.log(
          "🔄 [UserExploreService] Real-time update received, processing users..."
        );

        const users: UserProfile[] = [];

        for (const docSnap of querySnapshot.docs) {
          const data = docSnap.data();
          const user = await this.mapFirestoreToUserProfile(docSnap.id, data);
          if (user) {
            users.push(user);
          }
        }

        console.log(
          `✅ [UserExploreService] Real-time update: ${users.length} users`
        );
        callback(users);
      },
      (error) => {
        console.error(
          "❌ [UserExploreService] Real-time subscription error:",
          error
        );
      }
    );

    return unsubscribe;
  }

  /**
   * Fetch a specific user by ID
   */
  async getUserById(userId: string): Promise<UserProfile | null> {
    try {
      console.log(`🔍 [UserExploreService] Fetching user ${userId}...`);

      const userDocRef = doc(firestore, this.USERS_COLLECTION, userId);
      const userDoc = await getDoc(userDocRef);

      if (!userDoc.exists()) {
        console.warn(`⚠️ [UserExploreService] User ${userId} not found`);
        return null;
      }

      const user = await this.mapFirestoreToUserProfile(
        userDoc.id,
        userDoc.data()
      );
      console.log(`✅ [UserExploreService] Fetched user ${userId}`);
      return user;
    } catch (error) {
      console.error(
        `❌ [UserExploreService] Error fetching user ${userId}:`,
        error
      );
      return null;
    }
  }

  /**
   * Search users by username or display name
   * Note: This is a simple client-side filter. For production,
   * consider using Algolia or similar for better search performance.
   */
  async searchUsers(searchQuery: string): Promise<UserProfile[]> {
    try {
      const allUsers = await this.getAllUsers();
      const query = searchQuery.toLowerCase();

      return allUsers.filter(
        (user) =>
          user.username.toLowerCase().includes(query) ||
          user.displayName.toLowerCase().includes(query)
      );
    } catch (error) {
      console.error("❌ [UserExploreService] Error searching users:", error);
      throw new Error("Failed to search users");
    }
  }

  /**
   * Map Firestore document data to UserProfile
   */
  private async mapFirestoreToUserProfile(
    userId: string,
    data: any
  ): Promise<UserProfile | null> {
    try {
      // Get user's display name and avatar from Firebase Auth data or Firestore
      const displayName = data.displayName || data.name || "Anonymous User";
      const username =
        data.username || data.email?.split("@")[0] || userId.substring(0, 8);
      const avatar = data.photoURL || data.avatar || undefined;

      // Get counts from subcollections or denormalized fields
      const sequenceCount = data.sequenceCount || 0;
      const collectionCount = data.collectionCount || 0;
      const followerCount = data.followerCount || 0;

      // Get join date from createdAt timestamp or use current date
      const joinedDate =
        data.createdAt?.toDate?.()?.toISOString() || new Date().toISOString();

      return {
        id: userId,
        username,
        displayName,
        avatar,
        email: data.email,
        sequenceCount,
        collectionCount,
        followerCount,
        joinedDate,
        isFollowing: false, // TODO: Implement following logic
      };
    } catch (error) {
      console.error(
        `❌ [UserExploreService] Error mapping user ${userId}:`,
        error
      );
      return null;
    }
  }
}
