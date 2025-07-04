from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
import pickle
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
from PIL import Image
import webbrowser
import threading

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load tokenizer and model
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

model = tf.keras.models.load_model('mymodel.h5')

# Load MobileNetV2 model for feature extraction
mobilenet = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

# Max caption length (adjust if needed)
max_length = 34

def extract_features(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    features = mobilenet.predict(img)
    return features

def generate_caption(model, tokenizer, photo, max_length):
    in_text = 'startseq'
    for _ in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = next((k for k, v in tokenizer.word_index.items() if v == yhat), None)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'endseq':
            break
    return in_text.replace('startseq', '').replace('endseq', '').strip()

def open_browser():
    webbrowser.get("windows-default").open("http://127.0.0.1:5000")

@app.route('/', methods=['GET', 'POST'])
def index():
    caption = None
    image_path = None
    if request.method == 'POST':
        file = request.files['image']
        if file:
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

            features = extract_features(image_path)
            caption = generate_caption(model, tokenizer, features, max_length)
    return render_template('index.html', caption=caption, image_path=image_path)

if __name__ == '__main__':
    app.run(debug=True)
