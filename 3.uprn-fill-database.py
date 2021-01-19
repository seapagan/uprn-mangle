import os
import pandas as pd

from sqlalchemy import create_engine

# load constants from external file so we can share it
from constants import (
    OUTPUT_DIR,
    OUTPUT_NAME,
    DB_HOST,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_TABLE,
)


print("\nUPRNTools : Importing ADDRESSBASE information to the Database.\n")
print(f"We are running from : {os.path.dirname(OUTPUT_DIR)}\n")

print("Importing the Formatted AddressBase CSV file...")
ab_data = pd.read_csv(
    os.path.join(OUTPUT_DIR, OUTPUT_NAME),
    # lets spell out the exact column types for clarity
    na_filter=False,
    dtype={
        "UPRN": "int",
        "SUB_BUILDING_NAME": "str",
        "BUILDING_NAME": "str",
        "BUILDING_NUMBER": "str",
        "THOROUGHFARE": "str",
        "POST_TOWN": "str",
        "POSTCODE": "str",
        "LOGICAL_STATUS": "int",
        # needs to be a string as annoyingly the data includes null values
        "BLPU_STATE": "str",
        "X_COORDINATE": "double",
        "X_COORDINATE": "double",
        "LATITUDE": "double",
        "LONGITUDE": "double",
        "COUNTRY": "str",
        "CLASSIFICATION_CODE": "str",
        # also contains Null values for demolished buildings so must  be a
        # string
        "USRN": "str",
        "STREET_DESCRIPTION": "str",
        "LOCALITY": "str",
        "TOWN_NAME": "str",
        "ADMINISTRATIVE_AREA": "str",
    },
)

# at this point we want to create an extra field in the DataFrame, with
# the address data concated for easier display.
ab_data.insert(1, "FULL_ADDRESS", "")

# now create a clean combined address from the relevant fields
print("Combining Address Fields...")
ab_data["FULL_ADDRESS"] = ab_data["SUB_BUILDING_NAME"].str.cat(
    ab_data[
        [
            "BUILDING_NAME",
            "BUILDING_NUMBER",
            "THOROUGHFARE",
        ]
    ],
    sep=" ",
)
# trim extra space from the first stage caused by empty fields
ab_data["FULL_ADDRESS"] = ab_data["FULL_ADDRESS"].str.strip()
# now add the next section
ab_data["FULL_ADDRESS"] = ab_data["FULL_ADDRESS"].str.cat(
    ab_data[
        [
            "POST_TOWN",
            "POSTCODE",
            "ADMINISTRATIVE_AREA",
        ]
    ],
    sep=", ",
)

# create a postgresql engine with SQLAlchemy that is linked to our database
db_url = "postgresql://{}:{}@{}:{}/{}".format(
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    5432,
    DB_NAME,
)
engine = create_engine(db_url)

# now use the Pandas to_sql function to write to the database...
# this will take a long time (Scotland is 5.7 Million rows for example and this
# takes 25 minutes on my decent PC). There are quicker ways to do this which I
# will look at later once the scripts are proven and trusted.
print("Exporting data to the Postgresql database ... this will take a while")
ab_data.to_sql(
    DB_TABLE, engine, if_exists="replace", index=False, chunksize=100
)
print("Done")
