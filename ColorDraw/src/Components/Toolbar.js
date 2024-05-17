import '../CSS/toolbar.css';
import React from 'react';
import { useRef, useState } from 'react';

function Toolbar( { strokeColor, lineWidth, clearCanvas, handleImage, saveCanvas, eraseCanvas, paintCanvas } ) {
  const toolbarRef = useRef(null);

  const [isActive, setIsActive] = useState({
    paintActive: true,
    eraseActive: false
});

  function handleClick(e) {
    if (e.target.id === 'paint') {
      setIsActive({paintActive: true, eraseActive: false});
      console.log('paint');
      paintCanvas();
    }
    if(e.target.id === 'erase') {
      setIsActive({paintActive: false, eraseActive: true});
      eraseCanvas();
    }
  }

  return (
    <div id="toolbar" ref={toolbarRef}>
      <div className='toolbarTitle'>
        <h1>Draw!</h1>
      </div>
      <ul>
        <li className='colorContainer'>
          <label htmlFor="stroke">Color</label>
          <input id="stroke" name='stroke' type="color" appearance="none" border="none" height="100px" onChange={(e) => strokeColor.current = e.target.value}></input>
        </li>
        <li className='lineContainer'>
          <label htmlFor="lineWidth">Line Width</label>
          <input id="lineWidth" name='lineWidth' type="number" defaultValue={5} onChange={(e) => lineWidth.current = e.target.value}></input>
        </li>
        <li className='paintOptions'>
          <button id="paint" className={`paint ${isActive.paintActive ? 'active' : 'inactive'}`} onClick={handleClick}>Paint</button>
          <button id="erase" className={`erase ${isActive.eraseActive ? 'active' : 'inactive'}`} onClick={handleClick}>Erase</button>
        </li>
        <li><button id="clear" onClick={clearCanvas}>Clear</button></li>
        <li><button id="save" onClick={saveCanvas}>Download</button></li>
        <li className='fileUploadContainer'>
          <label htmlFor="file" className="custom-file-upload">Upload Image</label>
          <input type="file" id="file" name="file" accept="image/png, image/jpeg" onChange={handleImage}/>
        </li>
      </ul>
    </div>
  );
}

export default Toolbar;
