from django.shortcuts import render
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
from django.http import HttpResponse

# Create your views here.

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "potato_model.h5"
)
model = None
def get_model():
    global model
    if model is None:
        model = load_model(MODEL_PATH, compile=False)
    return model

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
    model = get_model()
    img_array = preprocess_image(image)
    predictions = model.predict(img_array)

    predicted_class = class_names[np.argmax(predictions)]
    confidence = float(np.max(predictions))

    return predicted_class, confidence

# Main view
def home(request):
    try:
        if request.method == "POST" and request.FILES.get("image"):
            image = Image.open(request.FILES["image"])

            result, confidence = predict_image(image)

            return render(request, "result.html", {
                "result": result
            })

        return render(request, "index.html")
    except Exception as e:
        return HttpResponse(f"Error: {e}")