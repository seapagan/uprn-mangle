import "react-app-polyfill/ie9"; // support IE 9 and above
import "react-app-polyfill/stable"; // extra polyfills

import React from "react";

import { createRoot } from "react-dom/client";

import App from "./components/App";

const root = createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
