import React from "react";

import "../css/resultheader.css";

const ResultHeader = () => {
  return (
    <div className="header-wrapper">
      <div className="header-item uprn">UPRN</div>
      <div className="header-item address">Address</div>
      <div className="header-item x-coord">X Coord</div>
      <div className="header-item y-coord">Y Coord</div>
      <div className="header-item lat">Lat</div>
      <div className="header-item lon">Lon</div>
      <div className="header-item link">Google Directions</div>
      <div className="header-item link">OS Maps</div>
    </div>
  );
};

export default ResultHeader;
