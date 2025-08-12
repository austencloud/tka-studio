#!/usr/bin/env python3
"""
Test script for generation functionality
"""

import sys
from pathlib import Path

# Add the modern directory to path
modern_path = Path(__file__).parent / "src" / "desktop" / "modern"
sys.path.insert(0, str(modern_path))

try:
    # Test imports
    print("Testing imports...")
    
    from desktop.modern.core.dependency_injection.di_container import DIContainer
    from desktop.modern.application.services.generation.generation_service_registration import register_generation_services
    from desktop.modern.core.interfaces.generation_services import IGenerationService, ISequenceConfigurationService
    from desktop.modern.domain.models.generation_models import GenerationConfig
    from desktop.modern.core.interfaces.generation_services import GenerationMode, LetterType, PropContinuity
    from desktop.modern.domain.models.enums import GridMode
    
    print("✅ All imports successful")
    
    # Create DI container and register services
    print("Creating DI container...")
    container = DIContainer()
    
    print("Registering generation services...")
    register_generation_services(container)
    
    print("✅ Services registered")
    
    # Resolve services
    print("Resolving services...")
    generation_service = container.resolve(IGenerationService)
    config_service = container.resolve(ISequenceConfigurationService)
    
    print("✅ Services resolved")
    print(f"Generation service: {type(generation_service)}")
    print(f"Config service: {type(config_service)}")
    
    # Test configuration
    print("Testing configuration...")
    config = config_service.get_current_config()
    print(f"✅ Current config: {config}")
    
    # Test generation
    print("Testing generation...")
    result = generation_service.generate_freeform_sequence(config)
    
    if result.success:
        print(f"✅ Generation successful! Generated {len(result.sequence_data)} beats")
        print(f"Metadata: {result.metadata}")
    else:
        print(f"❌ Generation failed: {result.error_message}")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
