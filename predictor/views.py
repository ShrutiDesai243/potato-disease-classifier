from django.shortcuts import render
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os

# Create your views here.

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "potato_model.keras"
)

model = load_model(MODEL_PATH)

# Class names (IMPORTANT: same order as training)
class_names = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']

# Preprocess image
def preprocess_image(image):
    image = image.convert("RGB")
    image = image.resize((256, 256))
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Prediction function
def predict_image(image):
    img_array = preprocess_image(image)
    predictions = model.predict(img_array)

    predicted_class = class_names[np.argmax(predictions)]
    confidence = float(np.max(predictions))

    return predicted_class, confidence

# Main view
def home(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = Image.open(request.FILES["image"])

        result, confidence = predict_image(image)

        return render(request, "result.html", {
            "result": result,
            "confidence": round(confidence * 100, 2)
        })

    return render(request, "index.html")