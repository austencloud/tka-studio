import sys

sys.path.insert(0, "src")

try:
    from application.services.start_position import StartPositionDataService

    print("✅ StartPositionDataService imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")

try:
    from application.services.start_position import StartPositionSelectionService

    print("✅ StartPositionSelectionService imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")

try:
    from application.services.start_position import StartPositionUIService

    print("✅ StartPositionUIService imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")

try:
    from application.services.start_position import StartPositionOrchestrator

    print("✅ StartPositionOrchestrator imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")
