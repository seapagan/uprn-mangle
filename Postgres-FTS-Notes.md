# Notes on speeding up Postgresql search of the database

## this is very slow, approx 20 to 25 sec

- SELECT * from "addressbase" WHERE to_tsvector("FULL_ADDRESS") @@
  to_tsquery('blackadder');

## prepare the table with extra col and index

- ALTER table addressbase add column tsv tsvector;
- CREATE index tsv_idx on addressbase using gin(tsv);

## this will need updated to also cover and weigh the UPRN field

- UPDATE addressbase SET tsv = to_tsvector("FULL_ADDRESS");

## now test .... much faster, less than 10ms

- SELECT * from "addressbase", plainto_tsquery('blackadder') AS q WHERE (tsv @@q);

## next 2 are around the 3ms mark

- SELECT * from "addressbase", plainto_tsquery('blackadder west') AS q WHERE
  (tsv @@ q);
- SELECT * from "addressbase", plainto_tsquery('blackadder west') AS q WHERE
  (tsv @@ q) ORDER BY "UPRN";
