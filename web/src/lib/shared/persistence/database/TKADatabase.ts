/**
 * TKA Database - Dexie Configuration
 *
 * This is your main database configuration using Dexie.js
 * Think of this as your "database schema" - it defines what tables you have
 * and how they're indexed for fast queries.
 */

import type {
  AppSettings,
  PictographData,
  SequenceData
} from '$shared';
import Dexie, { type EntityTable } from 'dexie';
import {
  DATABASE_NAME,
  DATABASE_VERSION,
  DEFAULT_USER_WORK_VERSION,
  TABLE_INDEXES
} from '../domain/constants';
import type { UserProject, UserWorkData } from '../domain/models';

// ============================================================================
// DATABASE CLASS
// ============================================================================

/**
 * TKA Database Class
 * 
 * This extends Dexie and defines your database structure.
 * Each property represents a "table" in your database.
 */
export class TKADatabase extends Dexie {
  // Define your tables with TypeScript types
  sequences!: EntityTable<SequenceData, 'id'>;
  pictographs!: EntityTable<PictographData, 'id'>;
  userWork!: EntityTable<UserWorkData, 'id'>;
  userProjects!: EntityTable<UserProject, 'id'>;
  settings!: EntityTable<AppSettings & { id: string }, 'id'>;

  constructor() {
    super(DATABASE_NAME);

    // Version 1 schema - this is like a database migration
    this.version(DATABASE_VERSION).stores(TABLE_INDEXES);

    // Optional: Add hooks for automatic timestamps
    this.userWork.hook('creating', function (_primKey, obj, _trans) {
      obj.lastModified = new Date();
      obj.version = obj.version || DEFAULT_USER_WORK_VERSION;
    });

    this.userWork.hook('updating', function (modifications, _primKey, _obj, _trans) {
      (modifications as Partial<UserWorkData>).lastModified = new Date();
    });
  }
}

// ============================================================================
// DATABASE INSTANCE
// ============================================================================

/**
 * Single database instance for your entire app
 * Import this wherever you need database access
 */
export const db = new TKADatabase();

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Initialize database - call this when your app starts
 */
export async function initializeDatabase(): Promise<void> {
  try {
    await db.open();
    console.log('✅ TKA Database initialized successfully');
  } catch (error) {
    console.error('❌ Failed to initialize database:', error);
    throw error;
  }
}

/**
 * Clear all data (useful for development/testing)
 */
export async function clearAllData(): Promise<void> {
  await db.transaction('rw', [db.sequences, db.pictographs, db.userWork, db.userProjects, db.settings], async () => {
    await db.sequences.clear();
    await db.pictographs.clear();
    await db.userWork.clear();
    await db.userProjects.clear();
    await db.settings.clear();
  });
  console.log('🗑️ All database data cleared');
}

/**
 * Get database info for debugging
 */
export async function getDatabaseInfo() {
  const info = {
    sequences: await db.sequences.count(),
    pictographs: await db.pictographs.count(),
    userWork: await db.userWork.count(),
    userProjects: await db.userProjects.count(),
    settings: await db.settings.count(),
  };
  console.log('📊 Database info:', info);
  return info;
}
