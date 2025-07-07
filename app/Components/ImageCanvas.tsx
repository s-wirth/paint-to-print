import React, { useRef, useEffect, useState } from "react";
import styles from "./imageCanvas.module.css";
import NextImage from "next/image";

export default function ImageCanvas({ selectedImage, bbSelectionActive, setBBSelectionActive, setClientParameters }: any) {
  const displayWidth = selectedImage ? selectedImage.displayWidth : 0;
  const displayHeight = selectedImage ? selectedImage.displayHeight : 0;
  const canvasRef = useRef(null);
  const [bgImage, setBgImage] = useState(null);
  const [pointList, setPointList] = useState([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    if (!canvas || !context || !selectedImage) {
      return;
    }
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(bgImage, 0, 0, canvas.width, canvas.height);
    if (bbSelectionActive) {
          context.fillStyle = "rgb(100 100 0 / 50%)";
          context.fillRect(0,0, canvas.width,canvas.height);
        }
    else if (pointList.length === 4) {
            for (let i = 0; i < pointList.length; i++) {
              switch (i) {
                case 3:
                  drawLine(pointList[i].x, pointList[i].y, pointList[0].x, pointList[0].y, true);
                  break;
                default:
                  drawLine(pointList[i].x, pointList[i].y, pointList[i + 1].x, pointList[i + 1].y, true);
              }
            }
            setPointList([]);
          }
  }, [bbSelectionActive])
  

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    if (!canvas || !context || !selectedImage) {
      return;
    }
    const image = new Image();
    image.src = selectedImage.uploadURL;
    image.onload = () => {
      setBgImage(image);
      context.drawImage(image, 0, 0, displayWidth, displayHeight);
    };
  }, [selectedImage]);

  const drawLine = (startX, startY, endX, endY, calledFromUE=false) => {
    if (calledFromUE) {
      // console.log('startX', startX)
      // console.log('startY', startY)
      // console.log('endX', endX)
      // console.log('endY', endY)
    }
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
    if (!bbSelectionActive) {
      return;
    }
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    const pX = e.clientX - canvas.getBoundingClientRect().left;
    const pY = e.clientY - canvas.getBoundingClientRect().top;
    if (pointList.length > 0) {
      drawLine(pointList[pointList.length - 1].x, pointList[pointList.length - 1].y, pX, pY, false);
    }
    if (pointList.length === 3) {
      drawLine(pointList[0].x, pointList[0].y, pX, pY, false);
      setBBSelectionActive(false);
      setClientParameters({
        contourBox: {
          p1: {
            x: pointList[0].x,
            y: pointList[0].y
          },
          p2: {
            x: pointList[1].x,
            y: pointList[1].y
          },
          p3: {
            x: pointList[2].x,
            y: pointList[2].y
          },
          p4: {
            x: pX,
            y: pY
          }
        }
      });
      
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
