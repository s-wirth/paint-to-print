"use client";
import { createContext, useContext, useState, useEffect } from "react";
import styles from "./page.module.css";
import { ClientSideContext } from "./client_context";
import Image from "next/image";

export default function Paint2Print() {
  const [uploadedImages, setUploadedImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState({});
  const [allImages, setAllImages] = useState([]);

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
    setAllImages(data.images);
    setSelectedImage(data.images[0]);
  };

  useEffect(() => {
    fetchUploads();
    fetchImageMeta();
  }, []);

  console.log('allImages', allImages)
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
        {JSON.stringify(selectedImage) !== "{}" && (
          <Image
            src={selectedImage.upload_url}
            alt="Selected Image"
            width={600}
            height={400}
          />
        )}
      </div>
      <div className={styles.up_and_down_loads_container}>
        <ul className={styles.uploaded_images}>
          {allImages.length > 0 &&
            allImages.map((image) => (
              <li key={image.id} onClick={() => setSelectedImage(image)}>
                <p>{image.name}</p>
              </li>
            ))}
        </ul>
      </div>
    </main>
  );
}
