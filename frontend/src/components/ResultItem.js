import React from "react";

import { FaMap } from "react-icons/fa";
import { SiGooglemaps } from "react-icons/si";

import "../css/resultitem.css";
import MapLink from "./MapLink";

const ResultItem = ({ result }) => {
  const GoogleURL = `https://www.google.com/maps/dir/?api=1&destination=${result.latitude},${result.longitude}`;
  const OSMapsURL = `https://osmaps.ordnancesurvey.co.uk/${result.latitude},${result.longitude},15/pin`;

  return (
    <div className="result-container">
      <div className="result uprn">{result.uprn}</div>
      <div className="result address">{result.full_address}</div>
      <div className="result x-coord">{result.x_coordinate}</div>
      <div className="result y-coord">{result.y_coordinate}</div>
      <div className="result lat">{result.latitude}</div>
      <div className="result lon">{result.longitude}</div>
      <div className="result link google">
        <MapLink Link={GoogleURL} Icon={SiGooglemaps} />
      </div>
      <div className="result link openstreet">
        <MapLink Link={OSMapsURL} Icon={FaMap} />
      </div>
    </div>
  );
};

export default ResultItem;
