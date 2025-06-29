"use client";
import { createContext, useContext, useState, useEffect } from "react";
import styles from "./page.module.css";
import { ClientSideContext } from "./client_context";
import Image from "next/image";

export default function Paint2Print() {
  const [uploadedImages, setUploadedImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState({});
  const [allImages, setAllImages] = useState({});
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
    console.log('data.images', data)
    setAllImages(data);
    setSelectedImage(Object.values(data)[0]);
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

  console.log('selectedImage', selectedImage)

  return (
    <main className={styles.main}>
      <div className={styles.parameter_container}>
        <h2>Parameters</h2>
        <form action="">
          <input name="param1" type="number" placeholder="Parameter 1" />
        </form>
      </div>
      <div className={styles.display_container}>
        <h2>Display</h2>
        {JSON.stringify(allImages) == "{}" && <button onClick={() => makeMeta()}>Make Meta</button>}
        {JSON.stringify(selectedImage) !== "{}" && (
          <Image
            src={selectedImage.uploadURL}
            alt="Selected Image"
            width={selectedImage.displayWidth}
            height={selectedImage.displayHeight}
          />
        )}
      </div>
      <div className={styles.up_and_down_loads_container}>
        <h2>Upload an Image</h2>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} />
          <input type="text"  onChange={(e) => setCustomFileName(e.target.value)}/>
          <button type="submit">Upload</button>
        </form>
        <h2>All Images</h2>
        <div className={styles.uploaded_images}>
          {Object.values(allImages).map((image) => (
            <div className={styles.uploaded_image_wrapper} key={image.id} onClick={() => setSelectedImage(image)}>
              <div className={styles.uploaded_image_name}>{image.customName}</div>
              <div className={styles.uploaded_image_delete} onClick={() => handleDelete(image.id)}>X</div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
