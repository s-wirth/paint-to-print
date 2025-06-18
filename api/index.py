from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import json
import cv2
import sys
import os

UPLOAD_FOLDER = "public/uploads"
OPENCV_STORE_FOLDER = "public/opencv_store"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)


cors = CORS(app)  # allow CORS for all domains on all routes.
app.config["CORS_HEADERS"] = "Content-Type"


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OPENCV_STORE_FOLDER"] = OPENCV_STORE_FOLDER
app.config["SECRET_KEY"] = "super secret key"


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
    allFiles = os.listdir(uploadFolder)
    files = [f for f in allFiles if os.path.isfile(os.path.join(uploadFolder, f)) and allowed_file(f)]
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
    opencvFolder = os.path.join(os.getcwd(), app.config["OPENCV_STORE_FOLDER"])
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
        if os.path.exists(os.path.join(uploadFolder, filename)):
            image = os.path.join(uploadFolder, filename)
            newName = 'contour_' + filename.split(".")[0] + '.jpg'
            # Load the image
            img = cv2.imread(image)

            # convert to grayscale
            cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            edged = cv2.Canny(img, 120, 890)
            # Apply adaptive threshold
            thresh = cv2.adaptiveThreshold(edged, 255, 1, 1, 11, 2)
            cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

            # apply some dilation and erosion to join the gaps - change iteration to detect more or less area's
            thresh = cv2.dilate(thresh, None, iterations=50)
            thresh = cv2.erode(thresh, None, iterations=50)

            # Find the contours
            contours, hierarchy = cv2.findContours(
                thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
            )

            # For each contour, find the bounding rectangle and draw it
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 20000:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
            if not os.path.exists(opencvFolder):
                os.makedirs(opencvFolder)
            
            cv2.imwrite(os.path.join(opencvFolder, newName), img)

            return (
                json.dumps(
                    {
                        "message": "File uploaded successfully to " + opencvFolder,
                        "filename": newName,
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
