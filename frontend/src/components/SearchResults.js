import React, { useState, useEffect } from "react";

import "../css/searchresults.css";
import Pager from "./Pager";
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

  return (
    <>
      {console.log(searchResults)}

      <div className="grid-container">
        <ResultHeader />
        {searchResults.results.map((result, index) => (
          <ResultItem key={index} result={result} />
        ))}
      </div>
      <Pager
        baseURL={baseURL}
        searchResults={searchResults}
        searchString={searchString}
        setSearchURL={setSearchURL}
      />
    </>
  );
};

export default SearchResults;
