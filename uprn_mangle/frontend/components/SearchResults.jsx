import { useEffect, useState } from "react";

import Pager from "./Pager";
import ResultHeader from "./ResultHeader";
import ResultItem from "./ResultItem";

import "../css/searchresults.css";

const SearchResults = ({ searchString }) => {
  // in here we will do the actual search, using the 'searchString' variable
  // passed into us.

  const baseURL = "http://127.0.0.1:8000/api/v2/";

  const [searchResults, setSearchResults] = useState({ addresses: [] });
  const [searchURL, setSearchURL] = useState("");

  useEffect(() => {
    if (searchString) {
      setSearchURL(`${baseURL}search?q=${encodeURI(searchString)}`);
    }
  }, [searchString]);

  useEffect(() => {
    if (searchURL) {
      fetch(searchURL)
        .then((response) => response.json())
        .then((data) => setSearchResults(data))
        .catch((error) => console.error("Error fetching data:", error));
    }
  }, [searchURL]);

  return (
    <div>
      {<Pager searchResults={searchResults} setSearchURL={setSearchURL} />}
      <div className="search-results-container">
        <ResultHeader />
        {searchResults.addresses.map((result, index) => (
          <ResultItem key={index} result={result} />
        ))}
      </div>
      {<Pager searchResults={searchResults} setSearchURL={setSearchURL} />}
    </div>
  );
};

export default SearchResults;
