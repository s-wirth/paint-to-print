from flask import Flask, flash, request, redirect
from werkzeug.utils import secure_filename
import os
import json
from image_meta_helpers import *
from image_processing_helpers import *
from helpers import *
from app_setup import *
from image_processing import *


########################################################################
# ROUTES
########################################################################

@app.route("/api/init", methods=["GET"])
def init():
    check_or_create_directory(PATH_TO_UPLOADS)
    check_or_create_directory(PATH_TO_STORE)
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
    files = [f for f in allFiles if check_valid_image(PATH_TO_UPLOADS + f)]
    if makeImageMetaData(files, PATH_TO_IMAGE_META):
        return json.dumps({"message": "success"})
    return json.dumps({"message": "failed"})


@app.route("/api/image-processing-meta", methods=["POST"])
def imageProcessingMeta():
    if request.method != "POST":
        return
    pprint(request.form.get("image"))
    make_image_processing_meta(
        request.form.get("image"), PATH_TO_IMAGE_PROCESSING_META
    )
    return json.dumps({"message": "success"})


@app.route("/api/update-processing-meta", methods=["POST"])
def updateProcessingMeta():
    if request.method != "POST":
        return
    pprint(request.form.get("image"))
    pprint(request.form.get("newValues"))
    update_processing_meta(
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
    files = [f for f in allFiles if check_valid_image(PATH_TO_UPLOADS + f)]
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
    customFileName = request.form.get("customFileName") or get_file_name(
        file.filename
    )
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    if not file or not check_valid_image(file.filename):
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
                "upload_url": get_file_upload_url(filename),
                "opencv_url": "",
                "id": len(image_meta_data["images"]) + 1,
                "width": get_image_dimensions(newFile)[1],
                "height": get_image_dimensions(newFile)[0],
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


########################################################################
# IMAGE PROCESSING ROUTES
########################################################################

@app.route("/api/create-contour", methods=["POST"])
def create_contour():
    IP_create_contour_from_points(request.form.get("image"))
    return json.dumps({"message": "success"})