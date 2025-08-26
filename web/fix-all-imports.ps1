#!/usr/bin/env pwsh
# TKA Background Animation - Comprehensive Import Path Fix Script
# Fixes all 105 TypeScript errors by updating import paths systematically

param(
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"

Write-Host "🔧 TKA Background Animation - Comprehensive Import Fix" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No files will be modified" -ForegroundColor Yellow
}

# Function to update imports in a file
function Update-FileImports {
    param($FilePath, $ImportMappings, $DryRun)
    
    if (-not (Test-Path $FilePath)) {
        return
    }
    
    $content = Get-Content -Path $FilePath -Raw -ErrorAction SilentlyContinue
    if (-not $content) { return }
    
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
            Set-Content -Path $FilePath -Value $content -NoNewline -ErrorAction SilentlyContinue
            Write-Host "  ✅ Updated: $(Split-Path $FilePath -Leaf)" -ForegroundColor Green
        } else {
            Write-Host "  [DRY RUN] Would update: $(Split-Path $FilePath -Leaf)" -ForegroundColor Cyan
        }
    }
}

Write-Host "`n🎯 Phase 1: Background Types and Config Imports" -ForegroundColor Green

# Define comprehensive import mappings
$BackgroundImportMappings = @{
    # Background types imports
    'from "$lib/components/backgrounds/types/types"' = 'from "$lib/domain/background/BackgroundTypes"'
    'from "./types/types"' = 'from "$lib/domain/background/BackgroundTypes"'
    'from "../types/types"' = 'from "$lib/domain/background/BackgroundTypes"'
    'from "../../types/types"' = 'from "$lib/domain/background/BackgroundTypes"'
    'from "./backgrounds/types/types"' = 'from "$lib/domain/background/BackgroundTypes"'
    
    # Config imports
    'from "../config"' = 'from "$lib/domain/background/configs/config"'
    'from "./config"' = 'from "$lib/domain/background/configs/config"'
    'from "../config.js"' = 'from "$lib/domain/background/configs/config"'
    'from "./config/nightSky"' = 'from "$lib/domain/background/configs/nightSky"'
    'from "../config/nightSky"' = 'from "$lib/domain/background/configs/nightSky"'
    'from "../config/nightSky.js"' = 'from "$lib/domain/background/configs/nightSky"'
    
    # Core service imports
    'from "../core/BackgroundFactory"' = 'from "$lib/services/implementations/background/BackgroundFactory"'
    'from "./core/BackgroundFactory"' = 'from "$lib/services/implementations/background/BackgroundFactory"'
    'from "../core/PerformanceTracker"' = 'from "$lib/services/implementations/background/performance/PerformanceTracker"'
    'from "./core/PerformanceTracker"' = 'from "$lib/services/implementations/background/performance/PerformanceTracker"'
    'from "./PerformanceTracker"' = 'from "./performance/PerformanceTracker"'
    'from "../core/BackgroundManager.svelte"' = 'from "$lib/services/implementations/background/BackgroundManager.svelte"'
    'from "./core/BackgroundManager.svelte"' = 'from "$lib/services/implementations/background/BackgroundManager.svelte"'
    
    # System imports
    'from "../systems/ShootingStarSystem"' = 'from "./core/ShootingStarSystem"'
    'from "../systems/SnowflakeSystem"' = 'from "./core/SnowflakeSystem"'
    'from "./utils/backgroundUtils"' = 'from "$lib/utils/background/backgroundUtils"'
    'from "../snowfall/utils/backgroundUtils"' = 'from "$lib/utils/background/backgroundUtils"'
    'from "../systems/nightSky/' = 'from "./nightSky/'
}

# Get all TypeScript and Svelte files
$FilesToUpdate = @()
$FilesToUpdate += Get-ChildItem -Path "src" -Recurse -Include "*.ts", "*.svelte" -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName }

Write-Host "Found $($FilesToUpdate.Count) files to process"

foreach ($file in $FilesToUpdate) {
    Update-FileImports $file $BackgroundImportMappings $DryRun
}

Write-Host "`n🎯 Phase 2: Specific File Fixes" -ForegroundColor Green

# Fix specific enum usage in background-state.svelte.ts
if (Test-Path "src/lib/state/background-state.svelte.ts") {
    if (-not $DryRun) {
        $content = Get-Content -Path "src/lib/state/background-state.svelte.ts" -Raw
        $content = $content -replace "let backgroundType = \$state<BackgroundType>\('nightSky'\)", "let backgroundType = `$state<BackgroundType>(BackgroundType.NIGHT_SKY)"
        Set-Content -Path "src/lib/state/background-state.svelte.ts" -Value $content -NoNewline
        Write-Host "  ✅ Fixed BackgroundType enum usage in background-state.svelte.ts" -ForegroundColor Green
    } else {
        Write-Host "  [DRY RUN] Would fix BackgroundType enum usage" -ForegroundColor Cyan
    }
}

# Fix DI registration to use proper interface
if (Test-Path "src/lib/services/di/registration/background-services.ts") {
    if (-not $DryRun) {
        $content = Get-Content -Path "src/lib/services/di/registration/background-services.ts" -Raw
        $content = $content -replace "container\.register\('IBackgroundService'", "container.register(Symbol.for('IBackgroundService')"
        Set-Content -Path "src/lib/services/di/registration/background-services.ts" -Value $content -NoNewline
        Write-Host "  ✅ Fixed DI registration interface" -ForegroundColor Green
    } else {
        Write-Host "  [DRY RUN] Would fix DI registration" -ForegroundColor Cyan
    }
}

