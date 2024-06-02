"""Set some support constants etc we need for the import."""

from pathlib import Path

# get our running path, then create the data_path from this.
our_path = Path(__file__).resolve().parent
data_path = our_path.parent / "data"

# set some constants for the other paths.
RAW_DIR = data_path / "raw-csv"
MANGLED_DIR = data_path / "mangled-csv"
HEADER_DIR = data_path / "header-files"
CROSSREF_DIR = data_path / "cross-ref-csv"
OUTPUT_DIR = data_path / "output-csv"

# these are the only code types we are interested in.
WANTED_CODES = [15, 21, 28, 32]

# this name should never change
CROSSREF_NAME = "BLPU_UPRN_Street_USRN_11.csv"

OUTPUT_NAME = "processed-addressbase.csv"
