import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import os

# Load model
model = keras.models.load_model('stone_classifier_model_weighted.h5')

# Your class names (adjust based on your actual classes)
class_names = ['granite', 'marble', 'quartz', 'travertine']

def predict_stone(image_path):
    # Load and preprocess
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Predict
    predictions = model.predict(img_array, verbose=0)
    predicted_class = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class]
    
    print(f"Image: {os.path.basename(image_path)}")
    print(f"Predicted: {class_names[predicted_class]}")
    print(f"Confidence: {confidence:.2%}")
    print(f"All probabilities:")
    for i, prob in enumerate(predictions[0]):
        print(f"  {class_names[i]}: {prob:.2%}")
    print()
    
    return predicted_class, confidence

# Test single image
predict_stone('Stone_Data/test/granite/some_image.jpg')

# OR test multiple images
test_folder = 'Stone_Data/test/'
for stone_type in os.listdir(test_folder):
    stone_path = os.path.join(test_folder, stone_type)
    if os.path.isdir(stone_path):
        print(f"\n=== Testing {stone_type} ===")
        for img_file in os.listdir(stone_path)[:5]:  # test first 5
            if img_file.endswith('.jpg'):
                predict_stone(os.path.join(stone_path, img_file))
