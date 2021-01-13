# this will take the raw CSV files provide by Ordinance Survey
# 'AddressBase Premium and tweak into more useful formats.j

# it will merge all the separate 5km files into combined files with the same
# header numbers
# it will also create one combined file suitable for inserting into a database
# - removing all the unneeded columns (configurable)

import os

# get script path
our_path = os.getcwd()

# set some constants
RAW_DIR = os.path.join(our_path, "raw-csv")
MANGLED_DIR = os.path.join(our_path, "mangled-csv")
HEADER_DIR = os.path.join(our_path, "header-files")
