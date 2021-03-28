import React, { useState, useEffect } from "react";

const SearchResults = ({ searchString }) => {
  // in here we will do the actual search, using the 'searchString' variable
  // passed into us.

  const baseURL = "/api/v1/";

  const [searchResults, setSearchResults] = useState({ results: [] });

  useEffect(() => {
    if (searchString) {
      const searchURL = baseURL + "search/?q=" + encodeURI(searchString);
      fetch(searchURL)
        .then(response => response.json())
        .then(data => setSearchResults(data));
    }
  }, [searchString]);

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
    </>
  );
};

export default SearchResults;
