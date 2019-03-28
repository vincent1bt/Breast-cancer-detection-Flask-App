from flask import Flask, render_template, request, jsonify

import tensorflow as tf
from keras.models import model_from_json
from keras.applications.mobilenet_v2 import preprocess_input

from PIL import Image
from io import BytesIO
from keras.preprocessing.image import img_to_array
import numpy as np

app = Flask(__name__)
model = None
graph = tf.get_default_graph()

def load_request_image(image):
    image = Image.open(BytesIO(image))
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize((48, 48))
    image = img_to_array(image)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)

    return image

def load_model():
    json_file = open('./model/model.json', 'r')
    model_json = json_file.read()
    json_file.close()
    global model
    model = model_from_json(model_json)
    model.load_weights("./model/weights.h5")

def predict_class(image_array):
    classes = ["Benign", "Malignant"]

    with graph.as_default():
        y_pred = model.predict(image_array, batch_size=None, verbose=0, steps=None)[0]
        class_index = np.argmax(y_pred, axis=0)
        confidence = y_pred[class_index]
        class_predicted = classes[class_index]
        return class_predicted, confidence

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    image = request.files["image"].read()
    image = load_request_image(image)
    class_predicted, confidence = predict_class(image)
    image_class = { "class": class_predicted, "confidence": str(confidence) } 

    return jsonify(image_class)

if __name__ == "__main__":
    load_model()
    app.run(debug = False, threaded = False)

if __name__ == "app":
    load_model()