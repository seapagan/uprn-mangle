import React from "react";

import { BsCaretDown } from "react-icons/bs";
import { BsCaretUp } from "react-icons/bs";

import "../css/resultheader.css";

const ResultHeader = () => {
  return (
    <div className="header-wrapper">
      <div className="header-item uprn">
        {/* <BsCaretDown className="select-order" /> */}
        UPRN
      </div>
      <div className="header-item address">
        {/* <BsCaretDown className="select-order" /> */}
        Address
      </div>

      <div className="header-item link">Google Directions</div>
      <div className="header-item link">OS Maps</div>
    </div>
  );
};

export default ResultHeader;
