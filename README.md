# Crop Disease Detection System

## About

Crop Disease Detection System is a Python-based desktop application that uses a Convolutional Neural Network (CNN) to detect crop diseases from leaf images. Users can upload an image, and the trained deep learning model analyzes it and predicts the corresponding crop condition.

The application includes a Tkinter-based graphical interface, SQLite database integration for user authentication, and text-to-speech functionality for prediction results.

## Features

* User registration and login
* Password hashing using hashlib
* Crop leaf image upload
* CNN-based disease classification
* Image preprocessing and resizing
* Prediction result display
* Text-to-speech prediction output
* SQLite database integration
* Tkinter graphical user interface

## Disease Classes

The model can classify images into four categories:

* Healthy
* Early Blight
* Late Blight
* Powdery Mildew

## Dataset

* Training images: 1,369
* Validation images: 341
* Input image size: 224 × 224 pixels

## Tech Stack

Python, TensorFlow, Keras, CNN, Tkinter, SQLite, OpenCV, PIL, NumPy, hashlib, py

