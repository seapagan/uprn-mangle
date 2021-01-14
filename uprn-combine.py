# this script will take the sorted data and create a single file containing
# only the required data columns, suitable for loading into a database.

import os
import pandas as pd
from glob import glob

# load constants from external file so we can share it
from constants import MANGLED_DIR

# first we need to get a list of the sorted files.
mangled_files = sorted(glob(os.path.join(MANGLED_DIR, "*.csv")))

# get a list of the codes linked to their actual files
CODE_LIST = {}
for filepath in mangled_files:
    # drop the path
    filename = os.path.basename(filepath)
    # get the record number
    record = filename.split("Record_")[1].split("_")[0]
    # add it to the dictionary with the record as a key
    CODE_LIST[record] = filename

# get record 15 (STREETDESCRIPTOR)
raw_record_15 = pd.read_csv(
    os.path.join(MANGLED_DIR, CODE_LIST["15"]),
    usecols=[
        "USRN",
        "STREET_DESCRIPTION",
        "LOCALITY",
        "TOWN_NAME",
        "ADMINISTRATIVE_AREA",
    ],
)

# get record 21 (BPLU)
raw_record_21 = pd.read_csv(
    os.path.join(MANGLED_DIR, CODE_LIST["21"]),
    usecols=[
        "UPRN",
        "X_COORDINATE",
        "Y_COORDINATE",
        "LATITUDE",
        "LONGITUDE",
    ],
)
raw_record_21.set_index(["UPRN"], inplace=True)

# get record 28 (DeliveryPointAddress)
raw_record_28 = pd.read_csv(
    os.path.join(MANGLED_DIR, CODE_LIST["28"]),
    usecols=["UPRN", "UDPRN", "BUILDING_NAME", "POST_TOWN", "POSTCODE"],
)
raw_record_28.set_index(["UPRN"], inplace=True)

# get record 32 (CLASSIFICATION)
raw_record_32 = pd.read_csv(
    os.path.join(MANGLED_DIR, CODE_LIST["32"]),
    usecols=["UPRN", "CLASSIFICATION_CODE"],
)
raw_record_32.set_index(["UPRN"], inplace=True)

# print(raw_record_15)
# print(raw_record_21)
# print(raw_record_28)
# print(raw_record_32)
