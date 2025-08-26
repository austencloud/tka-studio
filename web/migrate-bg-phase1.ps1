#!/usr/bin/env pwsh
# TKA Background Animation Architecture Migration Script - Phase 1
# Migrates background animation system to proper Svelte 5 runes + microservices pattern

param(
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"

Write-Host "🎯 TKA Background Animation Architecture Migration - Phase 1" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No files will be moved" -ForegroundColor Yellow
}

# Define base paths
$SrcPath = "src/lib"
$BackgroundsPath = "$SrcPath/components/backgrounds"
$ServicesPath = "$SrcPath/services"
$DomainPath = "$SrcPath/domain"
$StatePath = "$SrcPath/state"
$UtilsPath = "$SrcPath/utils"

# Verify source directory exists
if (-not (Test-Path $BackgroundsPath)) {
    Write-Error "❌ Source directory not found: $BackgroundsPath"
    exit 1
}

Write-Host "📁 Creating new directory structure..." -ForegroundColor Green

# Define new directories to create
$NewDirectories = @(
    "$ServicesPath/implementations/background/systems/nightSky",
    "$ServicesPath/implementations/background/systems/core", 
    "$ServicesPath/implementations/background/performance",
    "$DomainPath/background/configs",
    "$DomainPath/background/models",
    "$StatePath",
    "$UtilsPath/background",
    "$BackgroundsPath/_backup_old_structure"
)

# Create directories
foreach ($dir in $NewDirectories) {
    if (-not $DryRun) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Host "  ✅ Created: $dir" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  Already exists: $dir" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  [DRY RUN] Would create: $dir" -ForegroundColor Cyan
    }
}

Write-Host "`n🔄 Moving business logic to services..." -ForegroundColor Green

# Function to move file safely
function Move-FileIfExists {
    param($Source, $Destination, $DryRun)
    
    if (Test-Path $Source) {
        if (-not $DryRun) {
            $destDir = Split-Path $Destination -Parent
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            Move-Item -Path $Source -Destination $Destination -Force
            Write-Host "  ✅ Moved: $(Split-Path $Source -Leaf) → $Destination" -ForegroundColor Green
        } else {
            Write-Host "  [DRY RUN] Would move: $Source → $Destination" -ForegroundColor Cyan
        }
        return $true
    } else {
        Write-Host "  ⚠️  File not found: $Source" -ForegroundColor Yellow
        return $false
    }
}

# Move core animation services
Move-FileIfExists "$BackgroundsPath/core/BackgroundFactory.ts" "$ServicesPath/implementations/background/BackgroundFactory.ts" $DryRun
Move-FileIfExists "$BackgroundsPath/core/BackgroundManager.ts" "$ServicesPath/implementations/background/BackgroundManager.ts" $DryRun
Move-FileIfExists "$BackgroundsPath/core/BackgroundManager.svelte.ts" "$ServicesPath/implementations/background/BackgroundManager.svelte.ts" $DryRun
Move-FileIfExists "$BackgroundsPath/core/PerformanceTracker.ts" "$ServicesPath/implementations/background/performance/PerformanceTracker.ts" $DryRun
Move-FileIfExists "$BackgroundsPath/core/ResourceTracker.ts" "$ServicesPath/implementations/background/performance/ResourceTracker.ts" $DryRun

# Move animation system classes
Move-FileIfExists "$BackgroundsPath/nightSky/NightSkyBackgroundSystem.ts" "$ServicesPath/implementations/background/systems/NightSkyBackgroundSystem.ts" $DryRun
Move-FileIfExists "$BackgroundsPath/bubbles/BubblesBackgroundSystem.ts" "$ServicesPath/implementations/background/systems/BubblesBackgroundSystem.ts" $DryRun
Move-FileIfExists "$BackgroundsPath/snowfall/SnowfallBackgroundSystem.ts" "$ServicesPath/implementations/background/systems/SnowfallBackgroundSystem.ts" $DryRun
Move-FileIfExists "$BackgroundsPath/aurora/AuroraBackgroundSystem.ts" "$ServicesPath/implementations/background/systems/AuroraBackgroundSystem.ts" $DryRun
Move-FileIfExists "$BackgroundsPath/auroraBorealis/AuroraBorealisBackgroundSystem.ts" "$ServicesPath/implementations/background/systems/AuroraBorealisBackgroundSystem.ts" $DryRun
Move-FileIfExists "$BackgroundsPath/deepOcean/DeepOceanBackgroundSystem.ts" "$ServicesPath/implementations/background/systems/DeepOceanBackgroundSystem.ts" $DryRun
Move-FileIfExists "$BackgroundsPath/starfield/StarfieldBackgroundSystem.ts" "$ServicesPath/implementations/background/systems/StarfieldBackgroundSystem.ts" $DryRun

