"use client";
import React, { useState, useEffect } from "react";
import Image from "next/image";
export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [responseData, setResponseData] = useState({
    message: "",
    fileName: "",
  });

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', selectedFile);

    const response = await fetch('/api/upload-image', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      setResponseData({
        message: data.message,
        fileName: data.filename,
      });
      console.log('File uploaded successfully');
    } else {
      console.error('Error uploading file');
    }
  };


  return (
    <main>
      {responseData.message && <p>{responseData.message}</p>}
      {responseData.fileName && <p>{responseData.fileName}</p>}
      {responseData.fileName && <Image src={`/uploads/${responseData.fileName}`} alt="Uploaded Image" width={200} height={200} />}
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
    </main>
  );
}
