import os
import requests
import time
import random
from pathlib import Path
from urllib.parse import urlparse
import json
from typing import List, Tuple

# Configuration
DATA_DIR = "Stone_Data"
IMAGES_PER_TYPE = 100  # Total images to download per stone type
TRAIN_SPLIT = 0.8  # 80% train, 20% validation
MIN_IMAGE_SIZE = 50000  # Minimum file size in bytes (50KB) to filter out small/placeholder images

# API Keys (get free keys from pexels.com and unsplash.com)
# Set via environment variables for security: export PEXELS_API_KEY="your_key"
# Or create a .env file (not tracked in git)
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', '')
UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY', '')  # Get from https://unsplash.com/developers

class ImageDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.downloaded_count = 0
        self.failed_count = 0
        
    def get_stone_types(self) -> List[Tuple[str, str, str]]:
        """
        Returns list of (stone_category, stone_type, folder_path) tuples
        Example: ('granite', 'absolute_black', 'Stone_Data/train/granite/absolute_black')
        """
        stone_types = []
        base_path = Path(DATA_DIR)
        
        for split in ['train', 'val']:
            split_path = base_path / split
            if not split_path.exists():
                continue
                
            for category in ['granite', 'marble', 'quartz', 'quartzite', 'travertine']:
                category_path = split_path / category
                if not category_path.exists():
                    continue
                    
                for stone_type in category_path.iterdir():
                    if stone_type.is_dir():
                        # Only add from train split to avoid duplicates
                        if split == 'train':
                            stone_types.append((category, stone_type.name, str(stone_type)))
        
        return stone_types
    
    def search_pexels(self, query: str, per_page: int = 80) -> List[str]:
        """Search Pexels for images"""
        if not PEXELS_API_KEY:
            print("  ⚠️  Pexels API key not set. Skipping Pexels.")
            return []
            
        url = "https://api.pexels.com/v1/search"
        headers = {"Authorization": PEXELS_API_KEY}
        params = {
            "query": query,
            "per_page": per_page,
            "orientation": "landscape"  # Better for countertop images
        }
        
        try:
            response = self.session.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                image_urls = [photo['src']['large'] for photo in data.get('photos', [])]
                return image_urls
            else:
                print(f"  ⚠️  Pexels API error: {response.status_code}")
                return []
        except Exception as e:
            print(f"  ⚠️  Pexels search error: {e}")
            return []
    
    def search_unsplash(self, query: str, per_page: int = 30) -> List[str]:
        """Search Unsplash for images"""
        if not UNSPLASH_API_KEY:
            print("  ⚠️  Unsplash API key not set. Skipping Unsplash.")
            return []
            
        url = "https://api.unsplash.com/search/photos"
        headers = {"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}
        params = {
            "query": query,
            "per_page": per_page,
            "orientation": "landscape"
        }
        
        try:
            response = self.session.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                image_urls = [photo['urls']['regular'] for photo in data.get('results', [])]
                return image_urls
            else:
                print(f"  ⚠️  Unsplash API error: {response.status_code}")
                return []
        except Exception as e:
            print(f"  ⚠️  Unsplash search error: {e}")
            return []
    
    def download_image(self, url: str, save_path: Path) -> bool:
        """Download a single image"""
        try:
            response = self.session.get(url, timeout=15, stream=True)
            if response.status_code == 200:
                # Check content type
                content_type = response.headers.get('content-type', '')
                if 'image' not in content_type:
                    return False
                
                # Save image
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Check file size
                if save_path.stat().st_size < MIN_IMAGE_SIZE:
                    save_path.unlink()  # Delete too small files
                    return False
                
                return True
        except Exception as e:
            if save_path.exists():
                save_path.unlink()
            return False
    
    def get_search_queries(self, category: str, stone_type: str) -> List[str]:
        """Generate search queries for a stone type"""
        # Clean stone type name
        clean_name = stone_type.replace('_', ' ')
        
        queries = [
            f"{clean_name} {category} countertop",
            f"{clean_name} {category} slab",
            f"{clean_name} {category} kitchen",
            f"{clean_name} {category}",
            f"{category} {clean_name}",
        ]
        
        # Add specific variations for quartz
        if category == 'quartz':
            if 'calacatta' in stone_type:
                queries.append(f"calacatta {clean_name.replace('calacatta ', '')} quartz")
            if 'carrara' in stone_type:
                queries.append(f"carrara {clean_name.replace('carrara ', '')} quartz")
        
        return queries
    
    def download_for_stone_type(self, category: str, stone_type: str, train_path: str):
        """Download images for a specific stone type"""
        print(f"\n📥 Downloading: {category}/{stone_type}")
        
        # Create paths
        train_dir = Path(train_path)
        val_dir = Path(train_path.replace('/train/', '/val/'))
        
        train_dir.mkdir(parents=True, exist_ok=True)
        val_dir.mkdir(parents=True, exist_ok=True)
        
        # Check existing images
        existing_train = len(list(train_dir.glob('*.jpg'))) + len(list(train_dir.glob('*.jpeg'))) + len(list(train_dir.glob('*.png')))
        existing_val = len(list(val_dir.glob('*.jpg'))) + len(list(val_dir.glob('*.jpeg'))) + len(list(val_dir.glob('*.png')))
        
        needed_train = max(0, int(IMAGES_PER_TYPE * TRAIN_SPLIT) - existing_train)
        needed_val = max(0, int(IMAGES_PER_TYPE * (1 - TRAIN_SPLIT)) - existing_val)
        needed_total = needed_train + needed_val
        
        if needed_total == 0:
            print(f"  ✅ Already have enough images ({existing_train} train, {existing_val} val)")
            return
        
        print(f"  Need {needed_train} train + {needed_val} val = {needed_total} images")
        
        # Get search queries
        queries = self.get_search_queries(category, stone_type)
        
        # Collect image URLs from multiple sources
        all_image_urls = []
        
        for query in queries[:3]:  # Use first 3 queries to avoid too many API calls
            print(f"  🔍 Searching: '{query}'")
            
            # Try Pexels
            pexels_urls = self.search_pexels(query, per_page=30)
            all_image_urls.extend(pexels_urls)
            time.sleep(0.5)  # Rate limiting
            
            # Try Unsplash
            unsplash_urls = self.search_unsplash(query, per_page=20)
            all_image_urls.extend(unsplash_urls)
            time.sleep(0.5)  # Rate limiting
            
            if len(all_image_urls) >= needed_total * 2:  # Get extra URLs in case some fail
                break
        
        # Remove duplicates
        all_image_urls = list(dict.fromkeys(all_image_urls))
        random.shuffle(all_image_urls)
        
        print(f"  📊 Found {len(all_image_urls)} unique image URLs")
        
        # Download images
        downloaded_train = 0
        downloaded_val = 0
        
        for i, url in enumerate(all_image_urls):
            if downloaded_train >= needed_train and downloaded_val >= needed_val:
                break
            
            # Determine if this goes to train or val
            if downloaded_train < needed_train:
                save_dir = train_dir
                downloaded_count = downloaded_train
                target_count = needed_train
            else:
                save_dir = val_dir
                downloaded_count = downloaded_val
                target_count = needed_val
            
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
                if save_dir == train_dir:
                    downloaded_train += 1
                else:
                    downloaded_val += 1
                self.downloaded_count += 1
                print(f"  ✅ Downloaded {downloaded_train + downloaded_val}/{needed_total} ({save_path.name})")
            else:
                self.failed_count += 1
            
            # Small delay to avoid overwhelming servers
            time.sleep(0.2)
        
        print(f"  ✨ Completed: {downloaded_train} train + {downloaded_val} val images")
    
    def run(self):
        """Main download function"""
        print("=" * 60)
        print("🖼️  Stone Classifier Image Downloader")
        print("=" * 60)
        
        # Check API keys
        if not PEXELS_API_KEY and not UNSPLASH_API_KEY:
            print("\n⚠️  WARNING: No API keys configured!")
            print("   Please get free API keys from:")
            print("   - Pexels: https://www.pexels.com/api/")
            print("   - Unsplash: https://unsplash.com/developers")
            print("\n   Add them to the script at the top (PEXELS_API_KEY and UNSPLASH_API_KEY)")
            print("   Or the script will not be able to download images.")
            response = input("\n   Continue anyway? (y/n): ")
            if response.lower() != 'y':
                return
        
        # Get all stone types
        stone_types = self.get_stone_types()
        print(f"\n📁 Found {len(stone_types)} stone types to process")
        print(f"📊 Target: {IMAGES_PER_TYPE} images per type")
        print(f"📊 Split: {int(TRAIN_SPLIT * 100)}% train, {int((1-TRAIN_SPLIT) * 100)}% validation")
        
        # Ask for confirmation
        total_images = len(stone_types) * IMAGES_PER_TYPE
        print(f"\n📈 Total images to download: ~{total_images:,}")
        response = input("\n🚀 Start downloading? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
        
        # Download for each stone type
        for i, (category, stone_type, folder_path) in enumerate(stone_types, 1):
            print(f"\n[{i}/{len(stone_types)}] Processing {category}/{stone_type}")
            try:
                self.download_for_stone_type(category, stone_type, folder_path)
            except Exception as e:
                print(f"  ❌ Error: {e}")
                continue
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Download Summary")
        print("=" * 60)
        print(f"✅ Successfully downloaded: {self.downloaded_count} images")
        print(f"❌ Failed downloads: {self.failed_count} images")
        print(f"📁 Processed: {len(stone_types)} stone types")
        print("\n✨ Done! You can now train your model.")


if __name__ == "__main__":
    downloader = ImageDownloader()
    downloader.run()

