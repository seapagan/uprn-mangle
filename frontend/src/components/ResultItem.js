import React from "react";
import "../css/resultitem.css";

const ResultItem = ({ result }) => {
  return (
    <>
      <div className="result uprn">{result.uprn} </div>
      <div className="result address">{result.full_address} </div>
      <div className="result x-coord">{result.x_coordinate} </div>
      <div className="result y-coord">{result.y_coordinate} </div>
      <div className="result lat">{result.latitude} </div>
      <div className="result lon">{result.longitude} </div>
    </>
  );
};

export default ResultItem;
