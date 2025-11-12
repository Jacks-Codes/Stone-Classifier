"""
Find corrupted images in the dataset
"""
import os
from PIL import Image
from pathlib import Path

def check_image(filepath):
    """Check if an image file is valid."""
    try:
        img = Image.open(filepath)
        img.verify()  # Verify it's a valid image
        return True, None
    except Exception as e:
        return False, str(e)

def find_corrupted_images(data_dir):
    """Find all corrupted images in the dataset."""
    corrupted = []
    image_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
    
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                filepath = os.path.join(root, file)
                is_valid, error = check_image(filepath)
                if not is_valid:
                    corrupted.append((filepath, error))
                    print(f"Corrupted: {filepath} - {error}")
    
    return corrupted

if __name__ == "__main__":
    data_dir = "Stone_Data"
    print(f"Scanning {data_dir} for corrupted images...")
    corrupted = find_corrupted_images(data_dir)
    
    print(f"\nFound {len(corrupted)} corrupted images")
    
    if corrupted:
        print("\nCorrupted files:")
        for filepath, error in corrupted:
            print(f"  {filepath}")
        
        print("\nTo remove them, run:")
        for filepath, _ in corrupted:
            print(f"  rm '{filepath}'")

