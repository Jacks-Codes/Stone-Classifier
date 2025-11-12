#!/bin/bash
# Monitor stone classifier download progress

echo "=================================="
echo "📊 Stone Classifier Download Monitor"
echo "=================================="
echo ""

# Check if script is running
if pgrep -f "download_images.py" > /dev/null; then
    echo "✅ Download script is RUNNING"
    echo "   PID: $(pgrep -f 'download_images.py')"
else
    echo "❌ Download script is NOT RUNNING"
fi

echo ""
echo "=================================="
echo "📁 Image Count by Category"
echo "=================================="

for split in train val; do
    echo ""
    echo "[$split]"
    if [ -d "Stone_Data/$split" ]; then
        for category in Stone_Data/$split/*/; do
            if [ -d "$category" ]; then
                cat_name=$(basename "$category")
                count=$(find "$category" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | wc -l)
                echo "  $cat_name: $count images"
            fi
        done
    else
        echo "  Directory not found"
    fi
done

echo ""
echo "=================================="
echo "💾 Disk Usage"
echo "=================================="
if [ -d "Stone_Data" ]; then
    du -sh Stone_Data
else
    echo "Stone_Data directory not found"
fi

echo ""
echo "=================================="
echo "📝 Recent Log Entries (last 10 lines)"
echo "=================================="
if [ -f "download_log.txt" ]; then
    tail -n 10 download_log.txt
else
    echo "No log file found"
fi

echo ""
echo "=================================="
echo "💻 System Resources"
echo "=================================="
echo "Disk space:"
df -h . | tail -n 1

echo ""
echo "Memory usage:"
free -h | grep "Mem:"

echo ""
echo "=================================="
echo "📌 Quick Commands:"
echo "  Watch live log:     tail -f download_log.txt"
echo "  Stop script:        pkill -f download_images.py"
echo "  Restart script:     nohup python download_images.py > download_log.txt 2>&1 &"
echo "  This monitor again: bash monitor_downloads.sh"
echo "=================================="
