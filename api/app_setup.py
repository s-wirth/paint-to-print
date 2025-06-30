from flask import Flask
from flask_cors import CORS
import os
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
