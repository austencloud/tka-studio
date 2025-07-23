import sys
sys.path.insert(0, "src")

from application.services.learn.mock_pictograph_data_service import MockPictographDataService

print("Testing Mock Service Position Data")
mock_service = MockPictographDataService()
dataset = mock_service.get_pictograph_dataset()

letter_a = dataset.get("A", [])
if letter_a:
    sample = letter_a[0]
    print("Sample pictograph keys:", list(sample.keys()))
    print("Has start_pos:", "start_pos" in sample)
    print("Has end_pos:", "end_pos" in sample)
    if "start_pos" in sample:
        print("start_pos value:", sample["start_pos"])
    if "end_pos" in sample:
        print("end_pos value:", sample["end_pos"])
    
    same_pos = [p for p in letter_a if p.get('start_pos') == p.get('end_pos')]
    print(f"Found {len(same_pos)} pictographs with start_pos == end_pos")
    
    start_positions = set(p.get('start_pos') for p in letter_a)
    print("Unique start positions:", sorted(start_positions))
else:
    print("No data for letter A")
