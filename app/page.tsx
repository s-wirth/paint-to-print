"use client";
import { createContext, useContext, useState, useEffect } from "react";
import styles from "./page.module.css";
import { ClientSideContext } from "./client_context";
import Image from "next/image";

export default function Paint2Print() {
  const blankPoints = {
    topLeft: { x: null, y: null },
    topRight: { x: null, y: null },
    bottomLeft: { x: null, y: null },
    bottomRight: { x: null, y: null },
  };
  const [rectanglePoints, setRectanglePoints] = useState(blankPoints);
  const [uploadedImages, setUploadedImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [allImages, setAllImages] = useState(null);
  const [fileToUpload, setFileToUpload] = useState(null);
  const [customFileName, setCustomFileName] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [responseData, setResponseData] = useState({
    message: "",
    fileName: "",
    status: "",
  });

  const fetchUploads = async () => {
    const res = await fetch("/api/get-all-uploads");
    const data = await res.json();
    setUploadedImages(data["files"]);
  };

  const fetchImageMeta = async () => {
    const res = await fetch("/api/image-meta", {
      method: "GET",
    });
    const data = await res.json();
    setAllImages(data);
    if (selectedImage == null) {
      setSelectedImage(Object.values(data)[0]);
    }
  };

  useEffect(() => {
    fetchUploads();
    fetchImageMeta();
  }, []);

  const handleFileChange = (event) => {
    setFileToUpload(event.target.files[0]);
  };

  const handleDelete = async (imageID) => {
    const formData = new FormData();
    formData.append("imageID", imageID);
    const response = await fetch(`/api/delete-image`, {
      method: "POST",
      body: formData,
    });
    if (response.ok) {
      fetchUploads();
      fetchImageMeta();
    }
  };

  const handleImageClick = (e) => {
    let ratioX = e.target.naturalWidth / e.target.offsetWidth;
    let ratioY = e.target.naturalHeight / e.target.offsetHeight;

    let domX = e.pageX + window.pageXOffset - e.target.offsetLeft;
    let domY = e.pageY + window.pageYOffset - e.target.offsetTop;

    let imgX = Math.floor(domX * ratioX);
    let imgY = Math.floor(domY * ratioY);

    const points = [imgX, imgY];
    for (const [key, value] of Object.entries(rectanglePoints)) {
      if (value.x === null && value.y === null) {
        setRectanglePoints((prev) => ({
          ...prev,
          [key]: { x: imgX, y: imgY },
        }));
        break;
      }
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", fileToUpload);
    formData.append("customFileName", customFileName);
    console.log('formData', formData)

    const response = await fetch("/api/upload-image", {
      method: "POST",
      body: formData,
    });
    if (response.ok) {
      fetchUploads();
      fetchImageMeta();
      setCustomFileName("");
      setFileToUpload(null);
    }
  };

  const makeMeta = async () => {
    const response = await fetch("/api/make-meta", {
      method: "GET",
    });
    if (response.ok) {
      fetchImageMeta();
    }
  };

  const makeProcessingMeta = async () => {
    const formData = new FormData();
    formData.append("image", JSON.stringify(selectedImage));
    const response = await fetch("/api/image-processing-meta", {
      method: "POST",
      body: formData,
    });
    console.log("selectedImage", selectedImage);
    if (response.ok) {
      console.log("response", response);
    }
  };

  const submitBoundingRectPointsToMeta = async () => {
    const formData = new FormData();
    formData.append("image", JSON.stringify(selectedImage));
    formData.append("newValues", JSON.stringify(rectanglePoints));
    const response = await fetch("/api/update-processing-meta", {
      method: "POST",
      body: formData,
    });
    if (response.ok) {
      fetchImageMeta();
    }
  };

  const createContour = async () => {
    submitBoundingRectPointsToMeta();
    const formData = new FormData();
    formData.append("image", JSON.stringify(selectedImage));
    const response = await fetch("/api/create-contour", {
      method: "POST",
      body: formData,
    });
    if (response.ok) {
      fetchImageMeta();
    }
  };

  return (
    <main className={styles.main}>
      <div className={styles.parameter_container}>
        <h2>Parameters</h2>

        {!allImages && (
          <button onClick={() => makeMeta()}>Make Meta</button>
        )}
        <button onClick={() => makeProcessingMeta()}>
          Make Processing Meta
        </button>
        <button onClick={() => submitBoundingRectPointsToMeta()}>
          Submit Bounding Rect Points to Meta
        </button>
        <button onClick={() => createContour()}>Create Contour</button>
      </div>
      <div className={styles.display_container}>
        <div className={styles.rectangle_point_wrapper}>
          {Object.entries(rectanglePoints).map(([key, value]) => (
            <div className={styles.rectangle_point} key={key}>
              {key}: {"["} {value.x || "-"}, {value.y || "-"} {"]"}
            </div>
          ))}
          <button
            className={styles.rectangle_point_reset_button}
            name="reset"
            onClick={() => setRectanglePoints(blankPoints)}
          >
            Reset Points
          </button>
        </div>
        {selectedImage && (
          <Image
            className={styles.selected_image}
            src={selectedImage.uploadURL}
            alt="Selected Image"
            onClick={(e) => handleImageClick(e)}
            width={selectedImage.displayWidth}
            height={selectedImage.displayHeight}
          />
        )}
      </div>
      <div className={styles.up_and_down_loads_container}>
        <h2 className={styles.upload_header}>Upload an Image</h2>
        <form onSubmit={handleSubmit} className={styles.upload_form}>
          <input
            type="file"
            onChange={handleFileChange}
            className={styles.file_input}
          />
          <input
            id="customFileName"
            type="text"
            onChange={(e) => setCustomFileName(e.target.value)}
            placeholder="Custom File Name"
          />
          <button type="submit" className={styles.upload_button} onClick={handleSubmit}>
            Upload
          </button>
        </form>
        <h2 className={styles.upload_header}>All Images</h2>
        <div className={styles.uploaded_images}>
          {allImages &&
            Object.values(allImages).map((image) => (
              <div
                className={
                  selectedImage && selectedImage.id === image.id
                    ? styles.uploaded_image_wrapper_selected
                    : styles.uploaded_image_wrapper
                }
                key={image.id}
                onClick={() => setSelectedImage(image)}
              >
                <div className={styles.uploaded_image_name}>
                  {image.customName}
                </div>
                <div
                  className={styles.uploaded_image_delete}
                  onClick={() => handleDelete(image.id)}
                >
                  X
                </div>
              </div>
            ))}
        </div>
      </div>
    </main>
  );
}
