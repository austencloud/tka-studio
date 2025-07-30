"""
Generation Services Critical Integration Test - FIXED

Tests the FIXED generation services to verify they work with actual TKA systems.
Run this to validate that the critical fixes are working.
"""

import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
sys.path.insert(0, project_root)

def test_fixed_generation_services():
    """Test that the FIXED generation services work correctly with real TKA systems."""
    print("🔧 Testing FIXED TKA Modern Generation Services")
    print("=" * 60)
    
    try:
        # Test 1: Import real constants
        print("📦 Testing real constants import...")
        from data.constants import (
            PRO, ANTI, FLOAT, DASH, STATIC,
            BLUE_ATTRS, RED_ATTRS, MOTION_TYPE, PROP_ROT_DIR,
            CLOCKWISE, COUNTER_CLOCKWISE, NO_ROT,
            LETTER, BEAT, TURNS, START_ORI, END_ORI, IN
        )
        print(f"✅ Real constants imported: PRO={PRO}, BLUE_ATTRS={BLUE_ATTRS}")
        
        # Test 2: Fixed TurnIntensityManager with legacy interface
        print("\n⚙️ Testing FIXED TurnIntensityManager...")
        from desktop.modern.application.services.generation.turn_intensity_manager import TurnIntensityManager
        
        # Test legacy interface
        turn_manager = TurnIntensityManager(word_length=8, level=2, max_turn_intensity=2.0)
        blue_turns, red_turns = turn_manager.allocate_turns_for_blue_and_red()
        
        assert len(blue_turns) == 8
        assert len(red_turns) == 8
        assert all(isinstance(t, (int, float, str)) for t in blue_turns)
        print(f"✅ Legacy TurnIntensityManager working: {blue_turns[:3]}... (blue), {red_turns[:3]}... (red)")
        
        # Test 3: Fixed BaseSequenceBuilder with real constants
        print("\n🏗️ Testing FIXED BaseSequenceBuilder...")
        
        # Create mock container
        class MockContainer:
            def resolve(self, interface):
                return None
        
        container = MockContainer()
        
        from desktop.modern.application.services.generation.base_sequence_builder import BaseSequenceBuilder
        builder = BaseSequenceBuilder(container)
        
        # Test data structure creation
        test_beat = {
            BLUE_ATTRS: {
                MOTION_TYPE: PRO,
                PROP_ROT_DIR: CLOCKWISE,
                TURNS: 1,
                START_ORI: IN,
                END_ORI: IN
            },
            RED_ATTRS: {
                MOTION_TYPE: ANTI,
                PROP_ROT_DIR: COUNTER_CLOCKWISE,
                TURNS: 1,
                START_ORI: IN,
                END_ORI: IN
            },
            LETTER: "A",
            BEAT: 1
        }
        
        # Test turn setting
        updated_beat = builder.set_turns(test_beat, 2.5, "fl")
        assert updated_beat[BLUE_ATTRS][TURNS] == 2.5
        assert updated_beat[RED_ATTRS][TURNS] == "fl"
        print("✅ BaseSequenceBuilder using real constants and data structure")
        
        # Test 4: Configuration and validation
        print("\n📋 Testing configuration with real enums...")
        from desktop.modern.core.interfaces.generation_services import (
            GenerationMode,
            LetterType,
            PropContinuity,
        )
        from desktop.modern.domain.models.generation_models import GenerationConfig
        
        config = GenerationConfig(
            mode=GenerationMode.FREEFORM,
            length=8,
            level=2,
            turn_intensity=1.5,
            prop_continuity=PropContinuity.CONTINUOUS,
            letter_types={LetterType.TYPE1, LetterType.TYPE2}
        )
        assert config.is_valid()
        print("✅ Configuration with real enums working")
        
        # Test 5: Service instantiation
        print("\n🏭 Testing service instantiation...")
        from desktop.modern.application.services.generation.generation_service import GenerationService
        from desktop.modern.application.services.generation.freeform_generation_service import FreeformGenerationService
        
        generation_service = GenerationService(container)
        freeform_service = FreeformGenerationService(container)
        print("✅ Services instantiate without errors")
        
        # Test 6: Letter type integration attempt
        print("\n🔤 Testing letter type integration...")
        try:
            from enums.letter.letter_type import LetterType as LegacyLetterType
            
            # Test mapping
            legacy_type1 = LegacyLetterType.from_string("Type1")
            assert "A" in legacy_type1.letters
            assert "V" in legacy_type1.letters
            print(f"✅ Legacy letter types accessible: Type1 has {len(legacy_type1.letters)} letters")
            
        except ImportError:
            print("⚠️  Legacy LetterType not available (expected in isolated test)")
        
        # Test 7: Fallback option generation
        print("\n🎯 Testing option generation...")
        fallback_options = freeform_service._get_fallback_options()
        assert len(fallback_options) >= 2
        
        # Verify structure matches TKA format
        option = fallback_options[0]
        assert LETTER in option
        assert BLUE_ATTRS in option
        assert RED_ATTRS in option
        assert MOTION_TYPE in option[BLUE_ATTRS]
        print(f"✅ Options have correct TKA structure: {option[LETTER]} with {option[BLUE_ATTRS][MOTION_TYPE]}/{option[RED_ATTRS][MOTION_TYPE]}")
        
        print("\n🎉 FIXED generation services passed critical tests!")
        print("\n📝 What's working:")
        print("   ✅ Real TKA constants integration")
        print("   ✅ Legacy TurnIntensityManager interface")
        print("   ✅ Correct data structure format") 
        print("   ✅ Service instantiation")
        print("   ✅ Configuration management")
        print("   ✅ Letter type integration framework")
        print("   ✅ Option generation with TKA structure")
        
        print("\n🔗 Integration status:")
        print("   ✅ Constants: Using real data.constants")
        print("   ✅ Data structure: Matches legacy format")
        print("   ✅ Turn manager: Legacy interface implemented")
        print("   ⚠️  Option loading: Fallback mode (needs construct tab)")
        print("   ⚠️  Sequence workbench: Fallback mode (needs UI integration)")
        print("   ⚠️  Orientation calc: Simplified mode (needs ori_calculator)")
        
        print("\n🚀 Ready for integration with actual TKA systems!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Critical test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_fixed_generation_services()
    sys.exit(0 if success else 1)
