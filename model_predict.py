import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

_model = None
_class_names = None

def _load_resources():
    global _model, _class_names
    if _model is None:
        _model = load_model("crop_disease_model.h5")
        with open("class_indices.json") as f:
            class_indices = json.load(f)
        _class_names = {v: k for k, v in class_indices.items()}
    return _model, _class_names

def predict_disease(img_path):
    model, class_names = _load_resources()
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array, verbose=0)[0]
    idx = int(np.argmax(predictions))
    disease = class_names[idx]
    confidence = round(float(predictions[idx]) * 100, 2)
    return disease, confidence