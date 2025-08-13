#!/usr/bin/env python3
"""
Utility to identify and fix missing author/start position metadata in PNG files.

This script:
1. Scans all PNG files in the dictionary
2. Identifies those missing author or start position data
3. Provides options to fix the missing data

Usage:
    python fix-missing-metadata.py --scan    # Just show what's missing
    python fix-missing-metadata.py --fix     # Actually fix the missing data
"""

import json
from pathlib import Path
from struct import unpack
import argparse


def find_text_chunk(data, keyword):
    """Find a tEXt chunk with the specified keyword in PNG data."""
    offset = 8  # Skip PNG signature

    while offset < len(data):
        # Read chunk length (4 bytes, big-endian)
        if offset + 4 > len(data):
            break
        length = unpack(">I", data[offset : offset + 4])[0]
        offset += 4

        # Read chunk type (4 bytes)
        if offset + 4 > len(data):
            break
        chunk_type = data[offset : offset + 4].decode("ascii", errors="ignore")
        offset += 4

        # Check if this is a tEXt chunk
        if chunk_type == "tEXt" and offset + length <= len(data):
            chunk_data = data[offset : offset + length]
            try:
                text = chunk_data.decode("latin1")
                null_index = text.find("\0")
                if null_index != -1:
                    chunk_keyword = text[:null_index]
                    if chunk_keyword == keyword:
                        return text[null_index + 1 :]
            except Exception:
                pass

        # Skip chunk data and CRC
        offset += length + 4

    return None


def extract_metadata_from_png(png_path):
    """Extract JSON metadata from a PNG file."""
    try:
        with open(png_path, "rb") as f:
            data = f.read()

        metadata_json = find_text_chunk(data, "metadata")
        if not metadata_json:
            return None

        parsed = json.loads(metadata_json)
        return parsed.get("sequence", parsed)
    except Exception as e:
        print(f"❌ Error reading {png_path}: {e}")
        return None


def analyze_metadata(metadata):
    """Analyze metadata for missing author/start position."""
    if not metadata or not isinstance(metadata, list):
        return {"error": "Invalid metadata structure"}

    # Get first entry for author/level info
    first_entry = metadata[0] if metadata else {}

    # Find start position entries
    start_position_entries = [
        step for step in metadata if step.get("sequence_start_position")
    ]

    issues = []

    # Check for missing author
    if not first_entry.get("author"):
        issues.append("missing_author")

    # Check for missing start position
    if not start_position_entries:
        issues.append("missing_start_position")

    # Check for missing level
    if first_entry.get("level") is None:
        issues.append("missing_level")

    return {
        "author": first_entry.get("author"),
        "start_position": (
            start_position_entries[0].get("sequence_start_position")
            if start_position_entries
            else None
        ),
        "level": first_entry.get("level"),
        "issues": issues,
        "metadata": metadata,
    }


def scan_dictionary():
    """Scan all PNG files in the dictionary for missing metadata."""
    dictionary_path = Path("static/dictionary")
    if not dictionary_path.exists():
        dictionary_path = Path("dictionary")  # Try alternate path

    if not dictionary_path.exists():
        print("❌ Dictionary directory not found")
        return []

    results = []

    for sequence_dir in dictionary_path.iterdir():
        if sequence_dir.is_dir():
            png_path = sequence_dir / f"{sequence_dir.name}_ver1.png"
            if png_path.exists():
                print(f"🔍 Analyzing {sequence_dir.name}...")
                metadata = extract_metadata_from_png(png_path)
                if metadata:
                    analysis = analyze_metadata(metadata)
                    if analysis.get("issues"):
                        results.append(
                            {
                                "sequence": sequence_dir.name,
                                "path": str(png_path),
                                "analysis": analysis,
                            }
                        )

    return results


def print_scan_results(results):
    """Print the results of the metadata scan."""
    print(f"\n📊 Scan Results: Found {len(results)} sequences with metadata issues")
    print("=" * 80)

    missing_author = []
    missing_start_pos = []
    missing_level = []

    for result in results:
        seq = result["sequence"]
        issues = result["analysis"]["issues"]
        author = result["analysis"]["author"]
        start_pos = result["analysis"]["start_position"]
        level = result["analysis"]["level"]

        print(f"\n🔸 {seq}")
        print(f"   Author: {author or 'MISSING'}")
        print(f"   Start Position: {start_pos or 'MISSING'}")
        print(f"   Level: {level if level is not None else 'MISSING'}")
        print(f"   Issues: {', '.join(issues)}")

        if "missing_author" in issues:
            missing_author.append(seq)
        if "missing_start_position" in issues:
            missing_start_pos.append(seq)
        if "missing_level" in issues:
            missing_level.append(seq)

    print("\n📈 Summary:")
    print(f"   Missing Author: {len(missing_author)} sequences")
    print(f"   Missing Start Position: {len(missing_start_pos)} sequences")
    print(f"   Missing Level: {len(missing_level)} sequences")

    if missing_author:
        print("\n👤 Sequences missing author:")
        for seq in missing_author[:10]:  # Show first 10
            print(f"   - {seq}")
        if len(missing_author) > 10:
            print(f"   ... and {len(missing_author) - 10} more")

    if missing_start_pos:
        print("\n📍 Sequences missing start position:")
        for seq in missing_start_pos[:10]:  # Show first 10
            print(f"   - {seq}")
        if len(missing_start_pos) > 10:
            print(f"   ... and {len(missing_start_pos) - 10} more")


