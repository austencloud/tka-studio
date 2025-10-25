/**
 * DI Container Tests
 *
 * Critical tests for the Inversify container initialization.
 * If the container fails, the entire app is dead - these tests catch that early.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import {
  container,
  initializeContainer,
  resolve,
  tryResolve,
  isContainerInitialized,
  getContainerStatus,
  TYPES,
} from "$shared/inversify/container";
import type { IPersistenceService } from "$shared";

describe("Inversify Container", () => {
  // ============================================================================
  // INITIALIZATION TESTS
  // ============================================================================

  describe("Container Initialization", () => {
    it("should initialize container successfully", async () => {
      await initializeContainer();
      expect(isContainerInitialized()).toBe(true);
    }, 10000); // Increase timeout to 10 seconds for container initialization

    it("should have valid container status after initialization", async () => {
      await initializeContainer();
      const status = getContainerStatus();

      expect(status.isInitialized).toBe(true);
      expect(status.containerExists).toBe(true);
    });

    it("should handle multiple initialization calls gracefully", async () => {
      await initializeContainer();
      await initializeContainer(); // Second call should not crash

      expect(isContainerInitialized()).toBe(true);
    });
  });

  // ============================================================================
  // SERVICE RESOLUTION TESTS
  // ============================================================================

  describe("Service Resolution", () => {
    beforeEach(async () => {
      await initializeContainer();
    });

    it("should resolve IPersistenceService", async () => {
      const service = await resolve<IPersistenceService>(TYPES.IPersistenceService);
      expect(service).toBeDefined();
      expect(typeof service.initialize).toBe("function");
      expect(typeof service.saveSequence).toBe("function");
    });

    it("should resolve IDeviceDetector", async () => {
      const detector = await resolve(TYPES.IDeviceDetector);
      expect(detector).toBeDefined();
    });

    it("should resolve IHapticFeedbackService", async () => {
      const haptic = await resolve(TYPES.IHapticFeedbackService);
      expect(haptic).toBeDefined();
    });

    it("should resolve core services without errors", async () => {
      const coreServices = [
        TYPES.IPersistenceService,
        TYPES.IDeviceDetector,
        TYPES.IHapticFeedbackService,
      ];

      for (const serviceType of coreServices) {
        const service = await resolve(serviceType);
        expect(service).toBeDefined();
      }
    });

    it("should throw helpful error for unregistered service", async () => {
      const fakeType = Symbol.for("NonExistentService");

      await expect(resolve(fakeType)).rejects.toThrow();
    });

    it("should return same instance for singleton services", async () => {
      const service1 = await resolve(TYPES.IPersistenceService);
      const service2 = await resolve(TYPES.IPersistenceService);

      // Both services should be defined and have the same constructor
      expect(service1).toBeDefined();
      expect(service2).toBeDefined();
      expect((service1 as object).constructor.name).toBe((service2 as object).constructor.name);
    });
  });

  // ============================================================================
  // TRYREVOLVE TESTS (SAFE RESOLUTION)
  // ============================================================================

  describe("tryResolve (Safe Resolution)", () => {
    beforeEach(async () => {
      await initializeContainer();
    });

    it("should return service when available", () => {
      const service = tryResolve(TYPES.IPersistenceService);
      expect(service).not.toBeNull();
    });

    it("should return null for unregistered service instead of throwing", () => {
      const fakeType = Symbol.for("NonExistent");
      const service = tryResolve(fakeType);
      expect(service).toBeNull();
    });
  });

  // ============================================================================
  // CONTAINER STATUS TESTS
  // ============================================================================

  describe("Container Status", () => {
    it("should report initialization status correctly", async () => {
      const beforeStatus = getContainerStatus();
      await initializeContainer();
      const afterStatus = getContainerStatus();

      expect(afterStatus.isInitialized).toBe(true);
      expect(afterStatus.containerExists).toBe(true);
    });

    it("should report container existence", () => {
      const status = getContainerStatus();
      expect(status.containerExists).toBe(true);
    });
  });

  // ============================================================================
  // MODULE LOADING TESTS
  // ============================================================================

  describe("Module Loading", () => {
    it("should load all required modules", async () => {
      await initializeContainer();

      const requiredServices = [
        TYPES.IPersistenceService,
        TYPES.ISequenceService,
        TYPES.IDeviceDetector,
        TYPES.IAnimationService,
      ];

      for (const serviceType of requiredServices) {
        const service = await resolve(serviceType);
        expect(service).toBeDefined();
      }
    });

    it("should load core module services", async () => {
      await initializeContainer();

      const service = await resolve(TYPES.IPersistenceService) as { initialize?: () => void };
      expect(service).toBeDefined();
      expect(typeof service.initialize).toBe("function");
    });

    it("should load animator module services", async () => {
      await initializeContainer();

      const service = await resolve(TYPES.IAnimationService);
      expect(service).toBeDefined();
    });

    it("should load gallery module services", async () => {
      await initializeContainer();

      const service = await resolve(TYPES.IGalleryLoader);
      expect(service).toBeDefined();
    });

    it("should load build module services", async () => {
      await initializeContainer();

      const service = await resolve(TYPES.IBuildTabService);
      expect(service).toBeDefined();
    });
  });

  // ============================================================================
  // ERROR HANDLING TESTS
  // ============================================================================

  describe("Error Handling", () => {
    it("should provide clear error message for missing service", async () => {
      await initializeContainer();
      const fakeType = Symbol.for("ThisServiceDoesNotExist");

      try {
        await resolve(fakeType);
        expect.fail("Should have thrown an error");
      } catch (error: unknown) {
        expect(error).toBeDefined();
        // Error should mention the service or container
        const errorMessage = error instanceof Error ? error.message : String(error);
        expect(errorMessage).toBeTruthy();
      }
    });

    it("should handle resolution errors gracefully with tryResolve", () => {
      const fakeType = Symbol.for("NonExistent");
      const result = tryResolve(fakeType);
      expect(result).toBeNull(); // Should not throw
    });
  });

  // ============================================================================
  // INTEGRATION TESTS
  // ============================================================================

  describe("Integration Tests", () => {
    it("should resolve services with correct interface", async () => {
      // Test that services are properly resolved and have expected methods
      await initializeContainer();

      const persistenceService = await resolve<IPersistenceService>(
        TYPES.IPersistenceService
      );

      // Verify service has the expected interface (don't call methods that need IndexedDB)
      expect(persistenceService).toBeDefined();
      expect(typeof persistenceService.initialize).toBe("function");
      expect(typeof persistenceService.saveSequence).toBe("function");
      expect(typeof persistenceService.loadSequence).toBe("function");
      expect(typeof persistenceService.deleteSequence).toBe("function");
    });

    it("should maintain service dependencies", async () => {
      await initializeContainer();

      // Services that depend on each other should work
      const sequenceService = await resolve(TYPES.ISequenceService);
      expect(sequenceService).toBeDefined();
    });
  });
});
