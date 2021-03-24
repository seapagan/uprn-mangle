import "react-app-polyfill/ie9"; // support IE 9 and above
import "react-app-polyfill/stable"; // extra polyfills
import React from "react";
import ReactDOM from "react-dom";

import App from "./components/App";

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);
