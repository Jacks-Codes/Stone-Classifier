import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json 
import os
import numpy as np
from sklearn.utils.class_weight import compute_class_weight

img_size= 224
batch_size = 32
epochs = 15
data_dir = "Stone_Data"

train_dir = os.path.join(data_dir, 'train')
val_dir = os.path.join(data_dir, 'val')

train_datagen = ImageDataGenerator(
    rescale = 1./255,
    shear_range = 0.2,
    zoom_range = 0.2,
    rotation_range = 20,
    width_shift_range = 0.2,
    height_shift_range = 0.2,
    brightness_range = [0.8,1.2],
    horizontal_flip = True,
    fill_mode = "nearest"
)

val_datagen = ImageDataGenerator(rescale = 1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size = (224,224),
    batch_size = 32,
    class_mode = "categorical"
)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size = (224,224),
    batch_size = 32,
    class_mode = "categorical"
)

num_classes = len(train_generator.class_indices)

# Calculate class weights to handle imbalance
print("\nCalculating class weights...")
class_counts = {}
for class_name, class_idx in train_generator.class_indices.items():
    class_dir = os.path.join(train_dir, class_name)
    if os.path.exists(class_dir):
        # Count all image files recursively
        count = 0
        for root, dirs, files in os.walk(class_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    count += 1
        class_counts[class_name] = count
        print(f"  {class_name}: {count} images")
    else:
        print(f"  Warning: {class_dir} not found")

# Compute class weights (inverse frequency weighting)
total_samples = sum(class_counts.values())
if total_samples == 0:
    print("Error: No images found. Check your data directory.")
    exit(1)

class_weights = {}
for class_name, class_idx in train_generator.class_indices.items():
    if class_name in class_counts and class_counts[class_name] > 0:
        # Weight inversely proportional to frequency
        weight = total_samples / (num_classes * class_counts[class_name])
        class_weights[class_idx] = weight
        print(f"  {class_name} (idx {class_idx}): weight = {weight:.3f}")
    else:
        print(f"  Warning: No images found for {class_name}, using default weight")
        class_weights[class_idx] = 1.0

print("\nClass weights:", class_weights)

base_model = keras.applications.MobileNetV2(
input_shape = (224,224,3),
include_top = False,
weights = 'imagenet'
)

base_model.trainable = False

model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(256, activation = 'relu'),
    layers.Dropout(.3),
    layers.Dense(128, activation = 'relu'),
    layers.Dropout(.2),
    layers.Dense(num_classes, activation = 'softmax')
])

model.compile(
    optimizer = keras.optimizers.Adam(learning_rate=0.001),
    loss = 'categorical_crossentropy',
    metrics = ['accuracy']
)

print("\nStarting training with class weights...")
history = model.fit(
    train_generator,
    epochs = epochs,
    validation_data = val_generator,
    class_weight = class_weights,  # Add class weights here
    verbose = 1
)

model.save('stone_classifier_model_weighted.h5')

with open('class_indices.json', 'w') as f:
    json.dump(train_generator.class_indices, f)

print("\nModel training completed and saved")
print(f"Classes: {num_classes}")
print(f"Class indices: {train_generator.class_indices}")
print(f"\nModel saved as 'stone_classifier_model_weighted.h5'")

