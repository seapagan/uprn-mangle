import React from "react";

import "../css/pager.css";

const Pager = ({ baseURL, searchResults, searchString, setSearchURL }) => {
  const totalPages = Math.floor(searchResults.count / 20) + 1;
  console.log("Total Pages : ", totalPages);

  const getLastPageLink = count => {
    return `${baseURL}search/?page=${count}&q=${encodeURI(searchString)}`;
  };

  const getFirstPageLink = () => {
    return `${baseURL}search/?page=1&q=${encodeURI(searchString)}`;
  };

  const getPathname = url => {
    const fullPath = new URL(url);
    return fullPath.pathname + fullPath.search;
  };

  return (
    <div
      className={`pager-container ${
        !searchResults.count || totalPages < 2 ? "pager-hidden" : ""
      }`}>
      {/* <span> */}
      <button
        disabled={!searchResults.previous ? true : false}
        className="btn btn-nav"
        onClick={() => setSearchURL(getFirstPageLink())}>
        &lt;&lt; First
      </button>
      <button
        disabled={!searchResults.previous ? true : false}
        className="btn btn-nav"
        onClick={() => setSearchURL(getPathname(searchResults.previous))}>
        &lt; Previous
      </button>
      {/* </span> */}

      {/* <span> */}
      <button
        disabled={!searchResults.next ? true : false}
        className="btn btn-nav"
        onClick={() => setSearchURL(getPathname(searchResults.next))}>
        Next &gt;
      </button>
      <button
        disabled={!searchResults.next ? true : false}
        className="btn btn-nav"
        onClick={() => setSearchURL(getLastPageLink(totalPages))}>
        Last &gt;&gt;
      </button>
      {/* </span> */}
    </div>
  );
};

export default Pager;
