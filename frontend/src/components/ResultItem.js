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
      <div className="result-details">
        <div className="result uprn">{result.uprn}</div>
        <div className="result address">{result.full_address}</div>

        <div className="result link">
          <MapLink Link={GoogleURL} Icon={SiGooglemaps} />
        </div>
        <div className="result link">
          <MapLink Link={OSMapsURL} Icon={FaMap} />
        </div>
      </div>
      {/* <div className="result-extra">
        <div className="result-coords">
          <div className="result-extra-coords-title">X / Y Coords: </div>
          <div className="result-extra-coords-values">
            {result.x_coordinate},&nbsp;{result.y_coordinate}
          </div>
        </div>

        <div className="result-coords">
          <div className="result-extra-coords-title">Lat / Lon Coords: </div>
          <div className="result-extra-coords-values">
            {result.latitude},&nbsp;{result.longitude}
          </div>
        </div>
      </div> */}
    </div>
  );
};

export default ResultItem;
