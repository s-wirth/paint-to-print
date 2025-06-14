from flask import Flask
import json
import cv2

app = Flask(__name__)

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/api/hello', methods=['GET'])
def hello():
    return json.dumps({'message': 'Hello, Again!'})