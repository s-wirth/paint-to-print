from flask import Flask, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import json
import helpers

UPLOAD_FOLDER = "public/uploads"
OPENCV_STORE_FOLDER = "public/opencv_store"
DEFAULT_SETTINGS_JSON_FILE = "server_side/default_settings.json"
USER_SETTINGS_JSON_FILE = "server_side/user_settings.json"
IMAGE_META_JSON_FILE = "server_side/image_meta.json"

app = Flask(__name__)


cors = CORS(app)  # allow CORS for all domains on all routes.
app.config["CORS_HEADERS"] = "Content-Type"


app.config["SECRET_KEY"] = "super secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OPENCV_STORE_FOLDER"] = OPENCV_STORE_FOLDER
app.config["IMAGE_META_JSON"] = IMAGE_META_JSON_FILE


PATH_TO_UPLOADS = helpers.ending_slash(os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"]))
PATH_TO_STORE = helpers.ending_slash(os.path.join(os.getcwd(), app.config["OPENCV_STORE_FOLDER"]))
PATH_TO_IMAGE_META = os.path.join(os.getcwd(), app.config["IMAGE_META_JSON"])


@app.route("/api/init", methods=["GET"])
def init():
    helpers.check_or_create_directory(PATH_TO_UPLOADS)
    helpers.check_or_create_directory(PATH_TO_STORE)
    return json.dumps(
        {
            "message": "initialized",
            "path_to_uploads": PATH_TO_UPLOADS,
            "path_to_store": PATH_TO_STORE,
            "status": 200,
        }
    )


@app.route("/api/get-all-uploads", methods=["GET"])
def getAllUploads():
    allFiles = os.listdir(PATH_TO_UPLOADS)
    files = [
        f
        for f in allFiles
        if helpers.check_valid_image(PATH_TO_UPLOADS + f)
    ]
    return json.dumps({"files": files})

@app.route("/api/image-meta", methods=["GET", "POST"])
def imageMeta():
    if request.method != "GET":
        return
    with open(PATH_TO_IMAGE_META, encoding="utf-8") as json_file:
        data = json.load(json_file)
    helpers.pprint(data)
    return json.dumps(data)


@app.route("/api/upload-image", methods=["POST"])
def uploadImage():
    if request.method != "POST":
        return
    # check if the post request has the file part
    if "file" not in request.files:
        flash("No file part")
        return json.dumps(
            {
                "message": "No file part",
                "status": 400,
            }
        )
    file = request.files["file"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    if not file or not helpers.check_valid_image(file.filename):
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
    filename = secure_filename(file.filename)
    newFile = os.path.join(PATH_TO_UPLOADS, filename)
    if os.path.exists(newFile):
        return json.dumps(
            {
                "message": "File already exists",
                "filename": filename,
                "status": 400,
            }
        )
    file.save(newFile)
    image_meta_data = {}
    with open(PATH_TO_IMAGE_META, "r") as json_file:
        image_meta_data = json.load(json_file)
    with open(PATH_TO_IMAGE_META, "w") as json_file:
        helpers.pprint(image_meta_data)
        image_meta_data["images"].append(
            {
                "name": helpers.get_file_name(filename),
                "upload_url": helpers.get_file_upload_url(filename),
                "opencv_url": "",
                "id": len(image_meta_data["images"]) + 1,
                "width": 600,
                "height": 400,
            }
        )
        json_file.write(json.dumps(image_meta_data, indent=4))
    return (
        json.dumps(
            {
                "message": f"File uploaded successfully to {PATH_TO_UPLOADS}",
                "filename": filename,
                "status": 200,
            }
        ),
        200,
    )
