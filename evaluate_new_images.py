"""
Helper script to evaluate new images before adding them to the dataset.
This helps you identify which images from your website would be most valuable.
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import json
import os
import sys
from pathlib import Path

# Load model and class indices
model = keras.models.load_model('stone_classifier_model.h5')
with open('class_indices.json', 'r') as f:
    class_indices = json.load(f)

idx_to_class = {v: k for k, v in class_indices.items()}
class_names = [idx_to_class[i] for i in range(len(class_indices))]

def predict_image(image_path, target_class=None):
    """Predict a single image and return results."""
    try:
        # Load and preprocess image
        img = load_img(image_path, target_size=(224, 224))
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Predict
        predictions = model.predict(img_array, verbose=0)[0]
        predicted_idx = np.argmax(predictions)
        predicted_class = class_names[predicted_idx]
        confidence = predictions[predicted_idx]
        
        # Get top 3 predictions
        top3_indices = np.argsort(predictions)[-3:][::-1]
        top3 = [(class_names[i], predictions[i]) for i in top3_indices]
        
        result = {
            'image': image_path,
            'predicted_class': predicted_class,
            'confidence': float(confidence),
            'top3': top3,
            'is_correct': predicted_class == target_class if target_class else None
        }
        
        return result
    except Exception as e:
        return {'error': str(e), 'image': image_path}

def evaluate_directory(directory, target_class=None):
    """Evaluate all images in a directory."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
    image_paths = [str(p) for p in Path(directory).rglob('*') if p.suffix in image_extensions]
    
    if not image_paths:
        print(f"No images found in {directory}")
        return []
    
    print(f"\nEvaluating {len(image_paths)} images...")
    if target_class:
        print(f"Target class: {target_class}")
    
    results = []
    for img_path in image_paths:
        result = predict_image(img_path, target_class)
        results.append(result)
    
    return results

def print_results(results, target_class=None):
    """Print evaluation results in a helpful format."""
    if not results:
        return
    
    print("\n" + "="*70)
    print("EVALUATION RESULTS")
    print("="*70)
    
    # Group by prediction
    by_prediction = {}
    correct = []
    incorrect = []
    low_confidence = []
    
    for r in results:
        if 'error' in r:
            print(f"\nERROR with {r['image']}: {r['error']}")
            continue
        
        pred = r['predicted_class']
        if pred not in by_prediction:
            by_prediction[pred] = []
        by_prediction[pred].append(r)
        
        if target_class:
            if r['is_correct']:
                correct.append(r)
            else:
                incorrect.append(r)
        
        if r['confidence'] < 0.7:
            low_confidence.append(r)
    
    # Summary
    print(f"\nTotal images evaluated: {len(results)}")
    if target_class:
        print(f"Correctly predicted as {target_class}: {len(correct)} ({len(correct)/len(results)*100:.1f}%)")
        print(f"Incorrectly predicted: {len(incorrect)} ({len(incorrect)/len(results)*100:.1f}%)")
    
    print(f"\nLow confidence predictions (<0.7): {len(low_confidence)}")
    
    # Breakdown by predicted class
    print("\nPredicted as:")
    for pred_class, pred_results in sorted(by_prediction.items(), key=lambda x: len(x[1]), reverse=True):
        avg_conf = np.mean([r['confidence'] for r in pred_results])
        print(f"  {pred_class:15s}: {len(pred_results):3d} images (avg confidence: {avg_conf:.3f})")
    
    # Recommendations
    print("\n" + "="*70)
    print("RECOMMENDATIONS")
    print("="*70)
    
    if target_class:
        if len(correct) > 0:
            print(f"\n✓ Good images for {target_class} dataset:")
            for r in sorted(correct, key=lambda x: x['confidence'], reverse=True)[:5]:
                print(f"  {os.path.basename(r['image']):50s} (conf: {r['confidence']:.3f})")
        
        if len(incorrect) > 0:
            print(f"\n⚠ Images that might confuse the model (predicted as something else):")
            for r in sorted(incorrect, key=lambda x: x['confidence'], reverse=True)[:5]:
                print(f"  {os.path.basename(r['image']):50s} -> {r['predicted_class']} (conf: {r['confidence']:.3f})")
    
    if low_confidence:
        print(f"\n⚠ Low confidence images (might need better quality or clearer features):")
        for r in sorted(low_confidence, key=lambda x: x['confidence'])[:5]:
            print(f"  {os.path.basename(r['image']):50s} -> {r['predicted_class']} (conf: {r['confidence']:.3f})")
    
    # Best candidates
    print(f"\n✓ Best candidates to add (high confidence, correct prediction):")
    if target_class:
        best = [r for r in correct if r['confidence'] > 0.8]
    else:
        best = sorted(results, key=lambda x: x['confidence'], reverse=True)
    
    for r in best[:10]:
        print(f"  {os.path.basename(r['image']):50s} -> {r['predicted_class']} (conf: {r['confidence']:.3f})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python evaluate_new_images.py <image_directory> [target_class]")
        print("\nExample:")
        print("  python evaluate_new_images.py ./new_marble_images marble")
        print("  python evaluate_new_images.py ./new_quartzite_images quartzite")
        sys.exit(1)
    
    directory = sys.argv[1]
    target_class = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist")
        sys.exit(1)
    
    if target_class and target_class not in class_names:
        print(f"Error: '{target_class}' is not a valid class")
        print(f"Valid classes: {', '.join(class_names)}")
        sys.exit(1)
    
    results = evaluate_directory(directory, target_class)
    print_results(results, target_class)

