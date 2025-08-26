#!/usr/bin/env pwsh
# TKA Background Animation Architecture Migration Script - Phase 2
# Fixes import paths and creates service layer integration

param(
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"

Write-Host "🎯 TKA Background Animation Architecture Migration - Phase 2" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "🔧 Fixing import paths and creating service integration" -ForegroundColor Green

if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No files will be modified" -ForegroundColor Yellow
}

# Define import path mappings
$ImportMappings = @{
    # Types imports
    'from "../types/types"' = 'from "$lib/domain/background/BackgroundTypes"'
    'from "../types/types.js"' = 'from "$lib/domain/background/BackgroundTypes"'
    
    # Config imports
    'from "../config"' = 'from "$lib/domain/background/configs/config"'
    'from "../config.js"' = 'from "$lib/domain/background/configs/config"'
    'from "../config/nightSky"' = 'from "$lib/domain/background/configs/nightSky"'
    'from "../config/nightSky.js"' = 'from "$lib/domain/background/configs/nightSky"'
    
    # Background system imports (for BackgroundFactory)
    'from "../nightSky/NightSkyBackgroundSystem"' = 'from "./systems/NightSkyBackgroundSystem"'
    'from "../bubbles/BubblesBackgroundSystem"' = 'from "./systems/BubblesBackgroundSystem"'
    'from "../snowfall/SnowfallBackgroundSystem"' = 'from "./systems/SnowfallBackgroundSystem"'
    'from "../aurora/AuroraBackgroundSystem"' = 'from "./systems/AuroraBackgroundSystem"'
    'from "../auroraBorealis/AuroraBorealisBackgroundSystem"' = 'from "./systems/AuroraBorealisBackgroundSystem"'
    'from "../deepOcean/DeepOceanBackgroundSystem"' = 'from "./systems/DeepOceanBackgroundSystem"'
    'from "../starfield/StarfieldBackgroundSystem"' = 'from "./systems/StarfieldBackgroundSystem"'
    
    # Utility imports
    'from "../snowfall/utils/backgroundUtils"' = 'from "$lib/utils/background/backgroundUtils"'
    
    # System imports (for background systems)
    'from "../systems/ShootingStarSystem"' = 'from "./core/ShootingStarSystem"'
    'from "../systems/SnowflakeSystem"' = 'from "./core/SnowflakeSystem"'
    'from "../systems/nightSky/' = 'from "./nightSky/'
    
    # Performance tracker imports
    'from "./PerformanceTracker"' = 'from "./performance/PerformanceTracker"'
    'from "./ResourceTracker"' = 'from "./performance/ResourceTracker"'
}

# Function to update imports in a file
function Update-FileImports {
    param($FilePath, $DryRun)
    
    if (-not (Test-Path $FilePath)) {
        Write-Host "  ⚠️  File not found: $FilePath" -ForegroundColor Yellow
        return
    }
    
    $content = Get-Content -Path $FilePath -Raw
    $originalContent = $content
    $updated = $false
    
    foreach ($mapping in $ImportMappings.GetEnumerator()) {
        $oldImport = $mapping.Key
        $newImport = $mapping.Value
        
        if ($content -match [regex]::Escape($oldImport)) {
            $content = $content -replace [regex]::Escape($oldImport), $newImport
            $updated = $true
        }
    }
    
    if ($updated) {
        if (-not $DryRun) {
            Set-Content -Path $FilePath -Value $content -NoNewline
            Write-Host "  ✅ Updated imports in: $(Split-Path $FilePath -Leaf)" -ForegroundColor Green
        } else {
            Write-Host "  [DRY RUN] Would update imports in: $(Split-Path $FilePath -Leaf)" -ForegroundColor Cyan
        }
    } else {
        Write-Host "  ℹ️  No import updates needed: $(Split-Path $FilePath -Leaf)" -ForegroundColor Gray
    }
}

Write-Host "`n🔄 Updating import paths in moved files..." -ForegroundColor Green

