import React, { useEffect, useState } from "react";

// import Pager from "./Pager";
import ResultHeader from "./ResultHeader";
import ResultItem from "./ResultItem";

import "../css/searchresults.css";

const SearchResults = ({ searchString }) => {
  // in here we will do the actual search, using the 'searchString' variable
  // passed into us.

  const baseURL = "/api/v2/";

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
        .then((response) => response.json())
        .then((data) => setSearchResults(data));
    }
  }, [searchURL]);

  return (
    <div>
      {/* <Pager
        baseURL={baseURL}
        searchResults={searchResults}
        searchString={searchString}
        searchURL={searchURL}
        setSearchURL={setSearchURL}
      /> */}
      <div className="search-results-container">
        <ResultHeader />
        {searchResults && console.log(searchResults)}
        {searchResults.addresses.map((result, index) => (
          <ResultItem key={index} result={result} />
        ))}
      </div>
      {/* <Pager
        baseURL={baseURL}
        searchResults={searchResults}
        searchString={searchString}
        searchURL={searchURL}
        setSearchURL={setSearchURL}
      /> */}
    </div>
  );
};

export default SearchResults;
