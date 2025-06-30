from flask import Flask, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import json
import helpers
from constants import *

########################################################################
# SETUP FOR APP
########################################################################

app = Flask(__name__)
cors = CORS(app)  # allow CORS for all domains on all routes.
app.config["CORS_HEADERS"] = "Content-Type"
app.config["SECRET_KEY"] = "super secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OPENCV_STORE_FOLDER"] = OPENCV_STORE_FOLDER
app.config["IMAGE_META_JSON"] = IMAGE_META_JSON_FILE
app.config["IMAGE_PROCESSING_META_JSON"] = IMAGE_PROCESSING_META_JSON_FILE


########################################################################
# CREATE PATH CONSTANTS
########################################################################

PATH_TO_UPLOADS = helpers.ending_slash(
    os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"])
)
PATH_TO_STORE = helpers.ending_slash(
    os.path.join(os.getcwd(), app.config["OPENCV_STORE_FOLDER"])
)
PATH_TO_IMAGE_META = os.path.join(os.getcwd(), app.config["IMAGE_META_JSON"])
PATH_TO_IMAGE_PROCESSING_META = os.path.join(
    os.getcwd(), app.config["IMAGE_PROCESSING_META_JSON"]
)


########################################################################
# ROUTES
########################################################################


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


########################################################################
# META ROUTES
########################################################################


@app.route("/api/make-meta", methods=["GET"])
def makeMeta():
    allFiles = os.listdir(PATH_TO_UPLOADS)
    files = [f for f in allFiles if helpers.check_valid_image(PATH_TO_UPLOADS + f)]
    if helpers.makeImageMetaData(files, PATH_TO_IMAGE_META):
        return json.dumps({"message": "success"})
    return json.dumps({"message": "failed"})


@app.route("/api/image-processing-meta", methods=["POST"])
def imageProcessingMeta():
    if request.method != "POST":
        return
    helpers.pprint(request.form.get("image"))
    helpers.make_image_processing_meta(
        request.form.get("image"), PATH_TO_IMAGE_PROCESSING_META
    )
    return json.dumps({"message": "success"})


@app.route("/api/update-processing-meta", methods=["POST"])
def updateProcessingMeta():
    if request.method != "POST":
        return
    helpers.pprint(request.form.get("image"))
    helpers.pprint(request.form.get("newValues"))
    helpers.update_processing_meta(
        request.form.get("image"),
        request.form.get("newValues"),
        PATH_TO_IMAGE_PROCESSING_META,
    )
    return json.dumps({"message": "success"})


@app.route("/api/image-meta", methods=["GET", "POST"])
def imageMeta():
    if request.method != "GET":
        return
    with open(PATH_TO_IMAGE_META, encoding="utf-8") as json_file:
        data = json.load(json_file)
    return json.dumps(data)


########################################################################
# UPLOAD ROUTES
########################################################################


@app.route("/api/get-all-uploads", methods=["GET"])
def getAllUploads():
    allFiles = os.listdir(PATH_TO_UPLOADS)
    files = [f for f in allFiles if helpers.check_valid_image(PATH_TO_UPLOADS + f)]
    return json.dumps({"files": files})


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
    customFileName = request.form.get("customFileName") or helpers.get_file_name(
        file.filename
    )
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
        image_meta_data["images"].append(
            {
                "customFileName": customFileName,
                "filename": filename,
                "upload_url": helpers.get_file_upload_url(filename),
                "opencv_url": "",
                "id": len(image_meta_data["images"]) + 1,
                "width": helpers.get_image_dimensions(newFile)[1],
                "height": helpers.get_image_dimensions(newFile)[0],
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


########################################################################
# DELETION ROUTES
########################################################################


@app.route("/api/delete-image", methods=["POST"])
def deleteImage():
    if request.method != "POST":
        return
    image_meta_data = {}
    imageID = request.form.get("imageID")
    with open(PATH_TO_IMAGE_META, "r") as json_file:
        image_meta_data = json.load(json_file)
    with open(PATH_TO_IMAGE_META, "w") as json_file:
        del image_meta_data[imageID]
        json_file.write(json.dumps(image_meta_data, indent=4))
    return (
        json.dumps(
            {
                "message": f"File deleted successfully to {PATH_TO_UPLOADS}",
                "status": 200,
            }
        ),
        200,
    )
