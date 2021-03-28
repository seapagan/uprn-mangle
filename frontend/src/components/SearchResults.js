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
  const [firstPageURL, setFirstPageURL] = useState("");
  const [lastPageURL, setLastPageURL] = useState("");

  useEffect(() => {
    if (searchString) {
      setSearchURL(`${baseURL}search/?q=${encodeURI(searchString)}`);
      setFirstPageURL(`${baseURL}search/?page=1&q=${encodeURI(searchString)}`);
    }
  }, [searchString]);

  useEffect(() => {
    if (searchURL) {
      fetch(searchURL)
        .then(response => response.json())
        .then(data => setSearchResults(data));
    }
  }, [searchURL]);

  const getPathname = url => {
    const fullPath = new URL(url);
    return fullPath.pathname + fullPath.search;
  };

  return (
    <>
      <div>Search Term is : {searchString}</div>
      <div>Number of Results : {searchResults.count}</div>
      {console.log(searchResults)}

      <div className="grid-container">
        <ResultHeader />
        {searchResults.results.map((result, index) => (
          <ResultItem key={index} result={result} />
        ))}
      </div>

      {console.log("SearchURL: ", searchURL)}
      {searchResults.previous ? (
        <span>
          <button onClick={() => setSearchURL(firstPageURL)}>
            &lt;&lt; First
          </button>
          <button
            onClick={() => setSearchURL(getPathname(searchResults.previous))}>
            &lt; Previous
          </button>
        </span>
      ) : (
        ""
      )}
      {searchResults.next ? (
        <span>
          <button onClick={() => setSearchURL(getPathname(searchResults.next))}>
            Next &gt;
          </button>
          <button>Last &gt;&gt;</button>
        </span>
      ) : (
        ""
      )}
    </>
  );
};

export default SearchResults;
