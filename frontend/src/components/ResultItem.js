import React from "react";

const ResultItem = ({ result }) => {
  return (
    <div>
      <span>{result.uprn} </span>
      <span>{result.full_address} </span>
      <span>{result.x_coordinate} </span>
      <span>{result.y_coordinate} </span>
      <span>{result.latitude} </span>
      <span>{result.longitude} </span>
    </div>
  );
};

export default ResultItem;
