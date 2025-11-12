# Fix for download_images.py - Proportional splitting when limited images available
# Replace the download loop section in download_images.py with this logic

# Download images with proportional splitting
downloaded_train = 0
downloaded_val = 0
total_downloaded = 0

# Calculate ratio for proportional splitting
train_ratio = TRAIN_SPLIT  # 0.8
val_ratio = 1 - TRAIN_SPLIT  # 0.2

for i, url in enumerate(all_image_urls):
    # Calculate what we should have based on ratio
    expected_train = int(total_downloaded * train_ratio)
    expected_val = int(total_downloaded * val_ratio)
    
    # Determine if this should go to train or val based on maintaining ratio
    # If we're behind on train, prioritize train. Otherwise, alternate or fill val
    if downloaded_train < expected_train or (downloaded_train < needed_train and downloaded_val >= expected_val):
        save_dir = train_dir
        downloaded_count = downloaded_train
        target_count = needed_train
        is_train = True
    elif downloaded_val < needed_val:
        save_dir = val_dir
        downloaded_count = downloaded_val
        target_count = needed_val
        is_train = False
    else:
        # Both targets met, but we might have more images - still maintain ratio
        if downloaded_train < expected_train:
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
        total_downloaded = downloaded_train + downloaded_val
        self.downloaded_count += 1
        print(f"  ✅ Downloaded {total_downloaded}/{len(all_image_urls)} ({'train' if is_train else 'val'}: {downloaded_train}/{needed_train} train, {downloaded_val}/{needed_val} val)")
    else:
        self.failed_count += 1
    
    # Small delay to avoid overwhelming servers
    time.sleep(0.2)

print(f"  ✨ Completed: {downloaded_train} train + {downloaded_val} val images (ratio: {downloaded_train/(downloaded_train+downloaded_val)*100:.1f}% train)")

