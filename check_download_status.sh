#!/bin/bash
# Diagnostic script to check download status

echo "=== Stone Classifier Download Status ==="
echo ""

# Count total images
TRAIN_COUNT=$(find Stone_Data/train -name "*.jpg" -o -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
VAL_COUNT=$(find Stone_Data/val -name "*.jpg" -o -name "*.png" 2>/dev/null | wc -l | tr -d ' ')

echo "📊 Total Images:"
echo "   Train: $TRAIN_COUNT"
echo "   Val:   $VAL_COUNT"
echo ""

# Check types with images
echo "📁 Stone Types with Train Images:"
TRAIN_TYPES=$(find Stone_Data/train -mindepth 2 -type d -exec sh -c 'count=$(find "$1" -maxdepth 1 \( -name "*.jpg" -o -name "*.png" \) 2>/dev/null | wc -l | tr -d " "); if [ "$count" -gt 0 ]; then echo "  $1: $count images"; fi' _ {} \; | wc -l | tr -d ' ')
echo "   Found: $TRAIN_TYPES types with train images"

echo ""
echo "📁 Stone Types with Val Images:"
VAL_TYPES=$(find Stone_Data/val -mindepth 2 -type d -exec sh -c 'count=$(find "$1" -maxdepth 1 \( -name "*.jpg" -o -name "*.png" \) 2>/dev/null | wc -l | tr -d " "); if [ "$count" -gt 0 ]; then echo "  $1: $count images"; fi' _ {} \; | wc -l | tr -d ' ')
echo "   Found: $VAL_TYPES types with val images"

echo ""
echo "🔍 Sample - First 5 types with train images:"
find Stone_Data/train -mindepth 2 -type d -exec sh -c 'count=$(find "$1" -maxdepth 1 \( -name "*.jpg" -o -name "*.png" \) 2>/dev/null | wc -l | tr -d " "); if [ "$count" -gt 0 ]; then echo "  $(basename $(dirname "$1"))/$(basename "$1"): $count train images"; fi' _ {} \; | head -5

echo ""
echo "🔍 Sample - First 5 types with val images:"
find Stone_Data/val -mindepth 2 -type d -exec sh -c 'count=$(find "$1" -maxdepth 1 \( -name "*.jpg" -o -name "*.png" \) 2>/dev/null | wc -l | tr -d " "); if [ "$count" -gt 0 ]; then echo "  $(basename $(dirname "$1"))/$(basename "$1"): $count val images"; fi' _ {} \; | head -5

echo ""
echo "🔍 Checking for incomplete types (has train but no val):"
find Stone_Data/train -mindepth 2 -type d | while read train_dir; do
    type_name=$(basename "$train_dir")
    category=$(basename $(dirname "$train_dir"))
    val_dir="Stone_Data/val/$category/$type_name"
    
    train_count=$(find "$train_dir" -maxdepth 1 \( -name "*.jpg" -o -name "*.png" \) 2>/dev/null | wc -l | tr -d ' ')
    val_count=$(find "$val_dir" -maxdepth 1 \( -name "*.jpg" -o -name "*.png" \) 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$train_count" -gt 0 ] && [ "$val_count" -eq 0 ]; then
        echo "  ⚠️  $category/$type_name: $train_count train, 0 val"
    fi
done | head -10

echo ""
echo "🔄 Script Status:"
if pgrep -f download_images.py > /dev/null; then
    echo "   ✅ Script is running (PID: $(pgrep -f download_images.py))"
else
    echo "   ❌ Script is NOT running"
fi

echo ""
echo "📝 Recent log entries (if download_log.txt exists):"
if [ -f download_log.txt ]; then
    tail -20 download_log.txt
else
    echo "   No log file found"
fi

