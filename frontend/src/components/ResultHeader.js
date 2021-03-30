import React from "react";

import "../css/resultheader.css";

const ResultHeader = () => {
  return (
    <div className="header-wrapper">
      <div className="header-item uprn">UPRN</div>
      <div className="header-item address">Address</div>
      <div className="header-item">X Coord</div>
      <div className="header-item">Y Coord</div>
      <div className="header-item">Lat</div>
      <div className="header-item">Lon</div>
      <div className="header-item">Google Directions</div>
      <div className="header-item">Open StreetMap</div>
    </div>
  );
};

export default ResultHeader;
