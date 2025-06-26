"use client";
import { createContext, useContext, useState, useEffect } from "react";
import styles from "./page.module.css";
import { ClientSideContext } from "./client_context";

export default function Paint2Print() {
  const [uploadedImages, setUploadedImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState("");

  const fetchUploads = async () => {
    const res = await fetch("/api/get-all-uploads");
    const data = await res.json();
    setUploadedImages(data["files"]);
  }

  useEffect(() => {
    fetchUploads();
  }, []);

  return (
    <ClientSideContext.Provider value={{ selectedImage: "" }}>
      <main className={styles.main}>
        <div className={styles.parameter_container}>
          <h2>Parameters</h2>
          <form action="">
            <input name="param1" type="number" placeholder="Parameter 1" />
          </form>
        </div>
        <div className={styles.display_container}>
          <h2>Display</h2>
          {selectedImage && (
            <img src={selectedImage} alt="Selected Image" />
          )}
        </div>
        <div className={styles.up_and_down_loads_container}>
          <ul className={styles.uploaded_images}>
            {uploadedImages.length > 0 && uploadedImages.map((file) => (
              <li key={file} onClick={() => setSelectedImage(file)}>
                <p>{file}</p>
              </li>
            ))}
          </ul>
        </div>
      </main>
    </ClientSideContext.Provider>
  );
}
