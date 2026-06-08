import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

class ImageClassifier:
    def __init__(self, model_path="models/cifar10_model.h5"):
        self.model = None
        self.class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                            'dog', 'frog', 'horse', 'ship', 'truck']
        self.load_model(model_path)
    
    def load_model(self, model_path):
        if os.path.exists(model_path):
            print(f"Loading model from {model_path}")
            self.model = keras.models.load_model(model_path)
        else:
            print(f"Model not found at {model_path}")
            self.model = self.create_simple_model()

    def create_simple_model(self):
        model = keras.Sequential([keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224,224,3)),
                                  keras.layers.MaxPooling2D((2,2)),
                                  keras.layers.Conv2D(64, (3,3), activation='relu'),
                                  keras.layers.MaxPooling2D((2,2)),
                                  keras.layers.Conv2D(64, (3,3), activation='relu'),
                                  keras.layers.Flatten(),
                                  keras.layers.Dense(64, activation='relu'),
                                  keras.layers.Dense(10, activation='softmax')])
        
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model
    
    def preprocess_image(self, image_array):
        image_array = image_array.astype('float32') / 255.0 #Normalize pixel value to [0,1]
        image_array = np.expand_dims(image_array, axis=0) #add batch dimension
        return image_array
    
    def predict(self, image_array):
        if self.model is None:
            return "Model not loaded"
        
        processed_image = self.preprocess_image(image_array)

        predictions = self.model.predict(processed_image)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        return {"class": self.class_names[predicted_class_idx],
                "confidence": confidence,
                "all_predictions": {self.class_names[i]: float(predictions[0][i])
                                    for i in range(len(self.class_names))}}