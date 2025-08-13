#!/usr/bin/env python3
"""
Test script to verify sequence card images are loading correctly.
"""

import sys
from pathlib import Path

# Add the modern directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_sequence_card_images():
    """Test if sequence card images exist and can be loaded."""
    print("🔍 Testing sequence card image loading...")
    
    # Check if images directory exists
    images_dir = current_dir / "images" / "sequence_card_images"
    print(f"Images directory: {images_dir}")
    print(f"Images directory exists: {images_dir.exists()}")
    
    if not images_dir.exists():
        print("❌ Images directory not found!")
        return False
    
    # Count subdirectories and images
    subdirs = [d for d in images_dir.iterdir() if d.is_dir()]
    print(f"Found {len(subdirs)} sequence subdirectories")
    
    total_images = 0
    sample_images = []
    
    for subdir in subdirs[:10]:  # Check first 10 subdirectories
        png_files = list(subdir.glob("*.png"))
        total_images += len(png_files)
        if png_files:
            sample_images.append((subdir.name, png_files[0]))
        print(f"  {subdir.name}: {len(png_files)} PNG files")
    
    print(f"\nTotal images found in sample: {total_images}")
    
    if sample_images:
        print("\n✅ Sample images found:")
        for word, image_path in sample_images[:5]:
            print(f"  {word}: {image_path.name} (exists: {image_path.exists()})")
        return True
    else:
        print("❌ No PNG images found in sequence directories!")
        return False

def test_sequence_data_service():
    """Test the sequence data service."""
    print("\n🔍 Testing sequence data service...")
    
    try:
        # Import with proper path setup
        from desktop.modern.application.services.sequence_card.sequence_data_service import SequenceCardDataService
        
        service = SequenceCardDataService()
        sequences = service.load_all_sequences()
        
        print(f"✅ Loaded {len(sequences)} sequences from data service")
        
        if sequences:
            print("\nSample sequences:")
            for i, seq in enumerate(sequences[:5]):
                print(f"  {i+1}. {seq.word} - {seq.path.name} (exists: {seq.path.exists()})")
            return True
        else:
            print("❌ No sequences loaded!")
            return False
            
    except Exception as e:
        print(f"❌ Error loading sequences: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Sequence Card Test Suite")
    print("=" * 50)
    
    images_ok = test_sequence_card_images()
    service_ok = test_sequence_data_service()
    
    print("\n" + "=" * 50)
    if images_ok and service_ok:
        print("✅ All tests passed! Sequence cards should work correctly.")
    else:
        print("❌ Some tests failed. Sequence cards may show placeholders.")