import React, { useRef, useEffect, useState } from "react";
import styles from "./imageCanvas.module.css";
import NextImage from "next/image";

export default function ImageCanvas({ selectedImage }: any) {
  const displayWidth = selectedImage ? selectedImage.displayWidth : 0;
  const displayHeight = selectedImage ? selectedImage.displayHeight : 0;
  const canvasRef = useRef(null);
  const [pointList, setPointList] = useState([]);

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

  const drawLine = (startX, startY, endX, endY) => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    context.beginPath();
    context.moveTo(startX, startY);
    context.lineTo(endX, endY);
    context.lineWidth = 2;
    context.strokeStyle = "yellow";
    context.stroke();
  }

  const handleClick = (e) => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    const pX = e.clientX - canvas.getBoundingClientRect().left;
    const pY = e.clientY - canvas.getBoundingClientRect().top;
    if (pointList.length === 0) {
      context.fillStyle = "rgb(0 100 0 / 50%)";
      context.fillRect(0,0, canvas.width,canvas.height);
    }
    if (pointList.length > 0) {
      drawLine(pointList[pointList.length - 1].x, pointList[pointList.length - 1].y, pX, pY);
    }
    if (pointList.length === 3) {
      drawLine(pointList[0].x, pointList[0].y, pX, pY);
    }
    setPointList([...pointList, { x: pX, y: pY }]);
  }
  return (
    <div className={styles.canvas_container}>
      {pointList.length > 0 && pointList.map((point, index) => (
        <div
          key={index}
          className={styles.cP}
          style={{ left: (point.x - 5), top: (point.y - 5) }}
        />
      ))}
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
