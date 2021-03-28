import React, { useState, useEffect } from "react";

import ResultItem from "./ResultItem";

const SearchResults = ({ searchString }) => {
  // in here we will do the actual search, using the 'searchString' variable
  // passed into us.

  const baseURL = "/api/v1/";

  const [searchResults, setSearchResults] = useState({ results: [] });
  const [searchURL, setSearchURL] = useState("");
  const [firstPage, setFirstPage] = useState("");
  const [lastPage, setLastPage] = useState("");

  useEffect(() => {
    if (searchString) {
      setSearchURL(baseURL + "search/?q=" + encodeURI(searchString));
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
      {searchResults.results.map((result, index) => (
        <ResultItem key={index} result={result} index={index} />
      ))}
      {searchResults.previous ? (
        <span>
          <button>&lt;&lt; First</button>
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
