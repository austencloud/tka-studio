/**
 * Notification Service Implementation
 *
 * Handles achievement unlock notifications, level-ups, and toast messages.
 * Uses both Firestore (persistent history) and Svelte 5 runes (reactive UI).
 */

import { injectable } from "inversify";
import {
  collection,
  doc,
  setDoc,
  getDocs,
  query,
  where,
  orderBy,
  limit,
  updateDoc,
  writeBatch,
  serverTimestamp,
} from "firebase/firestore";
import { auth, firestore } from "../../../auth/firebase";
import { db } from "../../../persistence/database/TKADatabase";
import { getUserNotificationsPath } from "../../data/firestore-collections";
import type { AchievementNotification } from "../../domain/models";
import type { INotificationService } from "../contracts";
import { getMilestoneForLevel } from "../../domain/constants";
import {
  addNotification,
  clearNotifications,
} from "../../state/notification-state.svelte";

@injectable()
export class NotificationService implements INotificationService {
  // ============================================================================
  // SHOW NOTIFICATIONS
  // ============================================================================

  async showAchievementUnlock(
    achievementId: string,
    title: string,
    icon: string,
    xpGained: number
  ): Promise<void> {
    const notification: AchievementNotification = {
      id: `achievement_${achievementId}_${Date.now()}`,
      type: "achievement",
      title: "Achievement Unlocked!",
      message: `${icon} ${title} (+${xpGained} XP)`,
      icon,
      timestamp: new Date(),
      isRead: false,
      data: {
        achievementId,
        xpGained,
      },
    };

    await this.saveAndQueueNotification(notification);

    console.log(`🎉 Achievement notification: ${title}`);
  }

  async showLevelUp(newLevel: number, milestoneTitle?: string): Promise<void> {
    // Check for milestone rewards
    const milestone = getMilestoneForLevel(newLevel);
    const title = milestone?.title || milestoneTitle;

    const notification: AchievementNotification = {
      id: `level_${newLevel}_${Date.now()}`,
      type: "level_up",
      title: "Level Up!",
      message: title
        ? `${milestone?.icon || "⭐"} Level ${newLevel}: ${title}`
        : `⭐ You've reached Level ${newLevel}!`,
      icon: milestone?.icon || "⭐",
      timestamp: new Date(),
      isRead: false,
      data: {
        newLevel,
        milestoneTitle: title,
      },
    };

    await this.saveAndQueueNotification(notification);

    console.log(`📈 Level up notification: Level ${newLevel}`);
  }

  async showChallengeComplete(
    challengeTitle: string,
    xpGained: number
  ): Promise<void> {
    const notification: AchievementNotification = {
      id: `challenge_${Date.now()}`,
      type: "challenge_complete",
      title: "Daily Challenge Complete!",
      message: `🎯 ${challengeTitle} (+${xpGained} XP)`,
      icon: "🎯",
      timestamp: new Date(),
      isRead: false,
      data: {
        challengeTitle,
        xpGained,
      },
    };

    await this.saveAndQueueNotification(notification);

    console.log(`🎯 Challenge completion notification: ${challengeTitle}`);
  }

  async showStreakMilestone(streakDays: number): Promise<void> {
    const getStreakIcon = (days: number): string => {
      if (days >= 100) return "⭐";
      if (days >= 30) return "💪";
      if (days >= 7) return "📅";
      return "🔥";
    };

    const getStreakMessage = (days: number): string => {
      if (days >= 100) return "Legendary 100-Day Streak!";
      if (days >= 30) return "Amazing 30-Day Streak!";
      if (days >= 7) return "One Week Streak!";
      return `${days}-Day Streak!`;
    };

    const notification: AchievementNotification = {
      id: `streak_${streakDays}_${Date.now()}`,
      type: "streak_milestone",
      title: "Streak Milestone!",
      message: `${getStreakIcon(streakDays)} ${getStreakMessage(streakDays)}`,
      icon: getStreakIcon(streakDays),
      timestamp: new Date(),
      isRead: false,
      data: {
        streakDays,
      },
    };

    await this.saveAndQueueNotification(notification);

    console.log(`🔥 Streak milestone notification: ${streakDays} days`);
  }

