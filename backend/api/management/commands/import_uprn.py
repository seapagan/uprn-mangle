"""Django command to format and import UPRN data to our database."""
import math
import os
from glob import glob
from pathlib import Path
from shutil import copyfile

import pandas as pd

# load constants from external file so we can share it
from api.management.support.constants import (
    CROSSREF_DIR,
    CROSSREF_NAME,
    HEADER_DIR,
    MANGLED_DIR,
    OUTPUT_DIR,
    OUTPUT_NAME,
    RAW_DIR,
)
from cursor import cursor
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine
from tqdm import tqdm


class Command(BaseCommand):
    """Base command class for import_uprn."""

    help = "Import raw data from CSV files into the database"

    def show_header(self, text_list, width=80):
        """Show a section Header with an arbitrary number of lines.

        Args:
            text_list (list): A list of Strings to be show, one per line
            width (int, optional): Width to make the box. Defaults to 50.
        """
        divider = "-" * (width - 2)
        self.stdout.write(self.style.HTTP_NOT_MODIFIED("\n/" + divider + "\\"))
        for line in text_list:
            self.stdout.write(
                self.style.HTTP_NOT_MODIFIED(
                    "|" + line.center((width - 2), " ") + "|"
                )
            )
        self.stdout.write(self.style.HTTP_NOT_MODIFIED("\\" + divider + "/"))
        self.stdout.write("\n")

    def chunker(self, seq, size):
        """Return chunks of the dataframe."""
        # fmt: off
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))
        # fmt: on

    def insert_with_progress(self, df, engine):
        """Insert the data to SQL, with a progress bar."""
        table_name = str(os.getenv("UPRN_DB_TABLE"))
        conn = engine.connect()
        conn.execute(f"TRUNCATE TABLE {table_name}")
        chunksize = int(len(df) / 100)
        with tqdm(
            total=len(df), ncols=80, unit=" records", leave=False
        ) as pbar:
            for i, cdf in enumerate(self.chunker(df, chunksize)):
                cdf.to_sql(
                    name=table_name,
                    con=conn,
                    if_exists="append",
                    index=False,
                )
                pbar.update(chunksize)
                tqdm._instances.clear()

    def phase_one(self):
        """Run phase 1 : Read in the raw CSV and mangle.

        Take the raw CSV files and mangle them into a format that is easier to
        work with, seperate files for each record type.
        """
        self.show_header(["Phase 1", "Mangle the Raw Files"])

        # loop through the header csv files and make a list of the codes and
        # filenames. We are generating this dynamically in case it changes in
        # the future.
        header_files = sorted(glob(os.path.join(HEADER_DIR, "*.csv")))
        # delete the current *.csv here first
        [f.unlink() for f in Path(MANGLED_DIR).glob("*.csv") if f.is_file()]

        # set up the dictionary and create the skeleton files
        code_list = {}
        for filepath in header_files:
            # drop the path
            header_filename = os.path.basename(filepath)
            # get the record number
            record = header_filename.split("Record_")[1].split("_")[0]
            filename = header_filename[:-11] + ".csv"
            # add it to the dictionary with the record as a key
            code_list[record] = filename

            # create an empty file with the contents of the header file
            # we basically just copy the file over and rename
            destpath = os.path.join(MANGLED_DIR, filename)
            copyfile(filepath, destpath)

        # get list of all *csv to process
        input_files = glob(os.path.join(RAW_DIR, "*.csv"))

        # loop over all the files if empty
        for filename in tqdm(input_files, ncols=80, unit=" files", leave=False):
            with open(filename) as fp:
                # get the next line
                line = fp.readline()
                while line:
                    # get the record type
                    record = line.split(",")[0]
                    # get the correct output file for this record type
                    output_filename = os.path.join(
                        MANGLED_DIR, code_list[record]
                    )
                    # append this line to the output file
                    with open(output_filename, "a") as f:
                        f.write(line)
                        if record == "99":
                            # record type 99 is always at the end of the file,
                            # so is lacking a LF. Add one.
                            f.write("\n")
                    line = fp.readline()

    def phase_two(self):
        """Run phase 2 : Format as we need and export to CSV for next stage."""
        self.show_header(["Phase 2", "Consolidate data into one CSV."])

        # first we need to get a list of the sorted files.
        mangled_files = sorted(glob(os.path.join(MANGLED_DIR, "*.csv")))

        # get a list of the codes linked to their actual files
        code_list = {}
        for filepath in mangled_files:
            # drop the path
            filename = os.path.basename(filepath)
            # get the record number
            record = filename.split("Record_")[1].split("_")[0]
            # add it to the dictionary with the record as a key
            code_list[record] = filename

        self.stdout.write(" Reading in the required Fields...")

        # initialise the progress bar
        progress = tqdm(total=4, ncols=80, leave=False)

        # get record 15 (STREETDESCRIPTOR)
        raw_record_15 = pd.read_csv(
            os.path.join(MANGLED_DIR, code_list["15"]),
            usecols=[
                "USRN",
                "STREET_DESCRIPTION",
                "LOCALITY",
                "TOWN_NAME",
                "ADMINISTRATIVE_AREA",
            ],
            dtype={"USRN": "str"},
        )
        progress.update()

        # get record 21 (BPLU)
        raw_record_21 = pd.read_csv(
            os.path.join(MANGLED_DIR, code_list["21"]),
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
        progress.update()

        # get record 28 (DeliveryPointAddress)
        raw_record_28 = pd.read_csv(
            os.path.join(MANGLED_DIR, code_list["28"]),
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
        progress.update()

        # get record 32 (CLASSIFICATION)
        raw_record_32 = pd.read_csv(
            os.path.join(MANGLED_DIR, code_list["32"]),
            usecols=["UPRN", "CLASSIFICATION_CODE", "CLASS_SCHEME"],
        )
        progress.update()

        raw_record_32.set_index(["UPRN"], inplace=True)
        # record 32 has duplicate information for many UPRN, this will cause
        # the concat to fail. We are only interested in the ones that have the
        # scheme named : "AddressBase Premium Classification Scheme"
        filtered_record_32 = raw_record_32[
            raw_record_32.CLASS_SCHEME.str.contains("AddressBase")
        ]

        progress.close()
        # now bring in the cross reference file to link UPRN to USRN
        self.stdout.write(" Reading the UPRN <-> USRN reference file")
        cross_ref_file = os.path.join(CROSSREF_DIR, CROSSREF_NAME)

        # set a chunk size for reading the csv file
        chunk_size = 1000

        # work out number of rows in CVS, then calc # of chunks for the progress
        # bar
        number_of_rows = sum(1 for row in open(cross_ref_file, "r"))
        number_of_chunks = math.ceil(number_of_rows / chunk_size)

        tp = pd.read_csv(
            cross_ref_file,
            iterator=True,
            chunksize=chunk_size,
            usecols=["IDENTIFIER_1", "IDENTIFIER_2"],
            dtype={"IDENTIFIER_1": "str", "IDENTIFIER_2": "str"},
        )

        cross_ref = pd.concat(
            tqdm(
                tp,
                ncols=80,
                total=number_of_chunks,
                unit=" chunks",
                leave=False,
            ),
            ignore_index=True,
        )

        # lets rename these 2 headers to the better names
        cross_ref.rename(
            columns={"IDENTIFIER_1": "UPRN", "IDENTIFIER_2": "USRN"},
            inplace=True,
        )

        self.stdout.write(" Merging in the STREETDATA")
        # concat the STREETDESCRIPTOR to the cross ref file in this step
        merged_usrn = pd.merge(
            cross_ref,
            raw_record_15,
            how="left",
            left_on="USRN",
            right_on="USRN",
        )

        self.stdout.write(" Concating data ...")
        chunk1 = pd.concat(
            [
                raw_record_28,
                raw_record_21,
                filtered_record_32.drop(columns=["CLASS_SCHEME"]),
            ],
            axis=1,
        )

        # we dont want it indexed for the next stage, and need to clearly
        # specifiy the UPRN datatype
        chunk1.reset_index(inplace=True)
        merged_usrn.UPRN = merged_usrn.UPRN.astype(int)

        self.stdout.write(" Merging in the Street data ...")
        final_output = pd.merge(
            chunk1,
            merged_usrn,
            how="left",
            left_on="UPRN",
            right_on="UPRN",
        )

        # set the index back onto the UPRN
        final_output.set_index(["UPRN"], inplace=True)

        # finally, save the formatted data to a new CSV file.
        output_file = os.path.join(OUTPUT_DIR, OUTPUT_NAME)
        self.stdout.write(f"\n Saving to {output_file}")
        final_output.to_csv(output_file, index_label="UPRN", sep="|")

    def phase_three(self):
        """Read in the prepared CSV file and then store it in our DB."""
        self.show_header(
            [
                "Phase 3",
                "Load to database",
                "This may take a while depending on the amount of data.",
            ]
        )

        self.stdout.write(" Importing the Formatted AddressBase CSV file...")

        # set a chunk size for reading the csv file
        chunk_size = 1000

        # work out number of rows in CVS, then calc # of chunks for the progress
        # bar
        number_of_rows = sum(
            1 for row in open(os.path.join(OUTPUT_DIR, OUTPUT_NAME), "r")
        )
        number_of_chunks = math.ceil(number_of_rows / chunk_size)

        tp = pd.read_csv(
            os.path.join(OUTPUT_DIR, OUTPUT_NAME),
            # lets spell out the exact column types for clarity
            na_filter=False,
            iterator=True,
            chunksize=chunk_size,
            sep="|",
            dtype={
                "UPRN": "int",
                "SUB_BUILDING_NAME": "str",
                "BUILDING_NAME": "str",
                "BUILDING_NUMBER": "str",
                "THOROUGHFARE": "str",
                "POST_TOWN": "str",
                "POSTCODE": "str",
                "LOGICAL_STATUS": "int",
                # needs to be a string as annoyingly the data includes null
                # values
                "BLPU_STATE": "str",
                "X_COORDINATE": "double",
                "X_COORDINATE": "double",
                "LATITUDE": "double",
                "LONGITUDE": "double",
                "COUNTRY": "str",
                "CLASSIFICATION_CODE": "str",
                # also contains Null values for demolished buildings so must
                # be a string
                "USRN": "str",
                "STREET_DESCRIPTION": "str",
                "LOCALITY": "str",
                "TOWN_NAME": "str",
                "ADMINISTRATIVE_AREA": "str",
            },
        )

        # actually read each chunk and concat them into one dataframe
        ab_data = pd.concat(
            tqdm(
                tp,
                ncols=80,
                total=number_of_chunks,
                unit=" chunks",
                leave=False,
            ),
            ignore_index=True,
        )

        # at this point we want to create an extra field in the DataFrame, with
        # the address data concated for easier display.
        ab_data.insert(1, "FULL_ADDRESS", "")

        # now create a clean combined address from the relevant fields
        # doing this in 2 runs so we can sort out formatting in the first due
        # to any missing data.
        self.stdout.write(" Combining Address Fields...")
        tqdm.pandas(desc="First Pass", ncols=80, leave=False, unit=" records")
        ab_data["FULL_ADDRESS"] = (
            ab_data["SUB_BUILDING_NAME"]
            .str.cat(
                ab_data[
                    [
                        "BUILDING_NAME",
                        "BUILDING_NUMBER",
                        "THOROUGHFARE",
                    ]
                ],
                sep=" ",
            )
            .str.strip()  # trim extra space
            .str.title()  # convert to Title Case
        ).progress_apply(lambda x: x)

        # add the rest...
        tqdm.pandas(desc="Second Pass", ncols=80, leave=False, unit=" records")
        ab_data["FULL_ADDRESS"] = (
            ab_data["FULL_ADDRESS"]
            .str.cat(ab_data["POST_TOWN"].str.title(), sep=", ")
            .str.cat(
                ab_data["POSTCODE"], sep=", "
            )  # no Title mod for the Postcode
            .str.cat(ab_data["ADMINISTRATIVE_AREA"].str.title(), sep=", ")
        ).progress_apply(lambda x: x)

        # create a postgresql engine with SQLAlchemy that is linked to our
        # database
        db_url = "postgresql://{}:{}@{}:{}/{}".format(
            str(os.getenv("UPRN_DB_USER")),
            str(os.getenv("UPRN_DB_PASSWORD")),
            str(os.getenv("UPRN_DB_HOST")),
            str(os.getenv("UPRN_DB_PORT")),
            str(os.getenv("UPRN_DB_NAME")),
        )
        engine = create_engine(db_url)

        # now use the Pandas to_sql function to write to the database...
        # using the chunking function allows us to display a progress bar and
        # actually seriously speeds up the process.
        self.stdout.write(" Loading data to the Postgresql database... ")
        self.insert_with_progress(ab_data, engine)

    def handle(self, *args, **options):
        """Actual function called by the command."""
        cursor.hide()

        # self.phase_one()
        self.phase_two()
        # self.phase_three()

        self.stdout.write("\n Finished!")
        self.stdout.write(" You may now run the API Server.\n\n")

        cursor.show()
