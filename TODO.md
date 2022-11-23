# UPRN Mangle TODO List

## Backend

- Move from `Pandas` to `Dask` `DataFrames`, to help reading the very large
  datafiles, with Dask they can stay be used more from disk instead of memory.
- Drop any demolished buildings in the combine stage? It may be useful to have
  these though, and we can always flag them as demolished in the web app.
- Fix the missing cursor on script abort.
- ~~Put the section (phase) header into a reusable function, use [list] of
  strings as input.~~
- ~~Move the import script completely into a Django manage command.~~
- Rewrite the database upload functionality in the script to use native Django
  ORM.
- Add ability to skip a phase if relevant data is detected, either quietly or by
  asking (default).
- Add the tsvector data and index once imported. When we use the Django ORM we
  can get this done automatically for each record.
- ~~Put the constants, especially DB info into a .env file and use this instead of
  hard coding.~~
- Write the README File.
- Add extra Django commands to recreate the tsvector, indexes etc.
- Add authentication to the API (probably token based).
- Filter out results where the postcode is empty, this will remove a lot of the
  useless stuff. Ideally, this should be done on the raw data import.
- Remove duplicated UPRN lines.
- Add another search parameter to return the JSON results sorted on the passed
  column name. Default to UPRN as it is now if none specified.

## Frontend

- Write the README File.
- Clickable titles to sort results
- add the street info as a smaller text below the address, also show the links
  to maps in this for smaller screen sizes
- complete the styling
- make fully responsive **[ Basically Complete for existing code ]**
- ~~does this need to be fully Flexbox instead of Grid to improve the
  styling?~~
- Add a footer
- ~~modify Pager component. if more than (eg) 12 pages, only show a subset in
  the page links~~