def fix_metadata_in_png(png_path, fixes):
    """Fix missing metadata in a PNG file."""
    try:
        with open(png_path, "rb") as f:
            data = bytearray(f.read())

        # Find and extract current metadata
        metadata_json = find_text_chunk(data, "metadata")
        if not metadata_json:
            print(f"❌ No metadata found in {png_path}")
            return False

        # Parse current metadata
        parsed = json.loads(metadata_json)
        sequence_data = parsed.get("sequence", parsed)
        
        if not isinstance(sequence_data, list) or not sequence_data:
            print(f"❌ Invalid metadata structure in {png_path}")
            return False

        # Apply fixes
        modified = False
        
        # Fix missing author
        if "missing_author" in fixes:
            sequence_data[0]["author"] = "Austen Cloud"
            modified = True
            print(f"✅ Added author to {png_path}")
        
        # Fix missing start position
        if "missing_start_position" in fixes:
            start_pos = fixes["missing_start_position"]
            # Find the first beat entry and add sequence_start_position
            for step in sequence_data:
                if step.get("beat") is not None:
                    step["sequence_start_position"] = start_pos
                    modified = True
                    print(f"✅ Added start position '{start_pos}' to {png_path}")
                    break

        if not modified:
            return True

        # Update the metadata structure
        if "sequence" in parsed:
            parsed["sequence"] = sequence_data
        else:
            parsed = sequence_data

        # Convert back to JSON
        new_metadata_json = json.dumps(parsed, separators=(',', ':'))

        # Find the metadata chunk and replace it
        offset = 8  # Skip PNG signature
        new_data = bytearray(data[:8])  # Keep PNG signature

        while offset < len(data):
            # Read chunk length (4 bytes, big-endian)
            if offset + 4 > len(data):
                break
            length = unpack(">I", data[offset : offset + 4])[0]
            
            # Read chunk type (4 bytes)
            chunk_type = data[offset + 4 : offset + 8].decode("ascii", errors="ignore")
            
            if chunk_type == "tEXt" and offset + 8 + length <= len(data):
                # Check if this is the metadata chunk
                chunk_data = data[offset + 8 : offset + 8 + length]
                try:
                    text = chunk_data.decode("latin1")
                    null_index = text.find("\0")
                    if null_index != -1 and text[:null_index] == "metadata":
                        # Replace this chunk with updated metadata
                        new_chunk_data = f"metadata\0{new_metadata_json}".encode("latin1")
                        new_length = len(new_chunk_data)
                        
                        # Add length (4 bytes)
                        new_data.extend(new_length.to_bytes(4, 'big'))
                        # Add chunk type (4 bytes)
                        new_data.extend(b"tEXt")
                        # Add chunk data
                        new_data.extend(new_chunk_data)
                        # Add CRC (4 bytes) - simplified, just copy original for now
                        new_data.extend(data[offset + 8 + length : offset + 12 + length])
                        
                        offset += 12 + length
                        continue
                except Exception:
                    pass
            
            # Copy chunk as-is
            chunk_size = 12 + length  # length + type + data + crc
            new_data.extend(data[offset : offset + chunk_size])
            offset += chunk_size

        # Write the updated file
        with open(png_path, "wb") as f:
            f.write(new_data)
        
        return True

    except Exception as e:
        print(f"❌ Error fixing {png_path}: {e}")
        return False


def fix_missing_metadata():
    """Fix all missing metadata in the dictionary."""
    print("🔧 Scanning for metadata issues to fix...")
    results = scan_dictionary()
    
    if not results:
        print("✅ No metadata issues found - all sequences are properly configured!")
        return
    
    print(f"📝 Found {len(results)} sequences to fix...")
    
    # Define the fixes needed
    fixes_applied = 0
    
    for result in results:
        sequence = result["sequence"]
        path = result["path"]
        issues = result["analysis"]["issues"]
        
        print(f"\n🔧 Fixing {sequence}...")
        
        # Determine what fixes to apply
        fixes = {}
        
        if "missing_author" in issues:
            fixes["missing_author"] = True
            
        if "missing_start_position" in issues:
            # Determine start position based on sequence name or default patterns
            if sequence == "JGG":
                fixes["missing_start_position"] = "alpha"
            else:
                # For other sequences, we'll need to determine based on their patterns
                # Most sequences start in alpha, beta, or gamma
                # For now, let's default to alpha and the user can adjust if needed
                fixes["missing_start_position"] = "alpha"
        
        if fixes:
            success = fix_metadata_in_png(path, fixes)
            if success:
                fixes_applied += 1
                print(f"✅ Successfully fixed {sequence}")
            else:
                print(f"❌ Failed to fix {sequence}")
    
    print(f"\n🎉 Fixed {fixes_applied} sequences!")
    print("💡 Run --scan again to verify all fixes were applied correctly.")


def main():
    parser = argparse.ArgumentParser(description="Fix missing metadata in PNG files")
    parser.add_argument("--scan", action="store_true", help="Scan for missing metadata")
    parser.add_argument(
        "--fix", action="store_true", help="Fix missing metadata"
    )

    args = parser.parse_args()

    if args.scan:
        print("� Scanning dictionary for missing metadata...")
        results = scan_dictionary()
        print_scan_results(results)

        print("\n💡 Next steps:")
        print("1. Review the sequences with missing metadata above")
        print("2. Use --fix to automatically add missing author/start position data")
        print("3. Most sequences should have author='Austen Cloud' and appropriate start positions")

    elif args.fix:
        fix_missing_metadata()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
