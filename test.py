import os

video_path = r"C:\Users\KrupaShah\Downloads\OneDrive_2025-06-04\test_video\WHat makes computer work\06_HardwareSoftware_sm.mp4"

# Check file exists
print("✅ File exists:", os.path.exists(video_path))
print("📄 Is file:", os.path.isfile(video_path))

# Try opening it
try:
    with open(video_path, 'rb') as f:
        print("✅ File opened successfully")
except Exception as e:
    print("❌ Error opening file:", e)
