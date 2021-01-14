# get script path
import os

our_path = os.getcwd()

# set some constants
RAW_DIR = os.path.join(our_path, "raw-csv")
MANGLED_DIR = os.path.join(our_path, "mangled-csv")
HEADER_DIR = os.path.join(our_path, "header-files")
