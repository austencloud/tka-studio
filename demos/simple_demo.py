#!/usr/bin/env python3
"""
Simple TKA Application Factory Demo

ASCII-only version that works reliably on all platforms.
Demonstrates the core functionality without Unicode characters.
"""

import sys
import time
from pathlib import Path

# Add TKA modern src to path
tka_src_path = Path(__file__).parent.parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(tka_src_path))

from core.application.application_factory import ApplicationFactory, ApplicationMode
from core.interfaces.core_services import (
    ISequenceDataService,
    ILayoutService,
    ISettingsService,
    ISequenceManagementService,
)


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_section(title):
    """Print a formatted section header."""
    print(f"\n--- {title} ---")


def test_application_mode(mode_name, description):
    """Test a specific application mode."""
    print_header(f"{mode_name.upper()} MODE TEST")
    print(f"Description: {description}")
    
    try:
        # Create container
        print_section("Creating Container")
        start_time = time.time()
        container = ApplicationFactory.create_app(mode_name)
        creation_time = time.time() - start_time
        
        print(f"[SUCCESS] Container created in {creation_time:.4f} seconds")
        
        # Show services
        services = container.get_registrations()
        print(f"Available services: {len(services)}")
        for service_interface in services.keys():
            print(f"  - {service_interface.__name__}")
        
        # Test sequence service
        print_section("Testing Sequence Service")
        try:
            seq_service = container.resolve(ISequenceDataService)
            print(f"[OK] Resolved sequence service: {type(seq_service).__name__}")
            
            # Create and save sequence
            sequence = seq_service.create_new_sequence("Test Sequence")
            saved = seq_service.save_sequence(sequence)
            print(f"Created and saved sequence: {saved}")
            
            # Retrieve sequences
            all_sequences = seq_service.get_all_sequences()
            print(f"Total sequences: {len(all_sequences)}")
            
        except Exception as e:
            print(f"[ERROR] Sequence service: {e}")
        
        # Test layout service
        print_section("Testing Layout Service")
        try:
            layout_service = container.resolve(ILayoutService)
            print(f"[OK] Resolved layout service: {type(layout_service).__name__}")
            
            # Get dimensions
            window_size = layout_service.get_main_window_size()
            print(f"Window size: {window_size.width}x{window_size.height}")
            
            # Test calculations
            grid = layout_service.get_optimal_grid_layout(16, (1920, 1080))
            print(f"Grid layout for 16 items: {grid[0]} rows x {grid[1]} cols")
            
        except Exception as e:
            print(f"[ERROR] Layout service: {e}")
        
        # Test settings service
        print_section("Testing Settings Service")
        try:
            settings_service = container.resolve(ISettingsService)
            print(f"[OK] Resolved settings service: {type(settings_service).__name__}")
            
            # Set and get settings
            settings_service.set_setting("test_key", "test_value")
            value = settings_service.get_setting("test_key")
            print(f"Setting test: {value}")
            
        except Exception as e:
            print(f"[ERROR] Settings service: {e}")
        
        return container
        
    except Exception as e:
        print(f"[ERROR] Failed to create {mode_name} application: {e}")
        return None


def compare_modes():
    """Compare different application modes."""
    print_header("MODE COMPARISON")
    
    modes = [
        (ApplicationMode.TEST, "Fast in-memory testing"),
        (ApplicationMode.HEADLESS, "Real logic without UI"),
        (ApplicationMode.PRODUCTION, "Full application")
    ]
    
    results = {}
    
    for mode, description in modes:
        print(f"\nTesting {mode} mode...")
        start_time = time.time()
        
        try:
            container = ApplicationFactory.create_app(mode)
            creation_time = time.time() - start_time
            
            # Quick service test
            services = container.get_registrations()
            service_count = len(services)
            
            results[mode] = {
                'success': True,
                'creation_time': creation_time,
                'service_count': service_count
            }
            
            print(f"  [OK] {mode}: {creation_time:.4f}s, {service_count} services")
            
        except Exception as e:
            results[mode] = {
                'success': False,
                'error': str(e)
            }
            print(f"  [ERROR] {mode}: {e}")
    
    # Summary
    print_section("Comparison Summary")
    for mode, result in results.items():
        if result['success']:
            print(f"{mode:12} | {result['creation_time']:.4f}s | {result['service_count']} services")
        else:
            print(f"{mode:12} | FAILED: {result['error']}")


def main():
    """Main demonstration function."""
    print_header("TKA APPLICATION FACTORY SIMPLE DEMO")
    print("This demo shows the Application Factory working across different modes.")
    print("All output uses ASCII characters for maximum compatibility.")
    
    # Test each mode individually
    test_application_mode(
        ApplicationMode.TEST,
        "Fast in-memory testing with mock services"
    )
    
    test_application_mode(
        ApplicationMode.HEADLESS,
        "Real business logic without UI components"
    )
    
    test_application_mode(
        ApplicationMode.PRODUCTION,
        "Full application with real services"
    )
    
    # Compare modes
    compare_modes()
    
    # Final summary
    print_header("DEMO COMPLETE")
    print("[SUCCESS] Application Factory demonstration completed")
    print("Key findings:")
    print("  - TEST mode: Fast, predictable, perfect for AI agents")
    print("  - HEADLESS mode: Real logic, no UI, good for servers")
    print("  - PRODUCTION mode: Complete functionality")
    print("\nThe Application Factory enables easy mode switching based on use case.")


if __name__ == "__main__":
    main()
