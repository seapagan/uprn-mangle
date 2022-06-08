"""Set some support constants etc we need for the import."""
# get script path
import os
from inspect import getsourcefile
from pathlib import Path

# get our running path, then create the data_path from this.
our_path = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))
data_path = os.path.join(str(Path(our_path).parents[2]), "data")

# set some constants for the other paths.
RAW_DIR = os.path.join(data_path, "raw-csv")
MANGLED_DIR = os.path.join(data_path, "mangled-csv")
HEADER_DIR = os.path.join(data_path, "header-files")
CROSSREF_DIR = os.path.join(data_path, "cross-ref-csv")
OUTPUT_DIR = os.path.join(data_path, "output-csv")

# this name should never change
CROSSREF_NAME = "BLPU_UPRN_Street_USRN_11.csv"

OUTPUT_NAME = "processed-addressbase.csv"