# Files to update
$FilesToUpdate = @(
    "src/lib/services/implementations/background/BackgroundFactory.ts",
    "src/lib/services/implementations/background/BackgroundManager.ts",
    "src/lib/services/implementations/background/BackgroundManager.svelte.ts",
    "src/lib/services/implementations/background/performance/PerformanceTracker.ts",
    "src/lib/services/implementations/background/performance/ResourceTracker.ts",
    "src/lib/services/implementations/background/systems/NightSkyBackgroundSystem.ts",
    "src/lib/services/implementations/background/systems/BubblesBackgroundSystem.ts",
    "src/lib/services/implementations/background/systems/SnowfallBackgroundSystem.ts",
    "src/lib/services/implementations/background/systems/AuroraBackgroundSystem.ts",
    "src/lib/services/implementations/background/systems/AuroraBorealisBackgroundSystem.ts",
    "src/lib/services/implementations/background/systems/DeepOceanBackgroundSystem.ts",
    "src/lib/services/implementations/background/systems/StarfieldBackgroundSystem.ts",
    "src/lib/services/implementations/background/systems/core/ShootingStarSystem.ts",
    "src/lib/services/implementations/background/systems/core/SnowflakeSystem.ts"
)

foreach ($file in $FilesToUpdate) {
    Update-FileImports $file $DryRun
}

Write-Host "`n📋 Creating service interfaces..." -ForegroundColor Green

# Create IBackgroundService interface
$backgroundServiceInterface = @'
// Background Animation Service Interface
export interface IBackgroundService {
  createSystem(type: BackgroundType, quality: QualityLevel): Promise<BackgroundSystem>;
  getSupportedTypes(): BackgroundType[];
  detectOptimalQuality(): QualityLevel;
  getSystemMetrics(system: BackgroundSystem): PerformanceMetrics | null;
}

// Background Performance Service Interface  
export interface IBackgroundPerformanceService {
  trackPerformance(system: BackgroundSystem): PerformanceMetrics;
  optimizeQuality(currentMetrics: PerformanceMetrics): QualityLevel;
  getRecommendations(metrics: PerformanceMetrics): string[];
}
'@

if (-not $DryRun) {
    # Add to existing interfaces file
    $interfacesPath = "src/lib/services/interfaces.ts"
    if (Test-Path $interfacesPath) {
        Add-Content -Path $interfacesPath -Value "`n$backgroundServiceInterface"
        Write-Host "  ✅ Added background service interfaces to interfaces.ts" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  interfaces.ts not found, creating separate interface file" -ForegroundColor Yellow
        Set-Content -Path "src/lib/services/interfaces/background-interfaces.ts" -Value $backgroundServiceInterface
        Write-Host "  ✅ Created background-interfaces.ts" -ForegroundColor Green
    }
} else {
    Write-Host "  [DRY RUN] Would add background service interfaces" -ForegroundColor Cyan
}

Write-Host "`n🏗️ Creating BackgroundService implementation..." -ForegroundColor Green

$backgroundServiceImpl = @'
import { BackgroundFactory } from './BackgroundFactory';
import { detectAppropriateQuality } from '$lib/domain/background/configs/config';
import type { 
  IBackgroundService, 
  BackgroundType, 
  QualityLevel, 
  BackgroundSystem,
  PerformanceMetrics
} from '$lib/domain/background/BackgroundTypes';

export class BackgroundService implements IBackgroundService {
  async createSystem(type: BackgroundType, quality: QualityLevel): Promise<BackgroundSystem> {
    return BackgroundFactory.createBackgroundSystem({
      type,
      initialQuality: quality
    });
  }
  
  getSupportedTypes(): BackgroundType[] {
    return [
      BackgroundType.NIGHT_SKY,
      BackgroundType.SNOWFALL,
      BackgroundType.AURORA,
      BackgroundType.BUBBLES,
      BackgroundType.DEEP_OCEAN
    ];
  }
  
  detectOptimalQuality(): QualityLevel {
    return detectAppropriateQuality();
  }
  
  getSystemMetrics(system: BackgroundSystem): PerformanceMetrics | null {
    if (system.getMetrics) {
      return system.getMetrics();
    }
    return null;
  }
}
'@

if (-not $DryRun) {
    Set-Content -Path "src/lib/services/implementations/background/BackgroundService.ts" -Value $backgroundServiceImpl
    Write-Host "  ✅ Created BackgroundService.ts" -ForegroundColor Green
} else {
    Write-Host "  [DRY RUN] Would create BackgroundService.ts" -ForegroundColor Cyan
}