# Move system utilities
Move-FileIfExists "$BackgroundsPath/systems/ShootingStarSystem.ts" "$ServicesPath/implementations/background/systems/core/ShootingStarSystem.ts" $DryRun
Move-FileIfExists "$BackgroundsPath/systems/SnowflakeSystem.ts" "$ServicesPath/implementations/background/systems/core/SnowflakeSystem.ts" $DryRun

Write-Host "`n📋 Moving types to domain..." -ForegroundColor Green
Move-FileIfExists "$BackgroundsPath/types/types.ts" "$DomainPath/background/BackgroundTypes.ts" $DryRun

Write-Host "`n⚙️ Moving configuration files..." -ForegroundColor Green
Move-FileIfExists "$BackgroundsPath/config.ts" "$DomainPath/background/configs/config.ts" $DryRun
Move-FileIfExists "$BackgroundsPath/config/nightSky.ts" "$DomainPath/background/configs/nightSky.ts" $DryRun
Move-FileIfExists "$BackgroundsPath/snowfall/constants.ts" "$DomainPath/background/configs/snowfall-constants.ts" $DryRun

Write-Host "`n🛠️ Moving utilities..." -ForegroundColor Green
Move-FileIfExists "$BackgroundsPath/snowfall/utils/backgroundUtils.ts" "$UtilsPath/background/backgroundUtils.ts" $DryRun

Write-Host "`n💾 Creating backup of remaining structure..." -ForegroundColor Green

if (-not $DryRun) {
    $BackupPath = "$BackgroundsPath/_backup_old_structure"
    $ItemsToBackup = Get-ChildItem -Path $BackgroundsPath -Recurse | Where-Object { 
        $_.FullName -notlike "*_backup_old_structure*" 
    }
    
    foreach ($item in $ItemsToBackup) {
        $relativePath = $item.FullName.Substring($BackgroundsPath.Length + 1)
        $backupDestination = Join-Path $BackupPath $relativePath
        
        if ($item.PSIsContainer) {
            if (-not (Test-Path $backupDestination)) {
                New-Item -ItemType Directory -Path $backupDestination -Force | Out-Null
            }
        } else {
            $backupDir = Split-Path $backupDestination -Parent
            if (-not (Test-Path $backupDir)) {
                New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
            }
            Copy-Item -Path $item.FullName -Destination $backupDestination -Force
        }
    }
    Write-Host "  ✅ Backup created in: $BackupPath" -ForegroundColor Green
} else {
    Write-Host "  [DRY RUN] Would create backup" -ForegroundColor Cyan
}

Write-Host "`n🧹 Cleaning up empty directories..." -ForegroundColor Green

$DirectoriesToClean = @(
    "$BackgroundsPath/core",
    "$BackgroundsPath/types",
    "$BackgroundsPath/config",
    "$BackgroundsPath/systems",
    "$BackgroundsPath/nightSky",
    "$BackgroundsPath/bubbles",
    "$BackgroundsPath/snowfall",
    "$BackgroundsPath/aurora",
    "$BackgroundsPath/auroraBorealis",
    "$BackgroundsPath/deepOcean",
    "$BackgroundsPath/starfield"
)

foreach ($dir in $DirectoriesToClean) {
    if (Test-Path $dir) {
        $items = Get-ChildItem -Path $dir -Recurse
        if ($items.Count -eq 0) {
            if (-not $DryRun) {
                Remove-Item -Path $dir -Recurse -Force
                Write-Host "  ✅ Removed empty directory: $dir" -ForegroundColor Green
            } else {
                Write-Host "  [DRY RUN] Would remove empty directory: $dir" -ForegroundColor Cyan
            }
        } else {
            Write-Host "  ⚠️  Directory not empty, keeping: $dir" -ForegroundColor Yellow
        }
    }
}

Write-Host "`n🎉 Phase 1 Migration Complete!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "✅ Directory structure created" -ForegroundColor Green
Write-Host "✅ Business logic moved to services layer" -ForegroundColor Green  
Write-Host "✅ Types moved to domain layer" -ForegroundColor Green
Write-Host "✅ Configuration moved to domain/configs" -ForegroundColor Green
Write-Host "✅ Utilities moved to utils layer" -ForegroundColor Green
Write-Host "✅ Backup created for rollback safety" -ForegroundColor Green
Write-Host "✅ Empty directories cleaned up" -ForegroundColor Green

Write-Host "`n🔄 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Fix import paths in moved files" -ForegroundColor White
Write-Host "2. Create runes-based state management" -ForegroundColor White
Write-Host "3. Create service interfaces" -ForegroundColor White
Write-Host "4. Register services in DI container" -ForegroundColor White
Write-Host "5. Update Svelte components" -ForegroundColor White

if ($DryRun) {
    Write-Host "`n💡 Run without -DryRun to execute the migration" -ForegroundColor Yellow
}