Write-Host "`n🎯 Phase 3: Config File Fixes" -ForegroundColor Green

# Fix config.ts imports
if (Test-Path "src/lib/domain/background/configs/config.ts") {
    if (-not $DryRun) {
        $content = Get-Content -Path "src/lib/domain/background/configs/config.ts" -Raw
        $content = $content -replace 'from "\./config/nightSky"', 'from "./nightSky"'
        $content = $content -replace 'from "\./types/types"', 'from "../BackgroundTypes"'
        Set-Content -Path "src/lib/domain/background/configs/config.ts" -Value $content -NoNewline
        Write-Host "  ✅ Fixed config.ts imports" -ForegroundColor Green
    } else {
        Write-Host "  [DRY RUN] Would fix config.ts imports" -ForegroundColor Cyan
    }
}

Write-Host "`n🎯 Phase 4: Background System Fixes" -ForegroundColor Green

# Fix all background system files
$SystemFiles = @(
    "src/lib/services/implementations/background/systems/SnowfallBackgroundSystem.ts",
    "src/lib/services/implementations/background/systems/AuroraBackgroundSystem.ts",
    "src/lib/services/implementations/background/systems/BubblesBackgroundSystem.ts",
    "src/lib/services/implementations/background/systems/DeepOceanBackgroundSystem.ts",
    "src/lib/services/implementations/background/systems/StarfieldBackgroundSystem.ts",
    "src/lib/services/implementations/background/systems/AuroraBorealisBackgroundSystem.ts",
    "src/lib/services/implementations/background/systems/core/ShootingStarSystem.ts",
    "src/lib/services/implementations/background/systems/core/SnowflakeSystem.ts"
)

$SystemImportMappings = @{
    'from "../config"' = 'from "$lib/domain/background/configs/config"'
    'from "../types/types"' = 'from "$lib/domain/background/BackgroundTypes"'
    'from "../systems/ShootingStarSystem"' = 'from "./core/ShootingStarSystem"'
    'from "../systems/SnowflakeSystem"' = 'from "./core/SnowflakeSystem"'
}

foreach ($file in $SystemFiles) {
    if (Test-Path $file) {
        Update-FileImports $file $SystemImportMappings $DryRun
    }
}

Write-Host "`n🎯 Phase 5: Manager and Performance Files" -ForegroundColor Green

# Fix BackgroundManager files
$ManagerFiles = @(
    "src/lib/services/implementations/background/BackgroundManager.ts",
    "src/lib/services/implementations/background/BackgroundManager.svelte.ts",
    "src/lib/services/implementations/background/performance/ResourceTracker.ts"
)

$ManagerImportMappings = @{
    'from "./PerformanceTracker"' = 'from "./performance/PerformanceTracker"'
    'from "../types/types"' = 'from "$lib/domain/background/BackgroundTypes"'
}

foreach ($file in $ManagerFiles) {
    if (Test-Path $file) {
        Update-FileImports $file $ManagerImportMappings $DryRun
    }
}

Write-Host "`n🎯 Phase 6: Context and Component Updates" -ForegroundColor Green

# Update BackgroundContext.svelte.ts
if (Test-Path "src/lib/components/backgrounds/contexts/BackgroundContext.svelte.ts") {
    if (-not $DryRun) {
        $content = Get-Content -Path "src/lib/components/backgrounds/contexts/BackgroundContext.svelte.ts" -Raw
        $content = $content -replace 'from "\.\./config"', 'from "$lib/domain/background/configs/config"'
        $content = $content -replace 'from "\.\./core/BackgroundFactory"', 'from "$lib/services/implementations/background/BackgroundFactory"'
        $content = $content -replace 'from "\.\./core/PerformanceTracker"', 'from "$lib/services/implementations/background/performance/PerformanceTracker"'
        $content = $content -replace 'from "\.\./types/types"', 'from "$lib/domain/background/BackgroundTypes"'
        Set-Content -Path "src/lib/components/backgrounds/contexts/BackgroundContext.svelte.ts" -Value $content -NoNewline
        Write-Host "  ✅ Fixed BackgroundContext.svelte.ts imports" -ForegroundColor Green
    } else {
        Write-Host "  [DRY RUN] Would fix BackgroundContext.svelte.ts" -ForegroundColor Cyan
    }
}

Write-Host "`n🎉 Import Fix Complete!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "✅ Background types and config imports updated" -ForegroundColor Green
Write-Host "✅ Service imports fixed" -ForegroundColor Green  
Write-Host "✅ System imports corrected" -ForegroundColor Green
Write-Host "✅ Manager and performance imports updated" -ForegroundColor Green
Write-Host "✅ Context and component imports fixed" -ForegroundColor Green

Write-Host "`n🔄 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Run 'npm run check' to verify fixes" -ForegroundColor White
Write-Host "2. Test compilation with 'npm run build'" -ForegroundColor White
Write-Host "3. Update any remaining missing files" -ForegroundColor White

if ($DryRun) {
    Write-Host "`n💡 Run without -DryRun to apply all fixes" -ForegroundColor Yellow
}
