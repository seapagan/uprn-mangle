# get script path
import os
from inspect import getsourcefile

# our_path = os.path.abspath(os.path.dirname(__file__))
our_path = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))

# set some constants
RAW_DIR = os.path.join(our_path, "raw-csv")
MANGLED_DIR = os.path.join(our_path, "mangled-csv")
HEADER_DIR = os.path.join(our_path, "header-files")
CROSSREF_DIR = os.path.join(our_path, "cross-ref-csv")
OUTPUT_DIR = os.path.join(our_path, "output-csv")

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
