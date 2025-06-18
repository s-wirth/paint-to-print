"use client";
import React, { useState, useEffect } from "react";
import Image from "next/image";
import styles from "./page.module.css";

export default function Home() {
  const [uploadedImages, setUploadedImages] = useState([]);
  const [contouredImages, setContouredImages] = useState([]);
  const [fileToUpload, setFileToUpload] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedContouredFile, setSelectedContouredFile] = useState(null);
  const [responseData, setResponseData] = useState({
    message: "",
    fileName: "",
    status: "",
  });

  const fetchUploads = async () => {
    console.log('fir')
    const res = await fetch("/api/get-all-uploads");
    const data = await res.json();
    console.log('data', data)
    setUploadedImages(data["files"]);
  }
  const fetchContours = async () => {
    console.log('fir')
    const res = await fetch("/api/get-all-contours");
    const data = await res.json();
    console.log('data', data)
    setContouredImages(data["files"]);
    if (data["files"].length > 0) {
      setSelectedContouredFile(data["files"][0])
    }
  }

  useEffect(() => {
    fetchUploads();
    fetchContours();
  }, []);

  const handleFileChange = (event) => {
    setFileToUpload(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", fileToUpload);

    const response = await fetch("/api/upload-image", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      setResponseData({
        message: data.message,
        fileName: data.filename,
        status: data.status,
      });
      fetchUploads();
    } else {
      setResponseData({
        message: data.message,
        status: data.status,
      });
    }
  };

  const getContour = async () => {
    const response = await fetch("/api/get-contour", {
      method: "POST",
      contentType: "application/json",
      body: JSON.stringify({
        fileName: selectedFile
      })
    });
    const data = await response.json();
    fetchContours();
    console.log('data', data)
  }

  console.log('typeof selectedFile', typeof selectedFile)
  console.log('selectedFile', selectedFile)
  return (
    <main className={styles.main}>
      <div className={styles.fileSelection}>
        <h1>Paint to Print</h1>
        <h2>Uploaded Images</h2>
        {uploadedImages.length > 0 && uploadedImages.map((image) => (
          <Image
            key={image}
            src={`/uploads/${image}`}
            alt="Uploaded Image"
            width={200}
            height={200}
            className={selectedFile === image ? styles.selectedImage + " " + styles.uploadedImage : styles.uploadedImage}
            onClick={() => setSelectedFile(image)}
          />
        ))}
        {selectedFile && <button onClick={getContour}>Get Contour</button>}
        <h2>Contoured Images</h2>
        {contouredImages.length > 0 && contouredImages.map((image) => (
          <Image
            key={image}
            src={`/opencv_store/${image}`}
            alt="Uploaded Image"
            width={200}
            height={200}
            className={selectedContouredFile === image ? styles.selectedContouredImage + " " + styles.contouredImage : styles.contouredImage}
            onClick={() => setSelectedContouredFile(image)}
          />
        ))}
        {responseData.message && <p>{responseData.message}</p>}
        {responseData.fileName && <p>{responseData.fileName}</p>}
        <h2>Upload an Image</h2>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} />
          <button type="submit">Upload</button>
        </form>
      </div>
      <div className={styles.workBench}>
        <div className={styles.workPiece}>
          {selectedContouredFile && (
            <Image
              src={`/opencv_store/${selectedContouredFile}`}
              alt="Contoured Image"
              width={400}
              height={400}
            />
          )}
        </div>
      </div>
    </main>
  );
}
