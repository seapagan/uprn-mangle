import React from "react";

import "../css/pager.css";

const Pager = ({
  baseURL,
  searchResults,
  searchString,
  searchURL,
  setSearchURL,
}) => {
  // calc the total pages for this result, ser to zero if no results
  const totalPages = Math.floor(searchResults.count / 20) + 1 || 0;

  const getPageLink = count => {
    return `${baseURL}search/?q=${encodeURI(searchString)}&page=${count}`;
  };

  const getFirstPageLink = () => {
    return `${baseURL}search/?page=1&q=${encodeURI(searchString)}`;
  };

  const getPathname = url => {
    const fullPath = new URL(url);
    return fullPath.pathname + fullPath.search;
  };

  const isCurrentPage = page => {
    const fullURL = new URL("http://localhost" + searchURL);
    const searchParams = fullURL.searchParams;
    const thisPage = parseInt(searchParams.get("page")) || 1;
    return thisPage === page;
  };

  return (
    <div className={`pager-container ${totalPages < 2 ? "pager-hidden" : ""}`}>
      <button // 'First'
        disabled={!searchResults.previous ? true : false}
        className="btn btn-nav"
        onClick={() => setSearchURL(getFirstPageLink())}>
        &lt;&lt; First
      </button>
      <button // 'Previous'
        disabled={!searchResults.previous ? true : false}
        className="btn btn-nav"
        onClick={() => setSearchURL(getPathname(searchResults.previous))}>
        &lt; Previous
      </button>
      <div className="pager-links">
        {[...Array(totalPages)].map((e, page) => (
          <button
            key={page + 1}
            disabled={isCurrentPage(page + 1)}
            className="btn pager-link"
            onClick={() => setSearchURL(getPageLink(page + 1))}>
            {page + 1}
          </button>
        ))}
      </div>

      <button // 'Next'
        disabled={!searchResults.next ? true : false}
        className="btn btn-nav"
        onClick={() => setSearchURL(getPathname(searchResults.next))}>
        Next &gt;
      </button>
      <button // 'Last'
        disabled={!searchResults.next ? true : false}
        className="btn btn-nav"
        onClick={() => setSearchURL(getPageLink(totalPages))}>
        Last &gt;&gt;
      </button>
    </div>
  );
};

export default Pager;
