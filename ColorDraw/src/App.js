import './App.css';
import Toolbar from './Components/Toolbar';
import Canvas from './Components/Canvas';
import { useRef } from 'react';

function App() {
  const strokeColor = useRef('#000000');
  const lineWidth = useRef(5);
  const canvasRef = useRef(null);
  const mouseCoordinates = useRef({ x: 0, y: 0 });
  let ctx;
  let canvas;

  const clearCanvas = () => {
    canvas = canvasRef.current;
    ctx = canvasRef.current.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    canvas.style.height = '100vh';
    canvas.style.width = '100%';
  };

  const saveCanvas = () => {
    canvas = canvasRef.current;
    var image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
    window.location.href=image; //save locally
  }

  const eraseCanvas = () => {
    canvas = canvasRef.current;
    ctx = canvasRef.current.getContext('2d');
    ctx.globalCompositeOperation = "destination-out";
    strokeColor.current = 'rgba(0,0,0,1)';
  };

  const paintCanvas = () => {
    canvas = canvasRef.current;
    ctx = canvasRef.current.getContext('2d');
    ctx.globalCompositeOperation = "source-over";
    // strokeColor.current = 'rgba(0,0,0,1)';
  };

  function handleImage(e){
    const canvas = canvasRef.current;
    const ctx = canvasRef.current.getContext('2d');
    var reader = new FileReader();
    reader.onload = function(event){
        const img = new Image();
        img.onload = function(){
          const canvasOffsetX = canvas.offsetLeft;
          const canvasOffsetY = canvas.offsetTop;

          canvas.style.height = 'auto';
          canvas.style.width = 'auto';
          canvas.style.border = 'solid black 1px';

          // Save the current canvas size
          const currentWidth = canvas.width;
          const currentHeight = canvas.height;
          
          canvas.width = img.width;
          canvas.height = img.height;
          ctx.drawImage(img, 0, 0);

          const rect = canvas.getBoundingClientRect();
          // const mouseX = e.clientX - rect.left;
          // const mouseY = e.clientY - rect.top;
          console.log(rect);

          // canvas.width = window.innerWidth - canvasOffsetX;
          // canvas.height = window.innerHeight - canvasOffsetY;

          // Calculate the new pointer's position relative to the resized canvas
          const mouseX = (e.clientX/canvas.width * img.width);
          const mouseY = (e.clientY/canvas.height * img.height);

          // const mouseX = (currentWidth/canvas.offsetLeft) * img.width;
          // const mouseY = (currentHeight/canvas.offsetTop) * img.height;
          mouseCoordinates.current = {x : mouseX, y : mouseY};

          // Move the painting start position to the new pointer's position
          ctx.beginPath();
          ctx.moveTo(mouseCoordinates.current.x, mouseCoordinates.current.y);
        }
        img.src = event.target.result;
    }
    
    reader.readAsDataURL(e.target.files[0]);     
  }

  return (
      <section className="container">
      <Toolbar strokeColor={strokeColor}
        lineWidth={lineWidth}
        clearCanvas={clearCanvas}
        handleImage={handleImage}
        saveCanvas={saveCanvas}
        eraseCanvas={eraseCanvas}
        paintCanvas={paintCanvas}/>
      <Canvas strokeColor={strokeColor} lineWidth={lineWidth} mouseCoordinates={mouseCoordinates} canvasRef = {canvasRef}/>
    </section>
  );
}

export default App;
