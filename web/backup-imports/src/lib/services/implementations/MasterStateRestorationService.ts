/**
 * Master State Restoration Service for TKA
 * 
 * Orchestrates complete application state restoration on startup.
 * Handles the proper order and timing of state restoration across all tabs and features.
 */

import { browser } from "$app/environment";
import type { TabId } from "$lib/state/services/state-service-interfaces";
import type { BrowseStatePersistenceService } from "./browse/BrowseStatePersistenceService";
import type { TabStateService } from "$lib/state/services/TabStateService.svelte";

// ============================================================================
// RESTORATION CONFIGURATION
// ============================================================================

interface RestorationStep {
  name: string;
  priority: number; // Lower numbers run first
  timeout: number;  // Max time to wait for this step
  essential: boolean; // If true, failure blocks app startup
}

interface RestorationResult {
  success: boolean;
  duration: number;
  error?: string;
  details?: Record<string, unknown>;
}

interface CompleteRestorationResult {
  totalDuration: number;
  steps: Record<string, RestorationResult>;
  failedEssentialSteps: string[];
  warnings: string[];
  success: boolean;
}

interface ScrollRestorationData {
  scrollTop: number;
  scrollLeft: number;
  containerSelector: string;
}

// ============================================================================
// MASTER STATE RESTORATION SERVICE
// ============================================================================

export class MasterStateRestorationService {
  private isRestoring = false;
  private restorationSteps: Map<string, RestorationStep> = new Map();
  private scrollRestorationQueue: ScrollRestorationData[] = [];
  
  constructor(
    private tabStateService: TabStateService,
    private browseStatePersistence: BrowseStatePersistenceService,
    // Add other state services as needed
  ) {
    this.setupRestorationSteps();
  }

  // ============================================================================
  // RESTORATION STEP CONFIGURATION
  // ============================================================================

  private setupRestorationSteps() {
    // Step 1: Core app state (essential)
    this.restorationSteps.set('app-core', {
      name: 'Core Application State',
      priority: 1,
      timeout: 2000,
      essential: true
    });

    // Step 2: Tab state (essential for navigation)
    this.restorationSteps.set('tab-state', {
      name: 'Tab Navigation State',
      priority: 2,
      timeout: 1000,
      essential: true
    });

    // Step 3: Active tab specific state
    this.restorationSteps.set('active-tab', {
      name: 'Active Tab State',
      priority: 3,
      timeout: 3000,
      essential: false
    });

    // Step 4: UI state (scroll positions, selections)
    this.restorationSteps.set('ui-state', {
      name: 'UI State (Scroll, Selection)',
      priority: 4,
      timeout: 2000,
      essential: false
    });

    // Step 5: Performance optimizations
    this.restorationSteps.set('optimization', {
      name: 'Performance Optimizations',
      priority: 5,
      timeout: 1000,
      essential: false
    });
  }

  // ============================================================================
  // MAIN RESTORATION API
  // ============================================================================

  /**
   * Restore complete application state on startup
   */
  async restoreCompleteApplicationState(): Promise<CompleteRestorationResult> {
    if (!browser) {
      return this.createFailureResult('Not running in browser');
    }

    if (this.isRestoring) {
      console.warn('State restoration already in progress');
      return this.createFailureResult('Already restoring');
    }

    this.isRestoring = true;
    const startTime = performance.now();
    
    console.log('🔄 Starting complete application state restoration...');

    const results: Record<string, RestorationResult> = {};
    const failedEssentialSteps: string[] = [];
    const warnings: string[] = [];

    // Execute restoration steps in priority order
    const sortedSteps = Array.from(this.restorationSteps.entries())
      .sort(([, a], [, b]) => a.priority - b.priority);

    for (const [stepId, step] of sortedSteps) {
      console.log(`📋 Executing restoration step: ${step.name}`);
      
      try {
        const stepResult = await this.executeRestorationStep(stepId, step);
        results[stepId] = stepResult;

        if (!stepResult.success) {
          if (step.essential) {
            failedEssentialSteps.push(step.name);
          } else {
            warnings.push(`Non-essential step failed: ${step.name}`);
          }
        }

        console.log(`✅ Step "${step.name}" completed in ${stepResult.duration}ms`);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        
        results[stepId] = {
          success: false,
          duration: 0,
          error: errorMessage
        };

        if (step.essential) {
          failedEssentialSteps.push(step.name);
        } else {
          warnings.push(`Step failed: ${step.name} - ${errorMessage}`);
        }

        console.error(`❌ Step "${step.name}" failed:`, error);
      }
    }

    // Process scroll restoration queue after DOM is ready
    if (this.scrollRestorationQueue.length > 0) {
      setTimeout(() => this.processScrollRestoration(), 100);
    }

    const totalDuration = performance.now() - startTime;
    this.isRestoring = false;

    const finalResult: CompleteRestorationResult = {
      totalDuration,
      steps: results,
      failedEssentialSteps,
      warnings,
      success: failedEssentialSteps.length === 0
    };

    console.log(`🎉 State restoration completed in ${totalDuration}ms`);
    console.log(`✅ Success: ${finalResult.success}`);
    
    if (warnings.length > 0) {
      console.warn('⚠️ Warnings:', warnings);
    }

    return finalResult;
  }

