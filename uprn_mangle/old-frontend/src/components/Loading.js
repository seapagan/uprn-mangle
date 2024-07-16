import React from "react";

import { TailSpin } from "react-loader-spinner";

import "../css/loading.css";

const Loading = () => {
  return (
    <div className="loading">
      <TailSpin
        ariaLabel="loading-indicator"
        color="gray"
        height={50}
        width={50}
      />
      <p>Please enter an Address to begin your Search</p>
    </div>
  );
};

export default Loading;
