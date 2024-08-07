import "../css/pager.css";

const Pager = ({ searchResults, setSearchURL }) => {
  const totalPages = searchResults.pages;
  const currentPage = searchResults.page;

  const links = searchResults.links || {};

  const isCurrentPage = (page) => {
    return currentPage === page;
  };

  const getPageArray = (howMany = 12) => {
    let startValue = 1;

    // never want more pages than we actually have...
    if (totalPages < howMany) howMany = totalPages;

    if (totalPages > howMany && currentPage > howMany / 2) {
      // we only want to return a subset of the pages
      startValue = currentPage - howMany / 2;
      if (currentPage >= totalPages - howMany / 2) {
        startValue = totalPages - howMany + 1;
      }
    }

    return Array.from({ length: howMany }, (_, index) => index + startValue);
  };

  const updatePageQueryParam = (url, newPage) => {
    const urlObj = new URL(url);
    urlObj.searchParams.set("page", newPage);

    return urlObj.toString();
  };

  // no pager needed for a single page of results...
  if (totalPages < 2) return null;

  // otherwise return the pager...
  return (
    <div className="pager-container">
      <button // 'First'
        disabled={currentPage == 1 ? true : false}
        className="btn btn-nav"
        onClick={() => setSearchURL(links.first)}
      >
        &lt;&lt; First
      </button>
      <button // 'Previous'
        disabled={!links.prev ? true : false}
        className="btn btn-nav"
        onClick={() => setSearchURL(links.prev)}
      >
        &lt; Previous
      </button>
      <div className="pager-links">
        {getPageArray(12).map((page) => (
          <button
            key={page}
            disabled={isCurrentPage(page)}
            className="btn pager-link"
            onClick={() => setSearchURL(updatePageQueryParam(links.self, page))}
          >
            {page}
          </button>
        ))}
      </div>

      <button // 'Next'
        disabled={!links.next ? true : false}
        className="btn btn-nav"
        onClick={() => {
          setSearchURL(links.next);
        }}
      >
        Next &gt;
      </button>
      <button // 'Last'
        disabled={currentPage == totalPages ? true : false}
        className="btn btn-nav"
        onClick={() => setSearchURL(links.last)}
      >
        Last &gt;&gt;
      </button>
    </div>
  );
};

export default Pager;
