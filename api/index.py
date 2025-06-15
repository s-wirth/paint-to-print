from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import json
import cv2
import sys
import os

UPLOAD_FOLDER = "public/uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)


cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super secret key'

def pprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/hello", methods=["GET"])
def hello():
    return json.dumps({"message": "Hello, Again!"})


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/api/get-all-uploads", methods=["GET"])
def getAllUploads():
    uploadFolder = os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"])
    files = os.listdir(uploadFolder)
    pprint(files)
    return json.dumps({"files": files})

@app.route("/api/upload-image", methods=["POST"])
def uploadImage():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uploadFolder = os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"])
            if not os.path.exists(uploadFolder):
                os.makedirs(uploadFolder)
            newFile = os.path.join(uploadFolder, filename)
            if os.path.exists(newFile):
                return json.dumps({"message": "File already exists", "filename": filename, "status": 400})
            file.save(newFile)
            return json.dumps({"message": "File uploaded successfully to " + uploadFolder, "filename": filename, "status": 200}), 200
        else:
            return json.dumps({"message": "File type is not allowed", "filename": filename, "status": 400}), 400