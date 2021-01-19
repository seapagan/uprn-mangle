# this script will take the sorted data and create a single file containing
# only the required data columns, suitable for loading into a database.

# probably not the most elegant way to do this, but works for now and can be
# improved later.

import os
import pandas as pd
from glob import glob

# load constants from external file so we can share it
from constants import (
    MANGLED_DIR,
    CROSSREF_DIR,
    CROSSREF_NAME,
    OUTPUT_DIR,
    OUTPUT_NAME,
)

print(f"We are running from : {os.path.dirname(OUTPUT_DIR)}\n")

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

print("Reading in the required Records...")

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
    dtype={"USRN": "str"},
)

# get record 21 (BPLU)
raw_record_21 = pd.read_csv(
    os.path.join(MANGLED_DIR, CODE_LIST["21"]),
    usecols=[
        "UPRN",
        "LOGICAL_STATUS",
        "BLPU_STATE",
        "X_COORDINATE",
        "Y_COORDINATE",
        "LATITUDE",
        "LONGITUDE",
        "COUNTRY",
    ],
    dtype={"BLPU_STATE": "str", "LOGICAL_STATUS": "str"},
)
raw_record_21.set_index(["UPRN"], inplace=True)

# get record 28 (DeliveryPointAddress)
raw_record_28 = pd.read_csv(
    os.path.join(MANGLED_DIR, CODE_LIST["28"]),
    usecols=[
        "UPRN",
        "SUB_BUILDING_NAME",
        "BUILDING_NAME",
        "BUILDING_NUMBER",
        "THOROUGHFARE",
        "POST_TOWN",
        "POSTCODE",
    ],
    dtype={"BUILDING_NUMBER": "str"},
)
raw_record_28.set_index(["UPRN"], inplace=True)

# get record 32 (CLASSIFICATION)
raw_record_32 = pd.read_csv(
    os.path.join(MANGLED_DIR, CODE_LIST["32"]),
    usecols=["UPRN", "CLASSIFICATION_CODE", "CLASS_SCHEME"],
)
raw_record_32.set_index(["UPRN"], inplace=True)
# record 32 has duplicate information for many UPRN, this will cause the concat
# to fail. We are only interested in the ones that have the scheme named :
# "AddressBase Premium Classification Scheme"
filtered_record_32 = raw_record_32[
    raw_record_32.CLASS_SCHEME.str.contains("AddressBase")
]

# now bring in the cross reference file to link UPRN to USRN
print("Reading the UPRN <-> USRN reference file")
cross_ref_file = os.path.join(CROSSREF_DIR, CROSSREF_NAME)
cross_ref = pd.read_csv(
    cross_ref_file,
    usecols=["IDENTIFIER_1", "IDENTIFIER_2"],
    dtype={"IDENTIFIER_1": "str", "IDENTIFIER_2": "str"},
)

# lets rename these 2 headers to the better names
cross_ref.rename(
    columns={"IDENTIFIER_1": "UPRN", "IDENTIFIER_2": "USRN"}, inplace=True
)

print("Merging in the STREETDATA")
# concat the STREETDESCRIPTOR to the cross ref file in this step
merged_usrn = pd.merge(
    cross_ref,
    raw_record_15,
    how="left",
    left_on="USRN",
    right_on="USRN",
)

print("Concating data ...")
chunk1 = pd.concat(
    [
        raw_record_28,
        raw_record_21,
        filtered_record_32.drop(columns=["CLASS_SCHEME"]),
    ],
    axis=1,
)

# we dont want it indexed for the next stage, and need to clearly specifiy the
# UPRN datatype
chunk1.reset_index(inplace=True)
merged_usrn.UPRN = merged_usrn.UPRN.astype(int)

print("Merging in the Street data ...")
final_output = pd.merge(
    chunk1,
    merged_usrn,
    how="left",
    left_on="UPRN",
    right_on="UPRN",
)

# set the index back onto the UPRN
final_output.set_index(["UPRN"], inplace=True)

# finally, save the formatted data to a new CSV file and we are done for this.
output_file = os.path.join(OUTPUT_DIR, OUTPUT_NAME)
print(f"\nSaving to {output_file}")
final_output.to_csv(output_file, index_label="UPRN")
print("Done!")
