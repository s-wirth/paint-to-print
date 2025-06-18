from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import json
import os
from imageProcessing import processContour
# from helpers import pprint

UPLOAD_FOLDER = "public/uploads"
OPENCV_STORE_FOLDER = "public/opencv_store"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)


cors = CORS(app)  # allow CORS for all domains on all routes.
app.config["CORS_HEADERS"] = "Content-Type"


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OPENCV_STORE_FOLDER"] = OPENCV_STORE_FOLDER
app.config["SECRET_KEY"] = "super secret key"


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
    allFiles = os.listdir(uploadFolder)
    files = [f for f in allFiles if os.path.isfile(os.path.join(uploadFolder, f)) and allowed_file(f)]
    return json.dumps({"files": files})


@app.route("/api/get-all-contours", methods=["GET"])
def getAllContours():
    contourFolder = os.path.join(os.getcwd(), app.config["OPENCV_STORE_FOLDER"])
    allFiles = os.listdir(contourFolder)
    files = [f for f in allFiles if os.path.isfile(os.path.join(contourFolder, f)) and allowed_file(f)]
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
                return json.dumps(
                    {
                        "message": "File already exists",
                        "filename": filename,
                        "status": 400,
                    }
                )
            file.save(newFile)
            return (
                json.dumps(
                    {
                        "message": "File uploaded successfully to " + uploadFolder,
                        "filename": filename,
                        "status": 200,
                    }
                ),
                200,
            )
        else:
            return (
                json.dumps(
                    {
                        "message": "File type is not allowed",
                        "filename": filename,
                        "status": 400,
                    }
                ),
                400,
            )


@app.route("/api/get-contour", methods=["POST"])
def getContour():
    uploadFolder = os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"])
    openCVFolder = os.path.join(os.getcwd(), app.config["OPENCV_STORE_FOLDER"])
    if not os.path.exists(openCVFolder):
        os.makedirs(openCVFolder)
    if request.method == "POST":
        content = request.get_json(silent=True, force=True)
        if content['fileName']:
            filename = content['fileName']
        else:
            return (
                json.dumps(
                    {
                        "message": "File name not provided",
                        "status": 400,
                    }
                ),
                400,
            )
        pathToImage = os.path.join(uploadFolder, filename)
        if os.path.exists(pathToImage):
            contouredImage = processContour(pathToImage, filename, openCVFolder)
            return (
                json.dumps(
                    {
                        "message": "File uploaded successfully to " + openCVFolder,
                        "filename": contouredImage,
                        "status": 200,
                    }
                ),
                200,
            )
        else:
            return (
                json.dumps(
                    {
                        "message": "File does not exist",
                        "status": 400,
                    }
                ),
                400,
            )
