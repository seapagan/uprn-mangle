# UPRN Search Tool <!-- omit in toc -->

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CodeQL](https://github.com/seapagan/uprn-mangle/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/seapagan/uprn-mangle/actions/workflows/codeql-analysis.yml)
[![Dependency Review](https://github.com/seapagan/uprn-mangle/actions/workflows/dependency-review.yml/badge.svg)](https://github.com/seapagan/uprn-mangle/actions/workflows/dependency-review.yml)

THIS README IS IN THE PROCESS OF BEING UPDATED.

<!-- TOC start -->
- [Update 28th May 2024](#update-28th-may-2024)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [UPRN Data](#uprn-data)
- [Setup and run the Backend](#setup-and-run-the-backend)
- [Setup and run the Frontend](#setup-and-run-the-frontend)
- [Contributing to this project](#contributing-to-this-project)
- [License](#license)
<!-- TOC end -->

This project is a (work in progress) tool to take the Ordnance Survey '[Address
Base Premium][abp]' data and mangle it into a more usable form.

The data is then loaded into a database and provided as an API (Using Django).
Finally, a Frontend web app (written in React JS) will allow searching this data
by address and return the UPRN and links for Google maps and OpenStreetMap.

- Backend and mangle scripts in [Django][django] (Python)
- Basic Frontend in [React][react] (JavaScript)

## Update 28th May 2024

The entire project is going through a major rewrite. The original project was
started in 2022 and was a bit of a mess. I have learned a lot since then and
can improve the codebase significantly.

All work is being done in a new branch `develop` and will be merged back to
`main` when ready. Release `0.1.0` on GitHub is the last version of the original
legacy project if anyone is interested.

For a start, the UPRN import process was VERY memory intensie and slow. It took
over 12-15Gb of memory and many hours to import the full Scotland data. I
have now reduced this to around 2Gb, though I still need to check the timing
changes - it is still pretty slow but that is alot of data.

Dependency management and virtual-environment control is now taken care of by
`Poetry` which is a much better fit for the project. I have also added
`pre-commit` hooks to ensure code quality and formatting. The latter two are now
handled completely by `Ruff`, while `Mypy` is used for type checking.

I have also replaced the original `Django` and `Django Rest Framework` with
`FastAPI` and `SQLAlchemy 2`. This is a much better fit for the project.
Database access is Async, and the pagination is blindingly fast.

The Frontend still needs work. It will still be in `React` but I'll update to
the latest version and move away from `CRA` to a faster `Vite`-based setup.

Note that all the documentation below is for the original project and will be
updated once the new version is ready to merge.

## Installation

On your local machine, you need a working copy of [Python][python] and
[Nodejs][nodejs]. I recommend you also set up a local VirtualEnv specific to
this application. For example, if you use [Pyenv][pyenv] (highly
recommended), you can use its inbuilt VirtualEnv feature. Then, Clone or
download the repository to your local machine and switch to this new directory.

## Database Setup

You will also need a PostgreSQL database set up, with a user, password, and
dedicated database, with the correct settings input to the `.env` file. The user
should have full access to the specified database; It is good practice to create
a specific Postgresql user that only has access to this database.

You can copy then rename the [.env.example](backend/.env.example) file to `.env`
and add your database connection settings.

```ini
# set up Database Users. We will be using Postgresql and this should already
# exist with the correct user and password
UPRN_DB_USER='mickey'
UPRN_DB_PASSWORD='mouse'
# actual database name for the UPRN data...
UPRN_DB_NAME='addressbase_db'
UPRN_DB_HOST='localhost'
UPRN_DB_PORT='5432'
# name of the table in the database that contains the UPRN data...
UPRN_DB_TABLE='addressbase'
```

## UPRN Data

The data used for this project comes from the `AddressBase Premium` ( noted as
`ABP` from now on) by [Ordnance Survey][os]. APB is a commercial product, but
you can apply for a **Data Exploration License** [here][osdel]. The DEL allows
you to test and use the data in a limited way.

I will assume you have a copy of ABP in **CSV** format for this App. Copy all
the individual CSV files into the `backend/data/raw-csv/` folder.

The data provided by Ordnance Survey is a bit of a mess; that was the original
inspiration for this project - to merge/prune/tidy them into a usable format for
development.

We also need several other data files that are provided for free by OS on their
[OpenData][opendata] pages :

  1. We need the '**BLPU UPRN Street USRN 11**' data from the `OS Open Linked
     Identifiers` dataset. Download this, unzip and place the CSV file in the
     `backend/data/cross-ref-csv/` folder.
  2. We need the **header files** for the ABP data; this allows us to parse the
     data automatically. The project already contains the latest header files as
     of June 2022, but if any changes cause the scripts to fail, you can
     download the latest from OS [here][headers]. Download this file and replace
     all the existing CVS files in the `backend/data/header-files/` folder with
     those  in the zip file
  3. Finally, run the following command to process the raw data and add it to
     the database: `python manage.py import_uprn`

Part 3 above can take a good long time and memory. I recommend you close any
applications you are not using and reboot your system before starting. If you
are developing remotely using VSCode Remote SSH or similar, close VSCode and run
from a plain terminal.

## Setup and run the Backend

   1. Change to the **backend** directory in your terminal and run `pip install
      -r requirements.txt`. This command installs all the required dependencies.
   2. Generate a new secret key, and add it to the `.env` file above. Go to
      <https://djecrety.ir/> to generate a good one.
   3. In the same terminal and still in the **backend** directory, run
      `python manage.py migrate`
   4. Finally, run `python manage.py runserver`

The Back-end API will now be available at `http://localhost:8000/api/v1/`

## Setup and run the Frontend

   1. In a terminal, change to the **frontend** directory and run `yarn` or
      (`npm install` if you prefer. I will use Yarn throughout, you can
      substitute with NPM if that is your preference). This command installs all
      the needed React.JS dependencies.
   2. Once complete, run `yarn start` to run the frontend.

You can now access the Front-end at `http://localhost:3000`

Running the Backend/Frontend from your terminal is good enough for development,
but use standard practices to run and harden the system for any production use.

## Contributing to this project

While this is currently just a personal project and at a very early stage,
contributions, especially Bug Reports, are very welcome.

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

## License

This project is under the
[MIT](https://choosealicense.com/licenses/mit/) license.

```pre
Copyright (c) 2022-2024 Grant Ramsay

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

[python]: https://www.python.org/
[nodejs]: https://nodejs.org/
[pyenv]: https://github.com/pyenv/pyenv/
[django]: https://www.djangoproject.com/
[react]: https://reactjs.org/

[os]: https://www.ordnancesurvey.co.uk/
[osdel]: https://www.ordnancesurvey.co.uk/business-government/licensing-agreements/data-exploration
[opendata]: https://osdatahub.os.uk/downloads/open
[headers]: https://www.ordnancesurvey.co.uk/documents/product-support/support/addressbase-premium-header-files.zip
[abp]: https://www.ordnancesurvey.co.uk/business-government/products/addressbase-premium