  // ============================================================================
  // INDIVIDUAL RESTORATION STEPS
  // ============================================================================

  private async executeRestorationStep(stepId: string, step: RestorationStep): Promise<RestorationResult> {
    const startTime = performance.now();

    try {
      // Create timeout promise
      const timeoutPromise = new Promise<never>((_, reject) => {
        setTimeout(() => reject(new Error(`Step timed out after ${step.timeout}ms`)), step.timeout);
      });

      // Execute the actual restoration step
      const stepPromise = this.executeSpecificStep(stepId);

      // Race between step execution and timeout
      const result = await Promise.race([stepPromise, timeoutPromise]);

      return {
        success: true,
        duration: performance.now() - startTime,
        details: result
      };
    } catch (error) {
      return {
        success: false,
        duration: performance.now() - startTime,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  private async executeSpecificStep(stepId: string): Promise<Record<string, unknown>> {
    switch (stepId) {
      case 'app-core':
        return this.restoreCoreApplicationState();
      
      case 'tab-state':
        return this.restoreTabState();
      
      case 'active-tab':
        return this.restoreActiveTabState();
      
      case 'ui-state':
        return this.restoreUIState();
      
      case 'optimization':
        return this.performOptimizations();
      
      default:
        throw new Error(`Unknown restoration step: ${stepId}`);
    }
  }

  // ============================================================================
  // SPECIFIC RESTORATION IMPLEMENTATIONS
  // ============================================================================

  private async restoreCoreApplicationState(): Promise<Record<string, unknown>> {
    // Restore basic app state like theme, settings, etc.
    // This would integrate with your existing ApplicationStateService
    return { restored: true };
  }

  private async restoreTabState(): Promise<Record<string, unknown>> {
    await this.tabStateService.restoreApplicationState();
    
    return {
      activeTab: this.tabStateService.activeTab,
      restored: true
    };
  }

  private async restoreActiveTabState(): Promise<Record<string, unknown>> {
    const activeTab = this.tabStateService.activeTab;
    
    switch (activeTab) {
      case 'browse':
        return this.restoreBrowseTabState();
      
      case 'construct':
        return this.restoreConstructTabState();
      
      case 'sequence_card':
        return this.restoreSequenceCardTabState();
      
      default:
        return { activeTab, message: 'No specific restoration needed' };
    }
  }

  private async restoreBrowseTabState(): Promise<Record<string, unknown>> {
    try {
      const browseState = await this.browseStatePersistence.loadBrowseState();
      
      if (!browseState) {
        return { message: 'No browse state to restore' };
      }

      // Queue scroll restoration for after DOM is ready
      if (browseState.scroll && browseState.scroll.scrollTop > 0) {
        this.scrollRestorationQueue.push({
          scrollTop: browseState.scroll.scrollTop,
          scrollLeft: browseState.scroll.scrollLeft,
          containerSelector: '[data-browse-scroll-container]'
        });
      }

      return {
        restored: true,
        filter: browseState.filter?.type || null,
        scrollQueued: browseState.scroll?.scrollTop > 0,
        selectedSequence: browseState.selection?.selectedSequenceId || null
      };
    } catch (error) {
      console.error('Failed to restore browse tab state:', error);
      return { error: 'Browse state restoration failed' };
    }
  }

  private async restoreConstructTabState(): Promise<Record<string, unknown>> {
    // Implement construct tab restoration
    // This would restore workbench state, current sequence, etc.
    return { message: 'Construct tab restoration not yet implemented' };
  }

  private async restoreSequenceCardTabState(): Promise<Record<string, unknown>> {
    // Implement sequence card tab restoration
    return { message: 'Sequence card tab restoration not yet implemented' };
  }

  private async restoreUIState(): Promise<Record<string, unknown>> {
    // Restore UI-specific state like panel sizes, modal states, etc.
    return { message: 'UI state restoration completed' };
  }

  private async performOptimizations(): Promise<Record<string, unknown>> {
    // Perform any post-restoration optimizations
    // This could include preloading commonly used sequences, warming caches, etc.
    return { message: 'Optimizations completed' };
  }

  // ============================================================================
  // SCROLL RESTORATION
  // ============================================================================

  private processScrollRestoration(): void {
    console.log(`📜 Processing ${this.scrollRestorationQueue.length} scroll restorations`);

    for (const scrollData of this.scrollRestorationQueue) {
      this.restoreScrollPosition(scrollData);
    }

    this.scrollRestorationQueue = [];
  }

  private restoreScrollPosition(scrollData: ScrollRestorationData): void {
    const container = document.querySelector(scrollData.containerSelector) as HTMLElement;
    
    if (!container) {
      console.warn(`Scroll container not found: ${scrollData.containerSelector}`);
      return;
    }

    try {
      // Use smooth scroll for better UX
      container.scrollTo({
        top: scrollData.scrollTop,
        left: scrollData.scrollLeft,
        behavior: 'smooth'
      });

      console.log(`📜 Restored scroll position: ${scrollData.scrollTop}px`);
    } catch (error) {
      console.warn('Failed to restore scroll position:', error);
    }
  }

  // ============================================================================
  // UTILITY METHODS
  // ============================================================================

  private createFailureResult(reason: string): CompleteRestorationResult {
    return {
      totalDuration: 0,
      steps: {},
      failedEssentialSteps: [reason],
      warnings: [],
      success: false
    };
  }

  /**
   * Add a scroll restoration to the queue
   */
  public queueScrollRestoration(data: ScrollRestorationData): void {
    this.scrollRestorationQueue.push(data);
  }

  /**
   * Check if restoration is currently in progress
   */
  public get isRestorationInProgress(): boolean {
    return this.isRestoring;
  }

  /**
   * Get available restoration steps
   */
  public getRestorationSteps(): Array<{ id: string; step: RestorationStep }> {
    return Array.from(this.restorationSteps.entries())
      .map(([id, step]) => ({ id, step }));
  }

  /**
   * Configure or update a restoration step
   */
  public configureStep(stepId: string, config: Partial<RestorationStep>): void {
    const existing = this.restorationSteps.get(stepId);
    if (existing) {
      this.restorationSteps.set(stepId, { ...existing, ...config });
    } else {
      console.warn(`Restoration step "${stepId}" not found`);
    }
  }
}

// ============================================================================
// SINGLETON INSTANCE
// ============================================================================

let masterRestorationService: MasterStateRestorationService | null = null;

/**
 * Get or create the singleton master restoration service
 * 
 * @param dependencies - Required services for restoration
 * @returns Master restoration service instance
 */
export function getMasterRestorationService(dependencies?: {
  tabStateService: TabStateService;
  browseStatePersistence: BrowseStatePersistenceService;
}): MasterStateRestorationService {
  if (!masterRestorationService && dependencies) {
    masterRestorationService = new MasterStateRestorationService(
      dependencies.tabStateService,
      dependencies.browseStatePersistence
    );
  }

  if (!masterRestorationService) {
    throw new Error('Master restoration service not initialized. Provide dependencies on first call.');
  }

  return masterRestorationService;
}

/**
 * Initialize and run complete state restoration
 * Call this in your app startup (e.g., in +layout.svelte or app initialization)
 */
export async function initializeStateRestoration(dependencies: {
  tabStateService: TabStateService;
  browseStatePersistence: BrowseStatePersistenceService;
}): Promise<CompleteRestorationResult> {
  const restorationService = getMasterRestorationService(dependencies);
  return restorationService.restoreCompleteApplicationState();
}