  /**
   * Save notification to Firestore and add to reactive queue
   */
  private async saveAndQueueNotification(
    notification: AchievementNotification
  ): Promise<void> {
    const user = auth.currentUser;

    // Add to reactive queue immediately (for UI)
    addNotification(notification);

    // Save to local DB
    await db.achievementNotifications.add(notification);

    // Save to Firestore if user is logged in
    if (user) {
      try {
        const notificationsPath = getUserNotificationsPath(user.uid);
        const notificationRef = doc(
          firestore,
          `${notificationsPath}/${notification.id}`
        );

        await setDoc(notificationRef, {
          ...notification,
          timestamp: serverTimestamp(),
        });
      } catch (error) {
        console.error("❌ Failed to save notification to Firestore:", error);
        // Don't throw - notification still shown locally
      }
    }
  }

  // ============================================================================
  // NOTIFICATION MANAGEMENT
  // ============================================================================

  async getUnreadNotifications(): Promise<AchievementNotification[]> {
    const user = auth.currentUser;
    if (!user) {
      // Try local DB
      return await db.achievementNotifications
        .filter((n) => n.isRead === false)
        .toArray();
    }

    const notificationsPath = getUserNotificationsPath(user.uid);
    const unreadQuery = query(
      collection(firestore, notificationsPath),
      where("isRead", "==", false),
      orderBy("timestamp", "desc"),
      limit(50)
    );

    const snapshot = await getDocs(unreadQuery);
    return snapshot.docs.map(
      (doc) => ({ ...doc.data(), id: doc.id }) as AchievementNotification
    );
  }

  async markAsRead(notificationId: string): Promise<void> {
    const user = auth.currentUser;

    // Update local DB
    await db.achievementNotifications.update(notificationId, { isRead: true });

    // Update Firestore if user is logged in
    if (user) {
      try {
        const notificationsPath = getUserNotificationsPath(user.uid);
        const notificationRef = doc(
          firestore,
          `${notificationsPath}/${notificationId}`
        );

        await updateDoc(notificationRef, {
          isRead: true,
        });
      } catch (error) {
        console.error("❌ Failed to mark notification as read:", error);
      }
    }
  }

  async markAllAsRead(): Promise<void> {
    const user = auth.currentUser;

    // Update local DB
    const unread = await db.achievementNotifications
      .filter((n) => n.isRead === false)
      .toArray();

    for (const notification of unread) {
      await db.achievementNotifications.update(notification.id, {
        isRead: true,
      });
    }

    // Update Firestore if user is logged in
    if (user) {
      try {
        const notificationsPath = getUserNotificationsPath(user.uid);
        const unreadQuery = query(
          collection(firestore, notificationsPath),
          where("isRead", "==", false)
        );

        const snapshot = await getDocs(unreadQuery);
        const batch = writeBatch(firestore);

        snapshot.docs.forEach((doc) => {
          batch.update(doc.ref, { isRead: true });
        });

        await batch.commit();

        console.log(`✅ Marked ${snapshot.size} notifications as read`);
      } catch (error) {
        console.error("❌ Failed to mark all notifications as read:", error);
      }
    }
  }

  async getNotificationHistory(
    limitCount: number = 50
  ): Promise<AchievementNotification[]> {
    const user = auth.currentUser;
    if (!user) {
      // Try local DB
      return await db.achievementNotifications
        .orderBy("timestamp")
        .reverse()
        .limit(limitCount)
        .toArray();
    }

    const notificationsPath = getUserNotificationsPath(user.uid);
    const historyQuery = query(
      collection(firestore, notificationsPath),
      orderBy("timestamp", "desc"),
      limit(limitCount)
    );

    const snapshot = await getDocs(historyQuery);
    return snapshot.docs.map(
      (doc) => ({ ...doc.data(), id: doc.id }) as AchievementNotification
    );
  }

  async clearAll(): Promise<void> {
    const user = auth.currentUser;

    // Clear local DB
    await db.achievementNotifications.clear();

    // Clear Firestore if user is logged in
    if (user) {
      try {
        const notificationsPath = getUserNotificationsPath(user.uid);
        const allQuery = query(collection(firestore, notificationsPath));

        const snapshot = await getDocs(allQuery);
        const batch = writeBatch(firestore);

        snapshot.docs.forEach((doc) => {
          batch.delete(doc.ref);
        });

        await batch.commit();

        console.log(`🗑️ Cleared ${snapshot.size} notifications`);
      } catch (error) {
        console.error("❌ Failed to clear notifications:", error);
      }
    }

    // Clear notification queue
    clearNotifications();
  }
}
