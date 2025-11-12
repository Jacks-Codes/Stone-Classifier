import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import json
import os
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Load model and class indices
model = keras.models.load_model('stone_classifier_model.h5')
with open('class_indices.json', 'r') as f:
    class_indices = json.load(f)

# Reverse mapping for readable labels
idx_to_class = {v: k for k, v in class_indices.items()}
class_names = [idx_to_class[i] for i in range(len(class_indices))]

# Setup data generators
data_dir = "Stone_Data"
val_dir = os.path.join(data_dir, 'val')

val_datagen = ImageDataGenerator(rescale=1./255)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=False  # Important: don't shuffle for evaluation
)

# Get true labels and predictions
print("Evaluating model on validation set...")
y_true = val_generator.classes
y_pred_proba = model.predict(val_generator, verbose=1)
y_pred = np.argmax(y_pred_proba, axis=1)

# Overall accuracy
accuracy = np.mean(y_true == y_pred)
print(f"\n{'='*60}")
print(f"Overall Validation Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"{'='*60}\n")

# Classification report
print("Classification Report:")
print(classification_report(y_true, y_pred, target_names=class_names))

# Confusion matrix
cm = confusion_matrix(y_true, y_pred)
print("\nConfusion Matrix:")
print(cm)

# Visualize confusion matrix
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=class_names, yticklabels=class_names)
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150)
print("\nConfusion matrix saved to 'confusion_matrix.png'")

# Per-class accuracy
print("\n" + "="*60)
print("Per-Class Accuracy:")
print("="*60)
for i, class_name in enumerate(class_names):
    class_mask = y_true == i
    if np.sum(class_mask) > 0:
        class_acc = np.mean(y_pred[class_mask] == i)
        count = np.sum(class_mask)
        print(f"{class_name:15s}: {class_acc:.4f} ({class_acc*100:.2f}%) - {count} samples")
    else:
        print(f"{class_name:15s}: No samples")

# Data distribution check
print("\n" + "="*60)
print("Validation Set Distribution:")
print("="*60)
unique, counts = np.unique(y_true, return_counts=True)
for idx, count in zip(unique, counts):
    print(f"{class_names[idx]:15s}: {count:4d} samples ({count/len(y_true)*100:.1f}%)")

# Check for misclassifications
print("\n" + "="*60)
print("Most Common Misclassifications:")
print("="*60)
misclassifications = {}
for true_idx, pred_idx in zip(y_true, y_pred):
    if true_idx != pred_idx:
        key = (class_names[true_idx], class_names[pred_idx])
        misclassifications[key] = misclassifications.get(key, 0) + 1

# Sort by frequency
sorted_mis = sorted(misclassifications.items(), key=lambda x: x[1], reverse=True)
for (true_class, pred_class), count in sorted_mis[:10]:
    print(f"{true_class:15s} -> {pred_class:15s}: {count:3d} times")

print("\nEvaluation complete!")

