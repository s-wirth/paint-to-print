import React, { useRef, useEffect, useState } from "react";
import styles from "./imageCanvas.module.css";
import NextImage from "next/image";

export default function ImageCanvas({ selectedImage }: any) {
  const displayWidth = selectedImage ? selectedImage.displayWidth : 0;
  const displayHeight = selectedImage ? selectedImage.displayHeight : 0;
  const canvasRef = useRef(null);
  const [cP, setCp] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    if (!canvas || !context || !selectedImage) {
      return;
    }
    const image = new Image();
    image.src = selectedImage.uploadURL;
    image.onload = () => {
      context.drawImage(image, 0, 0, displayWidth, displayHeight);
    };
  }, [selectedImage]);

  const handleClick = (e) => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    console.log('canvas.getBoundingClientRect(', canvas.getBoundingClientRect())
    console.log('e', e)
    const pX = e.clientX - canvas.getBoundingClientRect().left - 5;
    const pY = e.clientY - canvas.getBoundingClientRect().top - 5;
    console.log('pX, pY', pX, pY)
    const imageData = context.getImageData(pX, pY, 1, 1);
    setCp({ x: pX, y: pY });
  }
  return (
    <div className={styles.canvas_container}>
      <div className={styles.cP} style={{ left: cP.x, top: cP.y }}/>
      <canvas
        onClick={handleClick}
        className={styles.image_canvas}
        ref={canvasRef}
        width={displayWidth}
        height={displayHeight}
      />
    </div>
  );
}
