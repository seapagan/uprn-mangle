# UPRN Search Tool <!-- omit in toc -->

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
THIS README IS IN THE PROCESS OF BEING UPDATED.

<!-- TOC start -->
- [Update 8th June 2022](#update-8th-june-2022)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [UPRN Data](#uprn-data)
- [Setup and run the Backend](#setup-and-run-the-backend)
- [Setup and run the Frontend](#setup-and-run-the-frontend)
- [Contributing to this project](#contributing-to-this-project)
- [License](#license)
<!-- TOC end -->

This is a (work in progress) tool to take the Ordnance Survey '[Address Base
Premium][abp]' data and mangle it into a more usable form.

The data is then loaded into a database and provided as an API (Using Django).
There is then a Frontend web app (written in React JS) which will allow
searching of this data - eg addresses, and return the UPRN along with links for
Google maps and OpenStreetMap.

- Backend and mangle scripts written in [Django][django] (Python)
- Basic Frontend written in [React][react] (JavaScript)

## Update 8th June 2022

The Backend and Frontend are going through a rewrite and tidy right now, but are
still usable.

I have updated to use the latest Django 4 and React 18, while improving the
configuration of development tooling such as Formatters and Linters for both
Python and React.

I am working to optimize the management command to mangle and import the csv
files, it is massively memory hungry - using the entire Scotland dataset as an
example, it will crash on less than 12GB (Physical + Swap) usable memory. This
is a priority to fix, likely at the expense of further increasing the time take
to process the files.

## Installation

On your local machine, you need a working copy of [Python][python] and
[Node.js][nodejs]. I recommend you also set up a local VirtualEnv specific to
this application. If you are using [Pyenv][pyenv] (highly recommended) you can
use it's inbuilt features to do this. Then, Clone or download the repository to
your local machine and switch to this new directory.

## Database Setup

You will also need a PostgreSQL database set up, with the `abuser` user and
`addressbase` database, with the correct settings input to the `.env` file. You
can copy then rename the [.env.example](backend/.env.example) file and add your
database connection settings.

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

`To be added.`

## Setup and run the Backend

   1. In a terminal, change to the __backend__ directory and run
      `pip install -r requirements.txt`. This will install all the required
      dependencies.
   2. Generate a new secret key, and add it to the `.env` file above. Go to
      <https://djecrety.ir/> to generate a good one.
   3. In the same terminal and still in the __backend__ directory, run
      `python manage.py migrate`
   4. Finally run `python manage.py runserver`

The backend API will now be available at `http://localhost:8000/api/v1/`

## Setup and run the Frontend

   1. In a terminal, change to the __frontend__ directory and run `yarn` or
      (`npm install` if you prefer. I will use Yarn throughout, you can
      substitute with NPM if that is your preference). This will install all the
      needed React.JS dependencies.
   2. Once complete, run `yarn start` to run the frontend.

The Frontend can now be accessed at `http://localhost:3000`

Running the Backend/Frontend directly is good enough for development but
obviously use standard practices to run and harden the system for any production
use.

## Contributing to this project

While this is currently just a personal project and at a very early stage,
contributions and especially Bug Reports are very welcome.

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## License

This project has been placed under the
[MIT](https://choosealicense.com/licenses/mit/) license.

```pre
Copyright (c) 2022 Grant Ramsay

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

[abp]:
    https://www.ordnancesurvey.co.uk/business-government/products/addressbase-premium
