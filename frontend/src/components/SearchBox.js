import React, { useState } from "react";

const SearchBox = ({ setSearchString }) => {
  const [searchTerm, setSearchTerm] = useState("");

  const search = e => {
    e.preventDefault();
    if (!searchTerm) return;
    setSearchString(searchTerm);
    console.log(searchTerm);
  };

  const clearSearchBox = e => {
    e.preventDefault();
    setSearchTerm("");
    setSearchString("");
  };

  return (
    <div>
      <form>
        <input
          type="text"
          placeholder="Search the Address Database"
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
        />

        <button type="submit" onClick={search}>
          Search
        </button>
        <button onClick={clearSearchBox}>Clear</button>
      </form>
    </div>
  );
};

export default SearchBox;
