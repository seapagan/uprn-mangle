import React from "react";

import { FaMap } from "react-icons/fa";
import { SiGooglemaps } from "react-icons/si";

import MapLink from "./MapLink";

import "../css/resultitem.css";

const ResultItem = ({ result }) => {
  const GoogleURL = `https://www.google.com/maps/dir/?api=1&destination=${result.latitude},${result.longitude}`;
  const OSMapsURL = `https://osmaps.ordnancesurvey.co.uk/${result.latitude},${result.longitude},15/pin`;

  return (
    <div className="result-container">
      <div className="result-details">
        <div className="result uprn">{result.uprn}</div>
        <div className="result address">
          <div className="result address-main">{result.full_address}</div>
          <div className="result address-extra">Extra Stuff</div>
        </div>

        <div className="result link">
          <MapLink Link={GoogleURL} Icon={SiGooglemaps} />
        </div>
        <div className="result link">
          <MapLink Link={OSMapsURL} Icon={FaMap} />
        </div>
      </div>
    </div>
  );
};

export default ResultItem;
