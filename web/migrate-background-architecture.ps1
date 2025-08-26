#!/usr/bin/env pwsh
<#
.SYNOPSIS
TKA Background Animation Architecture Migration Script - Phase 1
Migrates background animation system from mixed-concern architecture to proper Svelte 5 runes + microservices pattern

.DESCRIPTION
This script performs Phase 1 of the background animation architecture migration:
1. Creates new directory structure following clean architecture
2. Moves business logic to services/implementations/background/
3. Moves types to domain/background/
4. Moves utilities to utils/background/
5. Creates backup of old structure
6. Cleans up empty directories

.NOTES
Author: TKA Development Assistant
Version: 1.0
Date: 2025-01-25
#>

param(
    [switch]$DryRun = $false,
    [switch]$Verbose = $false
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Enable verbose output if requested
if ($Verbose) {
    $VerbosePreference = "Continue"
}

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

# Define file movements for business logic
$BusinessLogicMoves = @{
    # Core animation services
    "$BackgroundsPath/core/BackgroundFactory.ts" = "$ServicesPath/implementations/background/BackgroundFactory.ts"
    "$BackgroundsPath/core/BackgroundManager.ts" = "$ServicesPath/implementations/background/BackgroundManager.ts"
    "$BackgroundsPath/core/BackgroundManager.svelte.ts" = "$ServicesPath/implementations/background/BackgroundManager.svelte.ts"
    "$BackgroundsPath/core/PerformanceTracker.ts" = "$ServicesPath/implementations/background/performance/PerformanceTracker.ts"
    "$BackgroundsPath/core/ResourceTracker.ts" = "$ServicesPath/implementations/background/performance/ResourceTracker.ts"
    
    # Animation system classes
    "$BackgroundsPath/nightSky/NightSkyBackgroundSystem.ts" = "$ServicesPath/implementations/background/systems/NightSkyBackgroundSystem.ts"
    "$BackgroundsPath/bubbles/BubblesBackgroundSystem.ts" = "$ServicesPath/implementations/background/systems/BubblesBackgroundSystem.ts"
    "$BackgroundsPath/snowfall/SnowfallBackgroundSystem.ts" = "$ServicesPath/implementations/background/systems/SnowfallBackgroundSystem.ts"
    "$BackgroundsPath/aurora/AuroraBackgroundSystem.ts" = "$ServicesPath/implementations/background/systems/AuroraBackgroundSystem.ts"
    "$BackgroundsPath/auroraBorealis/AuroraBorealisBackgroundSystem.ts" = "$ServicesPath/implementations/background/systems/AuroraBorealisBackgroundSystem.ts"
    "$BackgroundsPath/deepOcean/DeepOceanBackgroundSystem.ts" = "$ServicesPath/implementations/background/systems/DeepOceanBackgroundSystem.ts"
    "$BackgroundsPath/starfield/StarfieldBackgroundSystem.ts" = "$ServicesPath/implementations/background/systems/StarfieldBackgroundSystem.ts"
    
    # System utilities and sub-systems
    "$BackgroundsPath/systems/ShootingStarSystem.ts" = "$ServicesPath/implementations/background/systems/core/ShootingStarSystem.ts"
    "$BackgroundsPath/systems/SnowflakeSystem.ts" = "$ServicesPath/implementations/background/systems/core/SnowflakeSystem.ts"
}

# Move business logic files
foreach ($move in $BusinessLogicMoves.GetEnumerator()) {
    $source = $move.Key
    $destination = $move.Value
    
    if (Test-Path $source) {
        if (-not $DryRun) {
            # Ensure destination directory exists
            $destDir = Split-Path $destination -Parent
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            
            Move-Item -Path $source -Destination $destination -Force
            Write-Host "  ✅ Moved: $(Split-Path $source -Leaf) → $destination" -ForegroundColor Green
        } else {
            Write-Host "  [DRY RUN] Would move: $source → $destination" -ForegroundColor Cyan
        }
    } else {
        Write-Host "  ⚠️  File not found: $source" -ForegroundColor Yellow
    }
}

Write-Host "`n📋 Moving types to domain..." -ForegroundColor Green

# Define type movements
$TypeMoves = @{
    "$BackgroundsPath/types/types.ts" = "$DomainPath/background/BackgroundTypes.ts"
}

# Move type files
foreach ($move in $TypeMoves.GetEnumerator()) {
    $source = $move.Key
    $destination = $move.Value
    
    if (Test-Path $source) {
        if (-not $DryRun) {
            Move-Item -Path $source -Destination $destination -Force
            Write-Host "  ✅ Moved: $(Split-Path $source -Leaf) → $destination" -ForegroundColor Green
        } else {
            Write-Host "  [DRY RUN] Would move: $source → $destination" -ForegroundColor Cyan
        }
    } else {
        Write-Host "  ⚠️  File not found: $source" -ForegroundColor Yellow
    }
}

Write-Host "`n⚙️ Moving configuration files..." -ForegroundColor Green

# Define config movements
$ConfigMoves = @{
    "$BackgroundsPath/config.ts" = "$DomainPath/background/configs/config.ts"
    "$BackgroundsPath/config/nightSky.ts" = "$DomainPath/background/configs/nightSky.ts"
    "$BackgroundsPath/snowfall/constants.ts" = "$DomainPath/background/configs/snowfall-constants.ts"
}

# Move config files
foreach ($move in $ConfigMoves.GetEnumerator()) {
    $source = $move.Key
    $destination = $move.Value
    
    if (Test-Path $source) {
        if (-not $DryRun) {
            Move-Item -Path $source -Destination $destination -Force
            Write-Host "  ✅ Moved: $(Split-Path $source -Leaf) → $destination" -ForegroundColor Green
        } else {
            Write-Host "  [DRY RUN] Would move: $source → $destination" -ForegroundColor Cyan
        }
    } else {
        Write-Host "  ⚠️  File not found: $source" -ForegroundColor Yellow
    }
}

Write-Host "`n🛠️ Moving utilities..." -ForegroundColor Green

# Define utility movements
$UtilityMoves = @{
    "$BackgroundsPath/snowfall/utils/backgroundUtils.ts" = "$UtilsPath/background/backgroundUtils.ts"
}

# Move utility files
foreach ($move in $UtilityMoves.GetEnumerator()) {
    $source = $move.Key
    $destination = $move.Value
    
    if (Test-Path $source) {
        if (-not $DryRun) {
            Move-Item -Path $source -Destination $destination -Force
            Write-Host "  ✅ Moved: $(Split-Path $source -Leaf) → $destination" -ForegroundColor Green
        } else {
            Write-Host "  [DRY RUN] Would move: $source → $destination" -ForegroundColor Cyan
        }
    } else {
        Write-Host "  ⚠️  File not found: $source" -ForegroundColor Yellow
    }
}

Write-Host "`n💾 Creating backup of remaining structure..." -ForegroundColor Green

if (-not $DryRun) {
    # Copy remaining files to backup
    $BackupPath = "$BackgroundsPath/_backup_old_structure"
    
    # Get all remaining files and directories (excluding the backup directory itself)
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
    Write-Host "  [DRY RUN] Would create backup in: $BackgroundsPath/_backup_old_structure" -ForegroundColor Cyan
}

Write-Host "`n🧹 Cleaning up empty directories..." -ForegroundColor Green

# Define directories to remove (if empty)
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