Write-Host "`n🎭 Creating runes-based state management..." -ForegroundColor Green

$backgroundState = @'
import { resolve } from '$lib/services/bootstrap';
import type { 
  BackgroundType, 
  QualityLevel, 
  PerformanceMetrics,
  BackgroundSystem 
} from '$lib/domain/background/BackgroundTypes';

export function createBackgroundState() {
  // Get services from DI container
  const backgroundService = resolve('IBackgroundService');
  
  // Runes-based reactive state
  let backgroundType = $state<BackgroundType>('nightSky');
  let quality = $state<QualityLevel>('medium');
  let isLoading = $state(true);
  let currentSystem = $state<BackgroundSystem | null>(null);
  let metrics = $state<PerformanceMetrics>({ fps: 60, warnings: [] });
  
  // Derived state
  let isReady = $derived(currentSystem !== null && !isLoading);
  let hasWarnings = $derived(metrics.warnings.length > 0);
  let shouldOptimize = $derived(metrics.fps < 30);
  
  return {
    // State getters
    get backgroundType() { return backgroundType; },
    get quality() { return quality; },
    get isLoading() { return isLoading; },
    get currentSystem() { return currentSystem; },
    get metrics() { return metrics; },
    get isReady() { return isReady; },
    get hasWarnings() { return hasWarnings; },
    get shouldOptimize() { return shouldOptimize; },
    
    // Actions
    async setBackgroundType(newType: BackgroundType) {
      isLoading = true;
      try {
        backgroundType = newType;
        currentSystem = await backgroundService.createSystem(newType, quality);
      } finally {
        isLoading = false;
      }
    },
    
    async setQuality(newQuality: QualityLevel) {
      quality = newQuality;
      if (currentSystem) {
        currentSystem.setQuality(newQuality);
      }
    },
    
    updateMetrics(newMetrics: PerformanceMetrics) {
      metrics = newMetrics;
    },
    
    async optimizePerformance() {
      if (shouldOptimize && currentSystem) {
        const optimalQuality = backgroundService.detectOptimalQuality();
        await this.setQuality(optimalQuality);
      }
    }
  };
}
'@

if (-not $DryRun) {
    Set-Content -Path "src/lib/state/background-state.svelte.ts" -Value $backgroundState
    Write-Host "  ✅ Created background-state.svelte.ts" -ForegroundColor Green
} else {
    Write-Host "  [DRY RUN] Would create background-state.svelte.ts" -ForegroundColor Cyan
}

Write-Host "`n🔧 Creating DI container registration..." -ForegroundColor Green

$diRegistration = @'
// Add to src/lib/services/di/registration/background-services.ts
import { BackgroundService } from '../../implementations/background/BackgroundService';
import type { ServiceContainer } from '../ServiceContainer';

export async function registerBackgroundServices(container: ServiceContainer): Promise<void> {
  // Register background animation services
  container.register('IBackgroundService', BackgroundService);
  
  console.log('✅ Background services registered');
}
'@

if (-not $DryRun) {
    New-Item -ItemType Directory -Path "src/lib/services/di/registration" -Force | Out-Null
    Set-Content -Path "src/lib/services/di/registration/background-services.ts" -Value $diRegistration
    Write-Host "  ✅ Created background-services.ts registration" -ForegroundColor Green
} else {
    Write-Host "  [DRY RUN] Would create background-services.ts registration" -ForegroundColor Cyan
}

Write-Host "`n🎉 Phase 2 Migration Complete!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "✅ Import paths updated in all moved files" -ForegroundColor Green
Write-Host "✅ Service interfaces created" -ForegroundColor Green  
Write-Host "✅ BackgroundService implementation created" -ForegroundColor Green
Write-Host "✅ Runes-based state management created" -ForegroundColor Green
Write-Host "✅ DI container registration prepared" -ForegroundColor Green

Write-Host "`n🔄 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Update bootstrap.ts to register background services" -ForegroundColor White
Write-Host "2. Update BackgroundCanvas.svelte to use new architecture" -ForegroundColor White
Write-Host "3. Test compilation and functionality" -ForegroundColor White
Write-Host "4. Verify visual output matches original" -ForegroundColor White

if ($DryRun) {
    Write-Host "`n💡 Run without -DryRun to execute Phase 2" -ForegroundColor Yellow
}
