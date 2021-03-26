# TODO List

- Drop any demolished buildings in the combine stage? It may be useful to have
  these though, and we can always flag them as demolished in the web app.
- Fix the missing cursor on script abort
- Put the section (phase) header into a reusable function, use [list] of strings
  as input
- Move the import script completely into a Django manage command
- Rewrite the database upload functionality in the script to use native Django
  ORM
- Add ability to skip a phase, either quietly or asking (default)
- Add the tsvector data and index once imported. When we use the Django ORM we
  can get this done automatically for each record.
- Put the constants, especially DB info into a .env file and use this instead of
  hard coding.
- Write the README for both backend and frontend.
