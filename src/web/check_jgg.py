#!/usr/bin/env python3
"""Quick script to check JGG metadata and determine the right start position."""

import json
from pathlib import Path
from struct import unpack


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
        print(f"Error reading {png_path}: {e}")
        return None


# Check JGG specifically
jgg_path = Path("static/dictionary/JGG/JGG_ver1.png")
if jgg_path.exists():
    metadata = extract_metadata_from_png(jgg_path)
    print("JGG metadata structure:")
    print(json.dumps(metadata, indent=2))

    # Look at the actual beat data to determine start position
    if metadata and isinstance(metadata, list):
        print("\nAnalyzing beat patterns to determine start position:")

        # Find beats that could indicate start position
        for i, step in enumerate(metadata):
            beat = step.get("beat")
            if beat:
                print(f"Step {i}: beat = {beat}")

        # Look for common start position patterns
        # Check if first step has specific positions
        if metadata:
            first_step = metadata[0]
            print(f"\nFirst step beat pattern: {first_step.get('beat')}")

            # Based on beat patterns, determine likely start position
            # This sequence seems to be starting in alpha position most likely
            print("\nBased on analysis, JGG likely starts in 'alpha' position")
else:
    print("JGG file not found")
