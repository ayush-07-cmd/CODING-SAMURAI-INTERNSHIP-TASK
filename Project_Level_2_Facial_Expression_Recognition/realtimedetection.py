import cv2
import numpy as np
from keras.models import model_from_json, Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, InputLayer

# === Load the model ===
with open('facialemotionmodel.json', 'r') as json_file:
    model_json = json_file.read()

# Important: Include 'custom_objects' to recognize 'Sequential'
model = model_from_json(model_json, custom_objects={"Sequential": Sequential})
model.load_weights("facialemotionmodel.h5")
print("✅ Model loaded successfully.")

# === Load Haar Cascade for face detection ===
haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)

# === Function to preprocess face image ===
def extract_features(image):
    feature = np.array(image).reshape(1, 48, 48, 1)
    return feature / 255.0

# === Define emotion labels ===
labels = {
    0: 'angry',
    1: 'disgust',
    2: 'fear',
    3: 'happy',
    4: 'neutral',
    5: 'sad',
    6: 'surprise'
}

# === Start webcam feed ===
webcam = cv2.VideoCapture(0)

print("🎥 Starting webcam. Press 'q' to quit.")

while True:
    ret, frame = webcam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (48, 48))
        img = extract_features(face)

        prediction = model.predict(img, verbose=0)
        label = labels[np.argmax(prediction)]

        # Draw rectangle and label
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.putText(frame, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imshow('Facial Expression Recognition', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
print("🛑 Webcam stopped.")
