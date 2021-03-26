# get script path
import os
from pathlib import Path
from inspect import getsourcefile

# get our running path, then create the data_path from this.
our_path = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))
# data_path = os.path.join(our_path, "data")
# data_path = str(Path(our_path).parents[2])
data_path = os.path.join(str(Path(our_path).parents[3]), "data")

# set some constants for the other paths.
RAW_DIR = os.path.join(data_path, "raw-csv")
MANGLED_DIR = os.path.join(data_path, "mangled-csv")
HEADER_DIR = os.path.join(data_path, "header-files")
CROSSREF_DIR = os.path.join(data_path, "cross-ref-csv")
OUTPUT_DIR = os.path.join(data_path, "output-csv")

# this name should never change
CROSSREF_NAME = "BLPU_UPRN_Street_USRN_11.csv"

OUTPUT_NAME = "processed-addressbase.csv"

# Database login stuff. These will eventually be put into ENV variables for
# security in a real situation.
# These already need to be setup in your Postgresql database.
DB_HOST = "localhost"
DB_NAME = "addressbase"
DB_USER = "abuser"
DB_PASSWORD = ".`)sA`=J|eyWd}8V~"
# this table will be created in the script and dropped first if exists.
DB_TABLE = "addressbase"
