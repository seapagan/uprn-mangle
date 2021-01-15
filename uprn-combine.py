# this script will take the sorted data and create a single file containing
# only the required data columns, suitable for loading into a database.

import os
import pandas as pd
from glob import glob

# load constants from external file so we can share it
from constants import MANGLED_DIR, CROSSREF_DIR, CROSSREF_NAME, OUTPUT_DIR

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
    dtype={"IDENTIFIER_2": "str"},
)

# lets rename these 2 headers to the better names
cross_ref.rename(
    columns={"IDENTIFIER_1": "UPRN", "IDENTIFIER_2": "USRN"}, inplace=True
)

# drop duplicates of the UPRN
print("Dropping duplicate UPRN's in the cross reference file")
cross_ref.drop_duplicates(subset=["UPRN"], inplace=True)
# index on the UPRN
cross_ref.set_index(["UPRN"], inplace=True)

# TODO : Would be good to pull in the proper STREETDESCRIPTOR data from Record
# 15 at this time, before the merge. We will need this in the final output.


print("Concating data ...")
result = pd.concat(
    [
        raw_record_28,
        raw_record_21,
        filtered_record_32.drop(columns=["CLASS_SCHEME"]),
        cross_ref,
    ],
    axis=1,
)

# After concating, the output has UPRN that were not in the original dataset
# since the cross ref file is the whole of the UK and generally the AddressBase
# is not. So, we will need to remove these extra rows.
print("Optimizing Output...")
optimized_result = result[result["LOGICAL_STATUS"].notnull()]

output_file = os.path.join(OUTPUT_DIR, "2processed-addressbase.csv")
print(f"\nSaving to {output_file}")
optimized_result.to_csv(output_file, index_label="UPRN")
# result.to_csv(output_file, index_label="UPRN")
print("Done!")
