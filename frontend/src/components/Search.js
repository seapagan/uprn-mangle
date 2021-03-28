import React, { useState } from "react";

import "../css/search.css";
import SearchBox from "./SearchBox";
import SearchResults from "./SearchResults";

const Search = () => {
  const [searchString, setSearchString] = useState("");

  return (
    <div className="search-container">
      <SearchBox setSearchString={setSearchString} />
      <SearchResults searchString={searchString} />
    </div>
  );
};

export default Search;
