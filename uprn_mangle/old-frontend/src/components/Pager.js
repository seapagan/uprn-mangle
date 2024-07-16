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
  const totalPages = Math.ceil(searchResults.count / 20) || 0;

  const getPageLink = count => {
    return `${baseURL}search/?q=${encodeURI(searchString)}&page=${count}`;
  };

  const getPathname = url => {
    const fullPath = new URL(url);

    return fullPath.pathname + fullPath.search;
  };

  const isCurrentPage = page => {
    return getCurrentPage() === page;
  };

  const getCurrentPage = () => {
    const fullURL = new URL("http://localhost" + searchURL);
    const searchParams = fullURL.searchParams;

    return parseInt(searchParams.get("page")) || 1;
  };

  const getPageArray = (howMany = 12) => {
    let startValue = 1;

    // never want more pages than we actually have...
    if (totalPages < howMany) howMany = totalPages;

    if (totalPages > howMany && getCurrentPage() > howMany / 2) {
      // we only want to return a subset of the pages
      startValue = getCurrentPage() - howMany / 2;
      if (getCurrentPage() >= totalPages - howMany / 2) {
        startValue = totalPages - howMany + 1;
      }
    }

    return Array.from({ length: howMany }, (x, index) => index + startValue);
  };

  // no pager needed for a single page of results...
  if (totalPages < 2) return null;

  // otherwise return the pager...
  return (
    <div className="pager-container">
      <button // 'First'
        disabled={!searchResults.previous ? true : false}
        className="btn btn-nav"
        onClick={() => setSearchURL(getPageLink(1))}>
        &lt;&lt; First
      </button>
      <button // 'Previous'
        disabled={!searchResults.previous ? true : false}
        className="btn btn-nav"
        onClick={() => setSearchURL(getPathname(searchResults.previous))}>
        &lt; Previous
      </button>
      <div className="pager-links">
        {getPageArray(12).map(page => (
          <button
            key={page}
            disabled={isCurrentPage(page)}
            className="btn pager-link"
            onClick={() => setSearchURL(getPageLink(page))}>
            {page}
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
