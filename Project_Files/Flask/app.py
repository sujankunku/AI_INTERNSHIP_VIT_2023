"""
Flask APP Development
"""

from flask import Flask, render_template, request, jsonify
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from tensorflow.keras.models import load_model

model_vgg16 = load_model("BuildingWeights_vgg16.h5")

app = Flask(__name__)


@app.route('/')
def load_home_page():
    return render_template("index.html")


@app.route("/index.html")
def load_index_page():
    return render_template("index.html")


@app.route("/intro.html")
def load_intro_page():
    return render_template("intro.html")


def predict_img(filepath):
    user_input_img = image.load_img(filepath, target_size=(224, 224))
    user_input_img = image.img_to_array(user_input_img)
    user_input_img = np.expand_dims(user_input_img, axis=0)
    pred = np.argmax(model_vgg16.predict(user_input_img))
    print(pred)
    output = ['Cracked', 'Non-cracked']
    outputDescription = {
        "cracked": "A defect was detected by our model upon thorough analysis.We recommend engaging an expert in the field to conduct a detailed examination and provide guidance on rectifying the issue promptly.",
        "not-cracked": "Great news! there are no apparent building defects. The construction quality seems to meet the highest industry standards, ensuring a robust and secure structure."
    }
    print(output[pred])
    if output[pred] == 'Cracked':
        print("Building Has a Defect!!! Better repair it!")
        return outputDescription["cracked"]
    else:
        print("Building has no Defect!!!")
        return outputDescription["not-cracked"]


@app.route("/upload.html", methods=['GET', 'POST'])
def load_upload_page():
    if request.method == "POST":
        input_file = request.files['image']
        print("input_file =", input_file)
        basepath = os.path.dirname(__file__)
        print("basepath =", basepath)
        filepath = os.path.join(basepath, 'upload', input_file.filename)
        input_file.save(filepath)
        print("filepath =", filepath)
        result = predict_img(filepath)
        return jsonify({'display_output': result})
    else:
        return render_template("upload.html")


if __name__ == '__main__':
    app.run()
