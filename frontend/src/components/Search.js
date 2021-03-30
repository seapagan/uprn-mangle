import React, { useState } from "react";

import "../css/search.css";
import Loading from "./Loading";
import SearchBox from "./SearchBox";
import SearchResults from "./SearchResults";

const Search = () => {
  const [searchString, setSearchString] = useState("");

  return (
    <div className="search-container">
      <SearchBox setSearchString={setSearchString} />
      {searchString ? (
        <SearchResults searchString={searchString} />
      ) : (
        <Loading />
      )}
    </div>
  );
};

export default Search;
