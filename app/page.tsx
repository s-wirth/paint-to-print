"use client";
import React, { useState, useEffect } from "react";
import Image from "next/image";
export default function Home() {
  const [image, setImage] = useState("");
  const [uploadMessage, setUploadMessage] = useState("");
  const [imageUrl, setImageUrl] = useState("");

  // const makeImage =(file) => {
  //     // assume only one file - read it, and when it's ready, upload to google drive
  //   const reader = new FileReader();
  //   reader.onload = () => {
  //       console.log(file)
  //       console.log('reader.result', reader.result)
  //       fetch('/api/image', {
  //           method: 'POST',
  //           headers: {
  //               'Content-Type': file.type,
  //               'Content-Length': file.size
  //           },
  //           body: reader.result
  //       })
  //       .then(data => data.json())
  //       .then(console.log)
  //       .catch(console.error)
  //   }
  //   reader.readAsArrayBuffer(image);
  // };
  // const uploadImage = () => {
  //   fetch("/api/image", {
  //     method: "POST",
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //     body: {
  //       files: JSON.stringify(image),
  //     },
  //   })
  //     .then((response) => response.json())
  //     .then((data) => setUploadMessage(data.message));
  // };

  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', selectedFile);

    const response = await fetch('/api/image', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      console.log('File uploaded successfully');
    } else {
      console.error('Error uploading file');
    }
  };


  return (
    <main>
      <h1>{uploadMessage}</h1>
      <p>Input: {imageUrl}</p>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
    </main>
  );
}
