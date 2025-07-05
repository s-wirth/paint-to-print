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
      p1: { x: null, y: null },
      p2: { x: null, y: null },
      p3: { x: null, y: null },
      p4: { x: null, y: null },
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
  const [bbSelectionActive, setBBSelectionActive] = useState(false);
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
        <ParameterContainer clientParameters={clientParameters} bbSelectionActive={bbSelectionActive} setBBSelectionActive={setBBSelectionActive} />
      </div>
      <div className={styles.display_container}>
        <ImageCanvas selectedImage={selectedImage} bbSelectionActive={bbSelectionActive} setClientParameters={setClientParameters} />
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
