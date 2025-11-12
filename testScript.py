import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import os
import json

# Load main stone type model
main_model = keras.models.load_model('stone_classifier_model_weighted.h5')

# Load main class indices
with open('class_indices.json', 'r') as f:
    class_indices = json.load(f)

# Create reverse mapping (index -> class name)
idx_to_class = {v: k for k, v in class_indices.items()}
class_names = [idx_to_class[i] for i in range(len(class_indices))]

# Load subtype models if they exist
subtype_models = {}
subtype_indices = {}

for stone_type in class_names:
    model_file = f'{stone_type}_subtype_model.h5'
    indices_file = f'{stone_type}_subtype_indices.json'
    
    if os.path.exists(model_file) and os.path.exists(indices_file):
        subtype_models[stone_type] = keras.models.load_model(model_file)
        with open(indices_file, 'r') as f:
            subtype_indices[stone_type] = json.load(f)
        print(f"Loaded {stone_type} subtype model")

def get_subtypes(stone_type):
    """Get available subtypes for a stone type."""
    subtype_dir = f'Stone_Data/train/{stone_type}'
    if os.path.exists(subtype_dir):
        subtypes = [d for d in os.listdir(subtype_dir) 
                   if os.path.isdir(os.path.join(subtype_dir, d))]
        return subtypes
    return []

def predict_stone(image_path):
    # Load and preprocess
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Stage 1: Predict stone type
    predictions = main_model.predict(img_array, verbose=0)
    predicted_class = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class]
    predicted_stone = class_names[predicted_class]
    
    print(f"Image: {os.path.basename(image_path)}")
    print(f"Predicted Stone Type: {predicted_stone}")
    print(f"Stone Type Confidence: {confidence:.2%}")
    
    # Stage 2: Predict subtype if model exists
    if predicted_stone in subtype_models:
        subtype_model = subtype_models[predicted_stone]
        subtype_preds = subtype_model.predict(img_array, verbose=0)
        subtype_idx = np.argmax(subtype_preds[0])
        subtype_confidence = subtype_preds[0][subtype_idx]
        
        # Get subtype name
        subtype_idx_to_name = {v: k for k, v in subtype_indices[predicted_stone].items()}
        predicted_subtype = subtype_idx_to_name[subtype_idx]
        
        print(f"Predicted {predicted_stone} Subtype: {predicted_subtype}")
        print(f"Subtype Confidence: {subtype_confidence:.2%}")
        
        # Show top 3 subtypes
        top3_indices = np.argsort(subtype_preds[0])[-3:][::-1]
        print(f"\nTop 3 {predicted_stone} subtypes:")
        for idx in top3_indices:
            subtype_name = subtype_idx_to_name[idx]
            prob = subtype_preds[0][idx]
            print(f"  {subtype_name}: {prob:.2%}")
    else:
        # Show available subtypes if no model yet
        subtypes = get_subtypes(predicted_stone)
        if subtypes:
            print(f"\nAvailable {predicted_stone} subtypes (subtype model not trained yet):")
            for subtype in sorted(subtypes):
                print(f"  - {subtype}")
    
    print(f"\nAll stone type probabilities:")
    for i, prob in enumerate(predictions[0]):
        print(f"  {class_names[i]}: {prob:.2%}")
    print()
    
    return predicted_class, confidence

# Test single image from test folder
test_image = 'test/IMG_6893.jpeg'
if os.path.exists(test_image):
    print("Testing image from test folder:")
    predict_stone(test_image)
else:
    print(f"Image not found: {test_image}")
    print("\nAvailable images in test folder:")
    for f in os.listdir('test/'):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"  - {f}")

# OR test multiple images from test folder
print("\n" + "="*50)
print("Testing all images in test folder:")
print("="*50)
test_folder = 'test/'
for img_file in os.listdir(test_folder):
    if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
        predict_stone(os.path.join(test_folder, img_file))
