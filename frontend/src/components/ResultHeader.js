import React from "react";

import "../css/resultheader.css";

const ResultHeader = () => {
  return (
    <div className="header-wrapper">
      <div className="header-item uprn">UPRN</div>
      <div className="header-item address">Address</div>

      <div className="header-item link">Google Directions</div>
      <div className="header-item link">OS Maps</div>
    </div>
  );
};

export default ResultHeader;
