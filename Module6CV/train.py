import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
from model import ImageClassifier

def download_and_prepare_data():
    print("Downloading CIFAR-10 dataset")

    (x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

    # Normalize pixel values
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0

    # Resize image
    x_train_resized = []
    x_test_resized = []
    
    print("Resizing training images...")
    for i in range(len(x_train)):
        img = tf.image.resize(x_train[i], [224,224])
        x_train_resized.append(img.numpy())

    print("Resizing test images...")
    for i in range(len(x_train)):
        img = tf.image.resize(x_test[i], [224,224])
        x_test_resized.append(img.numpy())

    x_train = np.array(x_train_resized)
    x_test = np.array(x_test_resized)
    return (x_train, y_train), (x_test, y_test)

def train_model():
    print("Starting model training...")
    os.makedirs("models", exist_ok=True)

    classifier = ImageClassifier()
    model = classifier.model
    (x_train, y_train), (x_test, y_test) = download_and_prepare_data()

    print("Training the data shape: {x_train.shape}")
    print("Training the label shape: {y_train.shape}")
    print("Testing the data shape: {x_test.shape}")
    print("Testing the label shape: {y_test.shape}")
    print("Training the model...")