# UPRN Search Tool <!-- omit in toc -->

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CodeQL](https://github.com/seapagan/uprn-mangle/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/seapagan/uprn-mangle/actions/workflows/codeql-analysis.yml)
[![Dependency Review](https://github.com/seapagan/uprn-mangle/actions/workflows/dependency-review.yml/badge.svg)](https://github.com/seapagan/uprn-mangle/actions/workflows/dependency-review.yml)

<!-- vim-markdown-toc GFM -->

- [Update 17th November 2024](#update-17th-november-2024)
- [Update 16th July 2024](#update-16th-july-2024)
- [Setup](#setup)
- [Installation](#installation)
  - [UPRN Data](#uprn-data)
  - [Python](#python)
  - [React](#react)
- [Contributing to this project](#contributing-to-this-project)
- [License](#license)

<!-- vim-markdown-toc -->

This project is a (work in progress) tool to take the Ordnance Survey '[Address
Base Premium][abp]' data and mangle it into a more usable form.

The data is then loaded into a database and provided as an API (Using FastAPI).
Finally, a Frontend web app (written in React JS) will allow searching this data
by address and return the UPRN and links for Google maps and OpenStreetMap.

- Backend and mangle scripts in [FastAPI][fastapi] (Python)
- Basic Frontend in [React][react] (JavaScript)

## Update 17th November 2024

Migrated from `Poetry` to [uv](https://docs.astral.sh/uv/) for dependency and
project management. I have been using this for a while now and it is a much
faster and feature-rich tool than `Poetry`.

## Update 16th July 2024

The entire project has just had a major rewrite. The original project was
started in 2022 and was a bit of a mess. I have learned a lot since then and
can improve the codebase significantly.

For a start, the UPRN import process was VERY memory intensive and slow. It took
over 12-15Gb of memory and many hours to import the full Scotland data. I have
now reduced this to around 2Gb, though I still need to check the timing changes,
it is still pretty slow but that is a lot of data.

Dependency management and virtual-environment control is now taken care of by
`Poetry` which is a much better fit for the project. I have also added
`pre-commit` hooks to ensure code quality and formatting. The latter two are now
handled completely by `Ruff`, while `Mypy` is used for type checking.

I have also replaced the original `Django` and `Django Rest Framework` with
`FastAPI` and `SQLAlchemy 2`. This is a much better fit for the project.
Database access is Async, and the pagination is blindingly fast.

The Frontend has been updated to use `Vite` instead of `Create React App`. This
is a much faster and more modern build tool.

## Setup

You will need a PostgreSQL database set up, with a user, password, and
dedicated database. The user should have full access to the specified database;
It is good practice to create a specific Postgresql user that only has access
to this database.

All setup for this project is done in the `config.toml` file in the root folder.

An `example-config.toml` file is provided. Copy this to `config.toml` and edit
the values to match your setup. Make sure to put the correct database details
in.

You can change the `api_prefix` to place the API at a different URL. The default
is `/api/v2/` so the API will be available at `http://localhost:8000/api/v2/`.

> [!NOTE]
> The frontend is currently hard-coded to look for the API at the above URL.
> If you change this, you will need to update the frontend code.

```toml
[uprn_mangle]
api_base_url = "http://localhost"
api_port = 8000
api_prefix = "/api/v2"

db_user = "addressbase"
db_password = "mysecurepassword"
db_name = "addressbase"
db_host = "localhost"
db_port = "5432"
db_table = "addressbase"
```

## Installation

On your local machine, you need a working copy of [Python][python] and
[Nodejs][nodejs]. It is recommended to have [uv](https://docs.astral.sh/uv/)
installed for `project`/`venv` and `Python` version management. If not, I
recommend you use [Pyenv][pyenv] to manage your Python versions.

Use `Yarn` or `npm` for the JavaScript dependencies (only needed for the
front-end).

### UPRN Data

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

### Python

From the root folder, run the following commands:

```terminal
uv sync
source .venv/bin/activate
```

> [!TIP]
>
> It is recomended to use `uv` to manage the project and virtual environment,
> but you can still use plain `pip` and `venv` if you prefer.
>
> Create a new virtual environment, then install the dependencies with:
>
> ```terminal
> pip install -r requirements.txt
> source .venv/bin/activate
> ```
>
> This will install the production dependencies. If you want to install the dev
> dependencies, use the `requirements-dev.txt` file instead. Both these files
> are auto-generated by the `pre-commit` hooks.

This will install all the required Python dependencies and switch to the virtual
environment.

Now, run the following command to set up the database and import the UPRN data:

```bash
python uprn_mangle/backend/import_uprn.py
```

This last part can take a good long time and memory to complete. It is recommended
to run this on a machine with a good amount of memory and a fast CPU.

Finally, if this completes successfully, you can start the backend server:

```bash
python uprn_mangle/backend/api/main.py
```

### React

Change to the `uprn_mangle/frontend` folder and run the following commands:

```bash
yarn install
yarn dev
```

You can also use `npm` if you prefer. This will install all the required
JavaScript dependencies and start the frontend server. You should leave this
running too.

You can now access the Front-end at `http://localhost:5173`

> [!IMPORTANT]
> The above is only useful for development and testing purposes. For production
> use, you should use a proper web server and reverse proxy setup.

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
[fastapi]: https://fastapi.tiangolo.com/
[react]: https://reactjs.org/

[os]: https://www.ordnancesurvey.co.uk/
[osdel]: https://www.ordnancesurvey.co.uk/business-government/licensing-agreements/data-exploration
[opendata]: https://osdatahub.os.uk/downloads/open
[headers]: https://www.ordnancesurvey.co.uk/documents/product-support/support/addressbase-premium-header-files.zip
[abp]: https://www.ordnancesurvey.co.uk/business-government/products/addressbase-premium
