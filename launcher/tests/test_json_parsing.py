#!/usr/bin/env python3
"""
Test JSON parsing for launcher configuration.
"""

import json
from pathlib import Path


def test_launcher_config_parsing():
    """Test parsing the launcher configuration JSON file."""
    
    config_dir = Path(__file__).parent.parent / "config" / "config"
    config_path = config_dir / "launcher_config.json"
    
    print(f"📄 Reading: {config_path}")
    print(f"📄 Exists: {config_path.exists()}")
    
    if not config_path.exists():
        print("❌ Launcher config file doesn't exist")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📄 File size: {len(content)} characters")
        print(f"📄 First 200 characters:")
        print(content[:200])
        
        # Parse JSON
        config = json.loads(content)
        print(f"✅ JSON parsed successfully!")
        print(f"📄 Version: {config.get('version')}")
        
        # Check structure
        sections = ['window', 'theme', 'application']
        for section in sections:
            if section in config:
                print(f"📄 Section '{section}': ✓")
                if section == 'window':
                    window_config = config[section]
                    print(f"   Width: {window_config.get('width')}")
                    print(f"   Height: {window_config.get('height')}")
                    print(f"   Mode: {window_config.get('mode')}")
            else:
                print(f"📄 Section '{section}': ❌ Missing")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_settings_json_parsing():
    """Test parsing the settings JSON file."""
    
    config_dir = Path(__file__).parent.parent / "config"
    settings_path = config_dir / "settings.json"
    
    print(f"\n📄 Reading settings: {settings_path}")
    print(f"📄 Exists: {settings_path.exists()}")
    
    if not settings_path.exists():
        print("⚠️ Settings file doesn't exist (this is normal for first run)")
        return True  # This is not an error
    
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📄 Settings file size: {len(content)} characters")
        
        # Parse JSON
        settings = json.loads(content)
        print(f"✅ Settings JSON parsed successfully!")
        
        # Show some settings
        for key, value in list(settings.items())[:5]:  # Show first 5 settings
            print(f"   {key}: {value}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Settings JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Settings error: {e}")
        return False


def test_json_with_settings_manager():
    """Test JSON parsing through the settings manager."""
    try:
        print(f"\n📄 Testing settings manager...")
        
        # Import settings manager
        import sys
        launcher_dir = Path(__file__).parent.parent
        sys.path.insert(0, str(launcher_dir))
        
        from config.settings import SettingsManager
        
        # Create settings manager (this will load/create settings)
        settings = SettingsManager()
        
        print(f"✅ Settings manager created successfully!")
        print(f"   Launch mode: {settings.get('launch_mode')}")
        print(f"   Window width: {settings.get('window_width')}")
        print(f"   Theme: {settings.get('theme')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Settings manager error: {e}")
        return False


def main():
    """Run all JSON parsing tests."""
    print("🧪 Testing JSON Configuration Parsing")
    print("=" * 50)
    
    success = True
    success &= test_launcher_config_parsing()
    success &= test_settings_json_parsing()
    success &= test_json_with_settings_manager()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All JSON parsing tests passed!")
    else:
        print("❌ Some JSON parsing tests failed.")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
