# UPRN Mangle TODO List

## Backend

- Check out [xorbits](https://github.com/xorbitsai/xorbits) which may be a
  better solution than `Dask`.
- Look at the utility of changing the generation script to use Typer instead of
  a plain Python script.
- Drop any demolished buildings in the combine stage? It may be useful to have
  these though, and we can always flag them as demolished in the web app.
- Fix the missing cursor on script abort.
- Add ability to skip a phase if relevant data is detected, either quietly or by
  asking (default).
- Add authentication to the API (probably token based).
- Add another search parameter to return the JSON results sorted on the passed
  column name. Default to UPRN as it is now if none specified.
- Add an option/script to dump the database into a backup, and to restore from
  a backup.

## Frontend

- Write the README File.
- Clickable titles to sort results
- add the street info as a smaller text below the address, also show the links
  to maps in this for smaller screen sizes
- complete the styling
- Add a footer
