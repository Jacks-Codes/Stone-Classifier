import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json 
import os

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

history = model.fit(
    train_generator,
    epochs = epochs,
    validation_data = val_generator,
    verbose = 1
)

model.save('stone_classifier_model.h5')

with open('class_indices.json', 'w') as f:
    json.dump(train_generator.class_indices, f)

print("Model training completed and saved")
print(f"Classes: {num_classes}")
print(f"Class indices: {train_generator.class_indices}")
