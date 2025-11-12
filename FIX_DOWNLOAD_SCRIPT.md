# Fix for Download Script - Proportional Image Splitting

## Problem
When the script finds fewer images than needed (e.g., only 50 images when it needs 80 train + 19 val), it fills all images into train and never switches to val.

## Solution
The script needs to proportionally split images as it downloads them, maintaining the 80/20 train/val ratio even when limited images are available.

## Quick Fix (Simpler Approach)

Replace the download loop in `download_images.py` (around line 200-250) with this alternate approach:

```python
# Download images - Alternate approach: maintain ratio as we download
downloaded_train = 0
downloaded_val = 0

# Alternate between train and val to maintain ratio
for i, url in enumerate(all_image_urls):
    # Calculate target ratio at current point
    current_total = downloaded_train + downloaded_val
    target_train_at_this_point = int(current_total * TRAIN_SPLIT)
    
    # Decide where this image should go
    if downloaded_train < target_train_at_this_point:
        # We're behind on train, put it in train
        save_dir = train_dir
        downloaded_count = downloaded_train
        is_train = True
    elif downloaded_val < needed_val:
        # Train ratio is met, fill val
        save_dir = val_dir
        downloaded_count = downloaded_val
        is_train = False
    else:
        # Both targets met, but maintain ratio for any extra images
        if downloaded_train / (downloaded_train + downloaded_val + 1) < TRAIN_SPLIT:
            save_dir = train_dir
            downloaded_count = downloaded_train
            is_train = True
        else:
            save_dir = val_dir
            downloaded_count = downloaded_val
            is_train = False
    
    # Generate filename
    file_ext = '.jpg'
    if '.png' in url.lower():
        file_ext = '.png'
    filename = f"{stone_type}_{downloaded_count + 1:04d}{file_ext}"
    save_path = save_dir / filename
    
    # Skip if already exists
    if save_path.exists():
        continue
    
    # Download
    if self.download_image(url, save_path):
        if is_train:
            downloaded_train += 1
        else:
            downloaded_val += 1
        total = downloaded_train + downloaded_val
        self.downloaded_count += 1
        print(f"  ✅ Downloaded {total}/{len(all_image_urls)} ({'train' if is_train else 'val'}: {downloaded_train}/{needed_train} train, {downloaded_val}/{needed_val} val)")
    else:
        self.failed_count += 1
    
    time.sleep(0.2)

print(f"  ✨ Completed: {downloaded_train} train + {downloaded_val} val images")
```

## Even Simpler Fix (Round-Robin)

If you want the simplest approach, use round-robin alternating:

```python
# Download images - Round-robin to maintain ratio
downloaded_train = 0
downloaded_val = 0
download_to_train = True  # Start with train

for i, url in enumerate(all_image_urls):
    # Alternate: 4 train, 1 val (maintains ~80/20 ratio)
    if downloaded_train >= needed_train:
        # Train full, all remaining go to val
        save_dir = val_dir
        downloaded_count = downloaded_val
        is_train = False
    elif downloaded_val >= needed_val:
        # Val full, all remaining go to train
        save_dir = train_dir
        downloaded_count = downloaded_train
        is_train = True
    else:
        # Alternate to maintain ratio
        # Every 5th image goes to val (80/20 split)
        if (downloaded_train + downloaded_val) % 5 == 4:
            save_dir = val_dir
            downloaded_count = downloaded_val
            is_train = False
        else:
            save_dir = train_dir
            downloaded_count = downloaded_train
            is_train = True
    
    # Generate filename
    file_ext = '.jpg'
    if '.png' in url.lower():
        file_ext = '.png'
    filename = f"{stone_type}_{downloaded_count + 1:04d}{file_ext}"
    save_path = save_dir / filename
    
    # Skip if already exists
    if save_path.exists():
        continue
    
    # Download
    if self.download_image(url, save_path):
        if is_train:
            downloaded_train += 1
        else:
            downloaded_val += 1
        total = downloaded_train + downloaded_val
        self.downloaded_count += 1
        print(f"  ✅ Downloaded {total}/{len(all_image_urls)} ({'train' if is_train else 'val'})")
    else:
        self.failed_count += 1
    
    time.sleep(0.2)

print(f"  ✨ Completed: {downloaded_train} train + {downloaded_val} val images")
```

## How to Apply

1. SSH into your server
2. Edit `download_images.py`
3. Find the section that starts with `# Download images` (around line 200)
4. Replace the download loop with one of the fixes above
5. Save and restart the script

The script will resume from where it left off (skipping existing images) and will now properly split images proportionally.

