"""
Train subtype classifier for a specific stone type.
Usage: python train_subtype_model.py <stone_type>
Example: python train_subtype_model.py marble
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import os
import sys
import numpy as np

if len(sys.argv) < 2:
    print("Usage: python train_subtype_model.py <stone_type>")
    print("Example: python train_subtype_model.py marble")
    sys.exit(1)

stone_type = sys.argv[1].lower()
data_dir = "Stone_Data"
train_dir = os.path.join(data_dir, 'train', stone_type)
val_dir = os.path.join(data_dir, 'val', stone_type)

if not os.path.exists(train_dir):
    print(f"Error: {train_dir} does not exist")
    sys.exit(1)

if not os.path.exists(val_dir):
    print(f"Error: {val_dir} does not exist")
    sys.exit(1)

print(f"Training {stone_type} subtype classifier...")
print(f"Train directory: {train_dir}")
print(f"Val directory: {val_dir}")

img_size = 224
batch_size = 32
epochs = 15

train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    brightness_range=[0.8, 1.2],
    horizontal_flip=True,
    fill_mode="nearest"
)

val_datagen = ImageDataGenerator(rescale=1./255)

# Clean corrupted images
print("\nChecking for corrupted images...")
from PIL import Image
import glob

def check_corrupted_images(directory):
    """Check for corrupted image files without deleting."""
    corrupted = []
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
    
    for ext in image_extensions:
        for img_path in glob.glob(os.path.join(directory, '**', ext), recursive=True):
            try:
                img = Image.open(img_path)
                img.load()
                img.close()
            except Exception as e:
                if "UnidentifiedImageError" in str(type(e).__name__) or "cannot identify" in str(e).lower():
                    corrupted.append(img_path)
    
    return corrupted

corrupted_train = check_corrupted_images(train_dir)
corrupted_val = check_corrupted_images(val_dir)

if corrupted_train or corrupted_val:
    print(f"WARNING: Found {len(corrupted_train)} corrupted images in train, {len(corrupted_val)} in val")
    print("These will be skipped during training.")

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical'
)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical'
)

num_classes = len(train_generator.class_indices)
print(f"\nFound {num_classes} {stone_type} subtypes:")
for subtype, idx in train_generator.class_indices.items():
    print(f"  {idx}: {subtype}")

# Calculate class weights
print("\nCalculating class weights...")
class_counts = {}
for subtype, subtype_idx in train_generator.class_indices.items():
    subtype_dir = os.path.join(train_dir, subtype)
    if os.path.exists(subtype_dir):
        count = 0
        for root, dirs, files in os.walk(subtype_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    count += 1
        class_counts[subtype] = count
        print(f"  {subtype}: {count} images")

total_samples = sum(class_counts.values())
class_weights = {}
for subtype, subtype_idx in train_generator.class_indices.items():
    if subtype in class_counts and class_counts[subtype] > 0:
        weight = total_samples / (num_classes * class_counts[subtype])
        class_weights[subtype_idx] = weight
        print(f"  {subtype} (idx {subtype_idx}): weight = {weight:.3f}")

print("\nClass weights:", class_weights)

# Build model
base_model = keras.applications.MobileNetV2(
    input_shape=(img_size, img_size, 3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False

model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print(f"\nStarting training for {stone_type} subtypes...")
history = model.fit(
    train_generator,
    epochs=epochs,
    validation_data=val_generator,
    class_weight=class_weights,
    verbose=1
)

# Save model
model_filename = f'{stone_type}_subtype_model.h5'
model.save(model_filename)

# Save class indices
indices_filename = f'{stone_type}_subtype_indices.json'
with open(indices_filename, 'w') as f:
    json.dump(train_generator.class_indices, f, indent=2)

print(f"\nModel training completed!")
print(f"Model saved as: {model_filename}")
print(f"Class indices saved as: {indices_filename}")
print(f"Classes: {num_classes}")
print(f"Class indices: {train_generator.class_indices}")

