# this will take the raw CSV files provide by Ordinance Survey
# 'AddressBase Premium and tweak into a more useful format.

# it will merge all the separate 5km files into combined files with the same
# header numbers.
# it will also create one combined file suitable for inserting into a database
# - removing all the unneeded columns (configurable)

import os
from glob import glob
from pathlib import Path
from shutil import copyfile

# load constants from external file so we can share it
from constants import RAW_DIR, MANGLED_DIR, HEADER_DIR

# loop through the header csv files and make a list of the codes and filenames.
# generating this dynamically in case it changes in the future.
header_files = sorted(glob(os.path.join(HEADER_DIR, "*.csv")))
# delete the current *.csv here first
[f.unlink() for f in Path(MANGLED_DIR).glob("*.csv") if f.is_file()]
# set up the dictionary and create the skeleton files
CODE_LIST = {}
for filepath in header_files:
    # drop the path
    header_filename = os.path.basename(filepath)
    # get the record number
    record = header_filename.split("Record_")[1].split("_")[0]
    filename = header_filename[:-11] + ".csv"
    # add it to the dictionary with the record as a key
    CODE_LIST[record] = filename

    # create an empty file with the contents of the header file
    # we basically just copy the file over and rename
    destpath = os.path.join(MANGLED_DIR, filename)
    copyfile(filepath, destpath)

# get list of all *csv to process
input_files = glob(os.path.join(RAW_DIR, "*.csv"))
# loop over all the files
for filename in input_files:
    print(f"Dealing with file {filename}")
    with open(filename) as fp:
        # get the next line
        line = fp.readline()
        while line:
            # get the record type
            record = line.split(",")[0]
            # get the correct output file for this record type
            output_filename = os.path.join(MANGLED_DIR, CODE_LIST[record])
            # append this line to the output file
            with open(output_filename, "a") as f:
                f.write(line)
                if record == "99":
                    # record type 99 is always at the end of the file, so
                    # is lacking a LF. Add one.
                    f.write("\n")
            line = fp.readline()
