# UPRN Search Tool

THIS README IS CURRENTLY A STUB, WILL BE UPDATED PROPERLY SHORTLY.

This is a (work in progress) tool to take the Ordnance Survey 'Address Base
Premium' data and mangle it into a more usable form. This is then loaded into a
database and provided as a Backend API. There is then a Frontend web app which
will allow searching of this data - eg addresses, and return the UPRN along with
links for Google maps and OpenStreetMap.

- Backend and mangle scripts written in Django (Python)
- Basic Frontend written in React

## Update 23rd November 2021

The Backend and Frontend are going through rewrites and tidy right now, __they
are not really usable__. Also needed is to optimize the management command to
mangle and import the csv files, it is massively memory hungry - using the
entire Scotland dataset as an example, it will crash on less than 12GB (Physical
& Swap) usable memory. This is a priority to fix, likely at the expense of
further increasing the time take to process the files.

The installation process documentation below needs to be updated to the new
changes involving reading settings from the `.env` file.

## Installation

On your local machine, you need a working copy of [Python][python] and
[Node.js][nodejs]. I recommend you also set up a local VirtualEnv specific to
this application. If you are using [Pyenv][pyenv] (highly recommended) you can
use it's inbuilt features to do this.

You will also need a PostgreSQL database set up, with the `abuser` user and
`addressbase` database, with the correct settings input to the
[settings.py](backend/backend/settings.py) (shortly these values will be set in
an `.env` file)

1. Clone or download the repository to your local machine
2. UPRN Data
   1. `To be updated`
3. Backend :
   1. In a terminal, change to the **backend** directory and run
      `pip install -r ../Requirements.txt`. This will install all the required
      dependencies.
   2. In the same terminal and still in the **backend** directory, run
      `python manage.py migrate`
   3. Finally run `python manage.py runserver`
4. Frontend :
   1. In a terminal, change to the **frontend** directory and run `yarn` or
      (`npm install` if you prefer. I will use Yarn throughout, you can
      substitute with NPM if that is your preference). This will install all the
      needed React.JS dependencies.
   2. Once complete, run `yarn start` to run the frontend.

Both the above scripts must be kept running at all times.

[python]: https://www.python.org/
[nodejs]: https://nodejs.org/
[pyenv]: https://github.com/pyenv/pyenv/
