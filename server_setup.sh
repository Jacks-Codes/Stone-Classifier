#!/bin/bash
# Server setup script for stone_classifier image downloader

set -e

echo "=================================="
echo "Stone Classifier Server Setup"
echo "=================================="

# Get server details
read -p "Enter server address (user@host): " SERVER
read -p "Enter destination path on server (e.g., /home/user/stone_classifier): " DEST_PATH

echo ""
echo "📦 Transferring files to server..."
rsync -avz --progress \
  --exclude 'Stone_Data/' \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --exclude '.git/' \
  --exclude 'models/' \
  --exclude 'venv/' \
  --exclude '.DS_Store' \
  ~/stone_classifier/ \
  "$SERVER:$DEST_PATH/"

echo ""
echo "✅ Files transferred successfully!"
echo ""
echo "📝 Next steps to run on the SERVER:"
echo "=================================="
echo "1. SSH into your server:"
echo "   ssh $SERVER"
echo ""
echo "2. Navigate to the project:"
echo "   cd $DEST_PATH"
echo ""
echo "3. Create virtual environment (optional but recommended):"
echo "   python3 -m venv venv"
echo "   source venv/bin/activate"
echo ""
echo "4. Install dependencies:"
echo "   pip install -r requirements.txt"
echo ""
echo "5. Set your API key as environment variable:"
echo "   export PEXELS_API_KEY='your_key_here'"
echo "   # OR edit .env file and run: source .env"
echo ""
echo "6. Run in background with nohup:"
echo "   nohup python download_images.py > download_log.txt 2>&1 &"
echo ""
echo "7. Monitor progress:"
echo "   tail -f download_log.txt"
echo "   # Or use: bash monitor_downloads.sh"
echo ""
echo "8. To bring images back after completion:"
echo "   rsync -avz --progress $SERVER:$DEST_PATH/Stone_Data/ ~/stone_classifier/Stone_Data/"
echo ""
