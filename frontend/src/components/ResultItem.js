import React from "react";

import { FaMap } from "react-icons/fa";
import { SiGooglemaps } from "react-icons/si";
import "../css/resultitem.css";

const ResultItem = ({ result }) => {
  return (
    <div className="result-container">
      <div className="result uprn">{result.uprn}</div>
      <div className="result address">{result.full_address}</div>
      <div className="result x-coord">{result.x_coordinate}</div>
      <div className="result y-coord">{result.y_coordinate}</div>
      <div className="result lat">{result.latitude}</div>
      <div className="result lon">{result.longitude}</div>
      <div className="result link google">
        <SiGooglemaps />
      </div>
      <div className="result link openstreet">
        <FaMap />
      </div>
    </div>
  );
};

export default ResultItem;
