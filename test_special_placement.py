import sys
sys.path.append('f:\\CODE\\TKA')
sys.path.append('f:\\CODE\\TKA\\src\\desktop\\modern\\src')

from application.services.positioning.arrows.placement.special_placement_service import SpecialPlacementService
from domain.models.motion_data import MotionData
from domain.models.pictograph_data import PictographData
from domain.models.enums import MotionType, Location, Orientation, PropRotDir

# Test the service
try:
    service = SpecialPlacementService()
    print('Service created successfully')
    
    # Try loading data
    print('Special placements loaded:', len(service.special_placements))
    for mode, data in service.special_placements.items():
        print(f'Mode {mode}: {len(data)} subfolders')
        for subfolder, letters in data.items():
            print(f'  {subfolder}: {len(letters)} letters')
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
