import React, { useState, useEffect } from "react";

import "../css/searchresults.css";
import ResultHeader from "./ResultHeader";
import ResultItem from "./ResultItem";

const SearchResults = ({ searchString }) => {
  // in here we will do the actual search, using the 'searchString' variable
  // passed into us.

  const baseURL = "/api/v1/";

  const [searchResults, setSearchResults] = useState({ results: [] });
  const [searchURL, setSearchURL] = useState("");

  useEffect(() => {
    if (searchString) {
      setSearchURL(`${baseURL}search/?q=${encodeURI(searchString)}`);
    }
  }, [searchString]);

  useEffect(() => {
    if (searchURL) {
      fetch(searchURL)
        .then(response => response.json())
        .then(data => setSearchResults(data));
    }
  }, [searchURL]);

  const getLastPageLink = count => {
    const numPages = Math.floor(count / 20) + 1;
    return `${baseURL}search/?page=${numPages}&q=${encodeURI(searchString)}`;
  };

  const getFirstPageLink = () => {
    return `${baseURL}search/?page=1&q=${encodeURI(searchString)}`;
  };

  const getPathname = url => {
    const fullPath = new URL(url);
    return fullPath.pathname + fullPath.search;
  };

  return (
    <>
      {console.log(searchResults)}

      <div className="grid-container">
        <ResultHeader />
        {searchResults.results.map((result, index) => (
          <ResultItem key={index} result={result} />
        ))}
      </div>

      {searchResults.previous ? (
        <span>
          <button
            className="btn btn-nav"
            onClick={() => setSearchURL(getFirstPageLink())}>
            &lt;&lt; First
          </button>
          <button
            className="btn btn-nav"
            onClick={() => setSearchURL(getPathname(searchResults.previous))}>
            &lt; Previous
          </button>
        </span>
      ) : (
        ""
      )}
      {searchResults.next ? (
        <span>
          <button
            className="btn btn-nav"
            onClick={() => setSearchURL(getPathname(searchResults.next))}>
            Next &gt;
          </button>
          <button
            className="btn btn-nav"
            onClick={() => setSearchURL(getLastPageLink(searchResults.count))}>
            Last &gt;&gt;
          </button>
        </span>
      ) : (
        ""
      )}
    </>
  );
};

export default SearchResults;
