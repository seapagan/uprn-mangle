import React, { useState } from "react";

import "../css/searchbox.css";

const SearchBox = ({ setSearchString }) => {
  const [searchTerm, setSearchTerm] = useState("");

  const search = e => {
    e.preventDefault();
    if (!searchTerm) return;
    setSearchString(searchTerm);
  };

  const clearSearchBox = e => {
    e.preventDefault();
    setSearchTerm("");
    setSearchString("");
  };

  return (
    <div>
      <form className="search-box-wrapper">
        <input
          className="input"
          type="text"
          placeholder="Search the Address Database"
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
        />

        <button className="btn btn-search" type="submit" onClick={search}>
          Search
        </button>
        <button className="btn btn-search" onClick={clearSearchBox}>
          Clear
        </button>
      </form>
    </div>
  );
};

export default SearchBox;
