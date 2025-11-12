# Image Downloader Guide

This script automatically downloads images for all your stone types from free stock photo APIs.

## Setup

### 1. Get API Keys (Free)

You need API keys from at least one of these services:

**Pexels API** (Recommended - Easy to get):
1. Go to https://www.pexels.com/api/
2. Sign up for free
3. Copy your API key
4. Add it to `download_images.py` line 15: `PEXELS_API_KEY = "your_key_here"`

**Unsplash API** (Alternative):
1. Go to https://unsplash.com/developers
2. Create a free developer account
3. Create a new application
4. Copy your Access Key
5. Add it to `download_images.py` line 16: `UNSPLASH_API_KEY = "your_key_here"`

### 2. Configure Settings

Edit the settings at the top of `download_images.py`:

```python
IMAGES_PER_TYPE = 100  # Total images per stone type
TRAIN_SPLIT = 0.8      # 80% train, 20% validation
```

## Usage

### Run the script:

```bash
python download_images.py
```

The script will:
1. Scan all stone type folders you've created
2. For each stone type, search for images using multiple queries
3. Download images from Pexels/Unsplash
4. Automatically split them into train/val folders
5. Skip folders that already have enough images
6. Show progress for each download

### Example Output:

```
📥 Downloading: granite/absolute_black
  Need 80 train + 20 val = 100 images
  🔍 Searching: 'absolute black granite countertop'
  📊 Found 45 unique image URLs
  ✅ Downloaded 1/100 (absolute_black_0001.jpg)
  ✅ Downloaded 2/100 (absolute_black_0002.jpg)
  ...
  ✨ Completed: 80 train + 20 val images
```

## Features

- ✅ Automatically discovers all stone types from your folder structure
- ✅ Smart search queries for each stone type
- ✅ Downloads from multiple sources (Pexels + Unsplash)
- ✅ Automatic train/val split (80/20 by default)
- ✅ Skips existing images (resume-friendly)
- ✅ Filters out small/placeholder images
- ✅ Progress tracking and error handling
- ✅ Rate limiting to respect API limits

## Troubleshooting

### No images downloading?
- Check that you've added API keys
- Verify your internet connection
- Check API rate limits (free tiers have limits)

### Low quality images?
- Some stone types may not have many results
- Try running the script multiple times to get more images
- Consider manually adding images for rare stone types

### API Rate Limits?
- Free APIs have rate limits (usually 50-200 requests/hour)
- The script includes delays to avoid hitting limits
- If you hit limits, wait an hour and run again
- Consider getting API keys from both services for more images

## Tips

1. **Start Small**: Test with `IMAGES_PER_TYPE = 20` first
2. **Run Multiple Times**: The script skips existing images, so you can run it multiple times to build up your dataset
3. **Manual Review**: Some images might not be exactly what you need - consider reviewing and removing poor quality images
4. **Specific Types**: For very specific stone types (like "calacatta_azulean"), you might need to manually add images

## Next Steps

After downloading images:
1. Review some images to ensure quality
2. Remove any incorrect or poor quality images
3. Run `train_model.py` to train your classifier
4. Evaluate results and add more images for poorly performing classes

