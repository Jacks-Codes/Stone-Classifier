# Setting Up Image Downloader on Home Server

## Option 1: Copy Everything to Server

### 1. Transfer files to server:
```bash
# From your laptop
scp -r /Users/jack/stone_classifier user@your-server:/path/to/destination/
```

### 2. On the server, install dependencies:
```bash
cd /path/to/stone_classifier
pip install -r requirements.txt
# requests should already be in requirements.txt, but if not:
pip install requests
```

### 3. Run on server:
```bash
python download_images.py
```

## Option 2: Run in Background (nohup or screen)

### Using nohup:
```bash
nohup python download_images.py > download_log.txt 2>&1 &
```

### Using screen (better for monitoring):
```bash
screen -S stone_downloader
python download_images.py
# Press Ctrl+A then D to detach
# Reattach later with: screen -r stone_downloader
```

### Using tmux:
```bash
tmux new -s stone_downloader
python download_images.py
# Press Ctrl+B then D to detach
# Reattach later with: tmux attach -t stone_downloader
```

## Option 3: Download to Server, Then Transfer Back

1. Run downloader on server (saves to server's disk)
2. After completion, transfer images back:
```bash
# From laptop
rsync -avz --progress user@server:/path/to/Stone_Data/ /Users/jack/stone_classifier/Stone_Data/
```

## Option 4: Download Directly to Network Storage

If your server has network storage (NFS, Samba, etc.):
1. Mount the network drive on server
2. Update `DATA_DIR` in script to point to network location
3. Run script - images save directly to network storage

## Monitoring Progress

### Check download progress:
```bash
# Count images downloaded so far
find Stone_Data/train -name "*.jpg" -o -name "*.png" | wc -l
find Stone_Data/val -name "*.jpg" -o -name "*.png" | wc -l

# Check disk space
df -h

# Check if script is still running
ps aux | grep download_images.py
```

## Tips

1. **Start Small**: Test with `IMAGES_PER_TYPE = 10` first to make sure everything works
2. **Monitor Disk Space**: Keep an eye on available space
3. **Check Logs**: Review the output/logs to ensure downloads are working
4. **Resume Capability**: The script skips existing images, so you can stop and resume anytime
5. **Rate Limits**: Free APIs have limits - the script handles this, but downloads may take hours/days

## Security Note

⚠️ Your Pexels API key is in the script. When transferring to server:
- Use secure methods (scp, rsync over SSH)
- Don't commit API keys to git
- Consider using environment variables for API keys instead

## Using Environment Variables (Recommended)

Instead of hardcoding API keys, use environment variables:

```python
import os
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', '')
UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY', '')
```

Then on server:
```bash
export PEXELS_API_KEY="your_key_here"
python download_images.py
```

