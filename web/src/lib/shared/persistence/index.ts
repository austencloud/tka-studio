/**
 * Persistence Module Barrel Export
 *
 * This file exports everything you need from the persistence module.
 * Import from here to get access to the database, services, and domain models.
 */

// Domain exports (models, enums, constants, types)
export * from './domain';

// Database
export { clearAllData, db, getDatabaseInfo, initializeDatabase, TKADatabase } from './database/TKADatabase';

// Service contracts
export type { IPersistenceService } from './services/contracts/IPersistenceService';

// Service implementations
export { DexiePersistenceService } from './services/implementations/DexiePersistenceService';
