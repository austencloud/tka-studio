#!/bin/bash

# Script to convert createEventDispatcher to callback props in Svelte 5 components
# This script processes modern app files only (src/lib directory, excluding legacy_web_app)

echo "Converting createEventDispatcher to callback props in modern Svelte components..."

# Find all .svelte files in src/lib that contain createEventDispatcher
files=$(grep -r "createEventDispatcher" src/lib --include="*.svelte" -l)

for file in $files; do
    echo "Processing: $file"
    
    # Skip if it's already been processed (no createEventDispatcher import)
    if ! grep -q "import.*createEventDispatcher" "$file"; then
        echo "  Already processed, skipping..."
        continue
    fi
    
    # Create backup
    cp "$file" "$file.backup"
    
    # Get all dispatch calls to understand what events are being emitted
    echo "  Finding dispatch calls..."
    dispatch_calls=$(grep -n "dispatch(" "$file" | head -10)
    echo "  Dispatch calls found:"
    echo "$dispatch_calls"
    
    echo "  Manual intervention needed for: $file"
    echo "  Please review the dispatch calls and update manually."
    echo ""
done

echo "Conversion script completed. Manual review required for each file."
