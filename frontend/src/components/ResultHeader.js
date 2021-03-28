import React from "react";

import "../css/resultheader.css";

const ResultHeader = () => {
  return (
    <>
      <div className="header-item">UPRN</div>
      <div className="header-item">Address</div>
      <div className="header-item">X Coord</div>
      <div className="header-item">Y Coord</div>
      <div className="header-item">Lat</div>
      <div className="header-item">Lon</div>
    </>
  );
};

export default ResultHeader;
