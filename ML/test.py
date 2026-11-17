import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
import os

# Load Models (Update these paths as needed)
RETINA_MODEL_PATH = r"D:\PROJECT1\DIabetic_final\DIA3_\ML\retina_classifier_v2.h5"
DR_MODEL_PATH = r"D:\PROJECT1\DIabetic_final\DIA3_\ML\model.hdf5"

# Load Models (without compiling)
retina_model = tf.keras.models.load_model(RETINA_MODEL_PATH, compile=False)
dr_model = tf.keras.models.load_model(DR_MODEL_PATH, compile=False)

# Compile (optional for inference)
retina_model.compile(optimizer=Adam(learning_rate=0.001), loss="binary_crossentropy")
dr_model.compile(optimizer=Adam(learning_rate=0.001), loss="categorical_crossentropy")

# Labels - ensure this matches your model's training class order!
labels = ["Mild DR","Moderate DR","No DR","Severe DR"]

# Function to check if input is a retina image
def is_retina_image(image_path):
    try:
        img = load_img(image_path, target_size=(224, 224))  # Resize for retina model
        img = img_to_array(img) / 255.0  # Normalize
        img = np.expand_dims(img, axis=0)

        prediction = retina_model.predict(img)[0][0]
        print(f"[Retina Check] Confidence: {prediction:.4f}")
        return prediction > 0.5  # Binary output: retina or not
    except Exception as e:
        print(f"Error in Retina Image Check: {e}")
        return False

# Function to predict Diabetic Retinopathy
def predict(image_path):
    if not os.path.exists(image_path):
        return "Error: Image path does not exist."

    if not is_retina_image(image_path):
        return "Not a retina image. Please upload a valid fundus image."

    try:
        # Preprocess for DR model
        img = load_img(image_path, target_size=(50, 50))  # Resize for DR model
        img = img_to_array(img)
        img = preprocess_input(img)  # Ensure consistent with ResNet preprocessing
        img = np.expand_dims(img, axis=0)

        # Predict
        pred = dr_model.predict(img)
        print("Model Output Probabilities:", pred[0])  # Debug output

        predicted_class = np.argmax(pred, axis=1)[0]
        return labels[predicted_class]

    except Exception as e:
        return f"Error in Prediction: {e}"

# Example test
if __name__ == "__main__":
    print("Test 1:", predict("test_images/retina_sample.jpg"))  # Expected: One of the DR classes
    print("Test 2:", predict("test_images/cat.jpg"))  # Expected: Not a retina image
