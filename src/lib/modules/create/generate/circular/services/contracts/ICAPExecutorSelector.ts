import type { CAPType } from "../../domain/models/circular-models";
import type { ICAPExecutor } from "./ICAPExecutor";

/**
 * Service for selecting the appropriate CAP executor based on CAP type
 *
 * Maps CAP type enums to their corresponding executor implementations,
 * providing a clean interface for the generation orchestration service
 * to access the correct transformation logic.
 */
export interface ICAPExecutorSelector {
  /**
   * Get the appropriate CAP executor for the given CAP type
   *
   * @param capType - The CAP type enum value (e.g., STRICT_ROTATED, STRICT_MIRRORED)
   * @returns The executor instance for this CAP type
   * @throws Error if the CAP type is not supported
   */
  getExecutor(capType: CAPType): ICAPExecutor;

  /**
   * Check if a CAP type is supported
   *
   * @param capType - The CAP type to check
   * @returns True if an executor exists for this type
   */
  isSupported(capType: CAPType): boolean;
}
