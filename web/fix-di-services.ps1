#!/usr/bin/env pwsh
# Comprehensive script to fix all remaining DI service resolution issues
# Converts old string-based and Symbol-based resolve calls to use TYPES

Write-Host "🔧 Starting comprehensive DI service resolution fix..." -ForegroundColor Green

# Define the files and their fixes
$fixes = @(
    @{
        File = "src\lib\components\core\pictograph\components\PropSvg.svelte"
        Pattern = "const propCoordinator: IPropCoordinatorService = resolve\("
        Replacement = "const propCoordinator: IPropCoordinatorService = resolve<IPropCoordinatorService>(TYPES.IPropCoordinatorService"
        AddImport = $true
    },
    @{
        File = "src\lib\components\tabs\browse-tab\BrowseTab.svelte"
        Pattern = "const sequenceIndexService = resolve\("
        Replacement = "const sequenceIndexService = resolve<import(`"`$lib/services/interfaces/browse-interfaces`").ISequenceIndexService>(TYPES.ISequenceIndexService"
        AddImport = $true
    },
    @{
        File = "src\lib\components\tabs\browse-tab\BrowseTab.svelte"
        Pattern = "const filterPersistenceService = resolve\("
        Replacement = "const filterPersistenceService = resolve<import(`"`$lib/services/interfaces/persistence-interfaces`").IFilterPersistenceService>(TYPES.IFilterPersistenceService"
        AddImport = $true
    },
    @{
        File = "src\lib\components\tabs\browse-tab\BrowseTab.svelte"
        Pattern = "const panelManagementService = resolve\("
        Replacement = "const panelManagementService = resolve<import(`"`$lib/services/interfaces/navigation-interfaces`").IPanelManagementService>(TYPES.IPanelManagementService"
        AddImport = $true
    },
    @{
        File = "src\lib\components\tabs\build-tab\export\ExportPanel.svelte"
        Pattern = "resolve\("
        Replacement = "resolve<import(`"`$lib/services/interfaces/export-interfaces`").IExportService>(TYPES.IExportService"
        AddImport = $true
    }
)

# Function to add TYPES import if needed
function Add-TypesImport {
    param($FilePath)
    
    $content = Get-Content $FilePath -Raw
    if ($content -notmatch "import.*TYPES.*from.*inversify") {
        # Find existing imports
        $lines = Get-Content $FilePath
        $lastImportIndex = -1
        
        for ($i = 0; $i -lt $lines.Count; $i++) {
            if ($lines[$i] -match "^\s*import\s+") {
                $lastImportIndex = $i
            }
        }
        
        if ($lastImportIndex -ge 0) {
            # Add TYPES import after last import
            $newLines = @()
            $newLines += $lines[0..$lastImportIndex]
            $newLines += "  import { resolve, TYPES } from `"`$lib/services/inversify/container`";"
            $newLines += $lines[($lastImportIndex + 1)..($lines.Count - 1)]
            
            $newLines | Set-Content $FilePath
            Write-Host "  ✅ Added TYPES import to $FilePath" -ForegroundColor Green
        }
    }
}

# Apply fixes
foreach ($fix in $fixes) {
    $filePath = $fix.File
    
    if (Test-Path $filePath) {
        Write-Host "🔧 Fixing $filePath..." -ForegroundColor Yellow
        
        # Add TYPES import if needed
        if ($fix.AddImport) {
            Add-TypesImport $filePath
        }
        
        # Apply the fix
        $content = Get-Content $filePath -Raw
        $newContent = $content -replace [regex]::Escape($fix.Pattern), $fix.Replacement
        
        if ($content -ne $newContent) {
            $newContent | Set-Content $filePath -NoNewline
            Write-Host "  ✅ Applied fix to $filePath" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️ No changes needed for $filePath" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ❌ File not found: $filePath" -ForegroundColor Red
    }
}

Write-Host "🎉 DI service resolution fixes completed!" -ForegroundColor Green
Write-Host "📋 Summary:" -ForegroundColor Cyan
Write-Host "  - Fixed PropSvg.svelte" -ForegroundColor White
Write-Host "  - Fixed BrowseTab.svelte (3 services)" -ForegroundColor White  
Write-Host "  - Fixed ExportPanel.svelte" -ForegroundColor White
Write-Host "  - Added TYPES imports where needed" -ForegroundColor White
Write-Host ""
Write-Host "🧪 Next steps:" -ForegroundColor Cyan
Write-Host "  1. Test the application" -ForegroundColor White
Write-Host "  2. Check for any remaining resolve() issues" -ForegroundColor White
Write-Host "  3. Verify all services are working" -ForegroundColor White
