# get script path
import os

# our_path = os.getcwd()
our_path = os.path.abspath(os.path.dirname(__file__))

# set some constants
RAW_DIR = os.path.join(our_path, "raw-csv")
MANGLED_DIR = os.path.join(our_path, "mangled-csv")
HEADER_DIR = os.path.join(our_path, "header-files")
CROSSREF_DIR = os.path.join(our_path, "cross-ref-csv")
OUTPUT_DIR = os.path.join(our_path, "output-csv")

# this name should never change
CROSSREF_NAME = "BLPU_UPRN_Street_USRN_11.csv"
