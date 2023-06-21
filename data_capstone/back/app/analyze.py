import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from django.conf import settings
from tensorflow import keras

analyze_dir = settings.ANALYZE_DIR
model_path = os.path.join(analyze_dir, 'three_landmark_epoch200_patience8.h5')

class ImageAnalyzer:
    def __init__(self):
        self.model = load_model(model_path, compile=False)
        self.class_labels = ['happy', 'neutral', 'sad'] 

    def analyze_image(self, image_path):
        img = cv2.imread(image_path)
        img = cv2.resize(img, (224, 224))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)

        prediction = self.model.predict(img)
        class_index = np.argmax(prediction)
        class_label = self.class_labels[class_index]

        return class_label
