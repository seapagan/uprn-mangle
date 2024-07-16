import { useState } from "react";

import Loading from "./Loading";
import SearchBox from "./SearchBox";
import SearchResults from "./SearchResults";

import "../css/search.css";

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
