"use client";
import { createContext, useContext, useState, useEffect } from "react";
import styles from "./page.module.css";
import { ClientSideContext } from "./client_context";
import Image from "next/image";
import ParameterContainer from "./Components/ParameterContainer";
import ImageCanvas from "./Components/ImageCanvas";

export default function Paint2Print() {
  const blankContourBox = {
    contourBox: {
      topLeft: { x: null, y: null },
      topRight: { x: null, y: null },
      bottomLeft: { x: null, y: null },
      bottomRight: { x: null, y: null },
    },
  };
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
  const [clientParameters, setClientParameters] =
    useState<ClientParameterInterface>(blankContourBox);

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

  const updateContourBox = (e) => {
    const nE = e.nativeEvent;
    const nELx = nE.layerX;
    const nELy = nE.layerY;
    console.log('e', e)

    for (const [key, value] of Object.entries(clientParameters.contourBox)) {
      if (value.x === null && value.y === null) {
        const cB = { ...clientParameters };
        cB.contourBox[key] = { x: nELx, y: nELy };
        setClientParameters(cB);
        break;
      }
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", fileToUpload);
    formData.append("customFileName", customFileName);
    console.log("formData", formData);

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
    formData.append("newValues", JSON.stringify(clientParameters.contourBox));
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
        <ParameterContainer clientParameters={clientParameters} />
        {!allImages && <button onClick={() => makeMeta()}>Make Meta</button>}
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
          {Object.entries(clientParameters.contourBox).map(([key, value]) => (
            <div className={styles.rectangle_point} key={key}>
              {key}: {"["} {value.x || "-"}, {value.y || "-"} {"]"}
            </div>
          ))}
          <button
            className={styles.rectangle_point_reset_button}
            name="reset"
            onClick={() => setClientParameters(blankContourBox)}
          >
            Reset Points
          </button>
        </div>
        <ImageCanvas selectedImage={selectedImage} />
        {false && (
          <div
            className={styles.image_container}
            style={{
              width: selectedImage.displayWidth,
              height: selectedImage.displayHeight,
            }}
            onClick={(e) => updateContourBox(e)}
          >
            <div
              className={styles.cb_point}
              style={{
                display: `${clientParameters.contourBox["topLeft"].x ? "block" : "none"}`,
                top: `${clientParameters.contourBox["topLeft"].y}px`,
                left: `${clientParameters.contourBox["topLeft"].x}px`,
              }}
            />
            <div
              className={styles.cb_point}
              style={{
                display: `${clientParameters.contourBox["topRight"].x ? "block" : "none"}`,
                top: `${clientParameters.contourBox["topRight"].y}px`,
                left: `${clientParameters.contourBox["topRight"].x}px`,
              }}
            />
            <div
              className={styles.cb_point}
              style={{
                display: `${clientParameters.contourBox["bottomLeft"].x ? "block" : "none"}`,
                top: `${clientParameters.contourBox["bottomLeft"].y}px`,
                left: `${clientParameters.contourBox["bottomLeft"].x}px`,
              }}
            />
            <div
              className={styles.cb_point}
              style={{
                display: `${clientParameters.contourBox["bottomRight"].x ? "block" : "none"}`,
                top: `${clientParameters.contourBox["bottomRight"].y}px`,
                left: `${clientParameters.contourBox["bottomRight"].x}px`,
              }}
            />
            <Image
              className={styles.selected_image}
              src={selectedImage.uploadURL}
              alt="Selected Image"
              width={selectedImage.displayWidth}
              height={selectedImage.displayHeight}
            />
          </div>
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
          <button
            type="submit"
            className={styles.upload_button}
            onClick={handleSubmit}
          >
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
