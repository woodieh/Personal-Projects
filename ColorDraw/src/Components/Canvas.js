import '../CSS/canvas.css';
import React from 'react';
import { useRef, useEffect } from 'react';

function Canvas({ strokeColor, lineWidth, canvasRef, mouseCoordinates }) {
  const isPainting = useRef(false);
  let ctx;
  let rect;
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) {
      alert('canvas not found');
      return;
    }
    ctx = canvas.getContext('2d');
    if (!ctx) {
      alert('canvas context not found');
      return; 
    }

    const canvasOffsetX = canvas.offsetLeft;
    const canvasOffsetY = canvas.offsetTop;

    canvas.width = window.innerWidth - canvasOffsetX;
    canvas.height = window.innerHeight - canvasOffsetY;

    function draw(e) {
      rect = canvas.getBoundingClientRect();
      canvas.style.cursor = 'crosshair';
      if(!isPainting.current) {
          return;
      }
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;
      mouseCoordinates.current = {x : mouseX, y : mouseY};

      ctx.lineWidth = lineWidth.current;
      ctx.lineCap = 'round';
      ctx.strokeStyle = strokeColor.current;

      ctx.lineTo(mouseCoordinates.current.x, mouseCoordinates.current.y);
      ctx.stroke();
    }

    const handleMouseDown = (e) => {
      const rect = canvas.getBoundingClientRect();
      isPainting.current = true;
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;
      mouseCoordinates.current = {x : mouseX, y : mouseY};
      console.log(mouseCoordinates.current);
      console.log(rect);
      ctx.beginPath();
      ctx.moveTo(mouseCoordinates.current.x, mouseCoordinates.current.y);
    };
  
    const handleMouseUp = (e) => {
      isPainting.current = false;
      ctx.closePath();
    };

    canvas.addEventListener('mousedown', handleMouseDown);
    canvas.addEventListener('mouseup', handleMouseUp);
    canvas.addEventListener('mousemove', draw);

    return () => {
      canvas.removeEventListener('mousedown', handleMouseDown);
      canvas.removeEventListener('mouseup', handleMouseUp);
      canvas.removeEventListener('mousemove', draw);
    };
}, [lineWidth, strokeColor]);

  return (
    <div className='canvasContainer'>
        <canvas id="drawingCanvas" ref={canvasRef}></canvas>
    </div>
  );
}

export default Canvas;
