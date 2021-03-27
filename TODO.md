# UPRN Mangle TODO List

## Backend

- Drop any demolished buildings in the combine stage? It may be useful to have
  these though, and we can always flag them as demolished in the web app.
- Fix the missing cursor on script abort.
- <del>Put the section (phase) header into a reusable function, use [list] of
  strings as input.</del>
- <del>Move the import script completely into a Django manage command.<del>
- Rewrite the database upload functionality in the script to use native Django
  ORM.
- Add ability to skip a phase if relevant data is detected, either quietly or by
  asking (default).
- Add the tsvector data and index once imported. When we use the Django ORM we
  can get this done automatically for each record.
- Put the constants, especially DB info into a .env file and use this instead of
  hard coding.
- Write the README File.
- Add extra Django commands to recreate the tsvector, indexes etc.
- Add authentication to the API (probably token based).
- Filter out results where the postcode is empty, this will remove a lot of the
  useless stuff. Ideally, this should be done on the raw data import.

## Frontend

- Write the README File.
