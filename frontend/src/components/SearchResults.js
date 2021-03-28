import React, { useState, useEffect } from "react";

const SearchResults = ({ searchString }) => {
  // in here we will do the actual search, using the 'searchString' variable
  // passed into us.

  const baseURL = "/api/v1/";

  const [searchResults, setSearchResults] = useState({ results: [] });
  const [searchURL, setSearchURL] = useState("");

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
        <div key={index}>
          {index + 1} : {result.uprn}, {result.full_address},
          {result.x_coordinate}, {result.y_coordinate}, {result.latitude},
          {result.longitude}
        </div>
      ))}
      {searchResults.previous ? (
        <button
          onClick={() => setSearchURL(getPathname(searchResults.previous))}>
          Previous
        </button>
      ) : (
        ""
      )}
      {searchResults.next ? (
        <button onClick={() => setSearchURL(getPathname(searchResults.next))}>
          Next
        </button>
      ) : (
        ""
      )}
    </>
  );
};

export default SearchResults;
