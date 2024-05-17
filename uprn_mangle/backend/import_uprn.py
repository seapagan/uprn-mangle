"""Script to format and import UPRN data to a database."""

# mypy: disable_error_code="attr-defined"
import re
import sys
from itertools import tee
from pathlib import Path
from shutil import copyfile
from typing import TYPE_CHECKING, Any

import dask.dataframe as dd
import pandas as pd
from dask.diagnostics.progress import ProgressBar
from rich import print as rprint
from rich.console import Console
from rich.progress import Progress, SpinnerColumn
from simple_toml_settings.exceptions import SettingsNotFoundError
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from uprn_mangle.backend.config import Settings

# load constants from external file so we can share it
from uprn_mangle.backend.constants import (
    CROSSREF_DIR,
    CROSSREF_NAME,
    HEADER_DIR,
    MANGLED_DIR,
    OUTPUT_DIR,
    OUTPUT_NAME,
    RAW_DIR,
    WANTED_CODES,
)
from uprn_mangle.backend.models import Address, AddressCreate, Base

if TYPE_CHECKING:
    from collections.abc import Iterable
    from io import TextIOWrapper


class MangleUPRN:
    """Overall class to handle the UPRN data mangle and import."""

    def __init__(self) -> None:
        """Initialise the class."""
        # Load the settings
        try:
            self.settings = Settings.get_instance(
                "uprn_mangle", auto_create=False, local_file=True
            )
        except SettingsNotFoundError:
            rprint(
                "\n[red] -> Settings file not found, please create a settings "
                "file and try again.\n"
            )
            sys.exit(1)
        else:
            self.database_url = (
                f"postgresql://{self.settings.get('db_user')}:"
                f"{self.settings.db_password}@"
                f"{self.settings.db_host}:"
                f"{self.settings.db_port}/"
                f"{self.settings.db_name}"
            )

    def extract_record_type(self, filename: str) -> int:
        """Return just the record type from the filename.

        Used with the header files.
        """
        match = re.search(r"Record_(\d+)_", filename)
        if match:
            return int(match.group(1))

        msg = f"Filename {filename} does not match the expected format"
        raise ValueError(msg)

    def show_header(self, text_list: list[str], width: int = 80) -> None:
        """Show a section Header with an arbitrary number of lines.

        Args:
            text_list (list): A list of Strings to be shown, one per line
            width (int, optional): Width to make the box. Defaults to 50.
        """
        divider = "-" * (width - 2)
        rprint("\n[green]/" + divider + "\\")
        for line in text_list:
            rprint("[green]|" + line.center((width - 2), " ") + "|")
        rprint("[green]\\" + divider + "/")

    def run(self) -> None:
        """Run the mangle and import process."""
        # self.phase_one()
        # self.phase_two()
        self.phase_three()

    # ------------------------------------------------------------------------ #
    #                                  Phase 1                                 #
    # ------------------------------------------------------------------------ #
    def phase_one(self) -> None:
        """Run phase 1 : Read in the raw CSV and mangle.

        Take the raw CSV files and mangle them into a format that is easier to
        work with, separate files for each record type.
        """
        self.show_header(
            ["Phase 1", "Extract the required codes from the Raw Files"]
        )

        # Loop through the header CSV files and make a list of the codes and
        # filenames.
        header_files: list[Path] = sorted(HEADER_DIR.glob("*.csv"))

        rprint(f"\n -> Found {len(header_files)} header files")
        rprint("\n -> Deleting any existing mangled files...")

        # Delete the current *.csv files in the mangled directory
        for f in MANGLED_DIR.glob("*.csv"):
            if f.is_file():
                f.unlink()

        # Set up the dictionary and create the skeleton files
        code_list: dict[int, str] = {}
        output_file_handles: dict[int, TextIOWrapper] = {}
        try:
            for filepath in header_files:
                # Drop the path
                header_filename: str = filepath.name
                # Get the record number
                record_type: int = self.extract_record_type(header_filename)
                if record_type in WANTED_CODES:
                    filename: str = header_filename[:-11] + ".csv"
                    # Add it to the dictionary with the record as a key
                    code_list[record_type] = filename

                    destpath = MANGLED_DIR / filename
                    copyfile(filepath, destpath)

                    # Open the output file in append mode and store the handle
                    output_file_handles[record_type] = destpath.open(mode="a")

            input_files: Iterable[Path] = RAW_DIR.glob("*.csv")

            input_files, input_files_count = tee(input_files)

            num_files = sum(1 for _ in input_files_count)

            rprint(f" -> Found {num_files} raw files")

            for index, input_filename in enumerate(input_files, start=1):
                rprint(
                    f" -> Dealing with file {index} of {num_files}".ljust(
                        80, " "
                    ),
                    end="\r",
                )

                with input_filename.open() as fp:
                    for line in fp:
                        record_type = int(line.split(",")[0])
                        if record_type in WANTED_CODES:
                            # Write line to the appropriate output file handle
                            output_file_handles[int(record_type)].write(line)

        finally:
            # Ensure all file handles are properly closed
            for file_handle in output_file_handles.values():
                file_handle.close()

        rprint("\n -> Phase 1 completed")

    # ------------------------------------------------------------------------ #
    #                                  Phase 2                                 #
    # ------------------------------------------------------------------------ #
    def phase_two(self) -> None:
        """Run phase 2 : Format as we need and export to CSV for next stage."""
        self.show_header(["Phase2", "Consolidate data"])

        # first we need to get a list of the sorted files.
        mangled_files = sorted(MANGLED_DIR.glob("*.csv"))

        # get a list of the codes linked to their actual files
        code_list: dict[str, str] = {}
        for filepath in mangled_files:
            filename = Path(filepath).name
            record = filename.split("Record_")[1].split("_")[0]
            code_list[record] = filename

        rprint(" -> Reading in the required Records")

        def to_parquet_with_progress(
            ddf: dd.DataFrame, filename: Path, **kwargs: dict[str, Any]
        ) -> None:
            with ProgressBar():
                ddf.to_parquet(filename, **kwargs)

        def read_csv_to_parquet(
            record_num: str, usecols: list[str], dtype: dict[str, str]
        ) -> dd.DataFrame:
            csv_path = MANGLED_DIR / code_list[record_num]
            parquet_path = csv_path.with_suffix(".parquet")
            if not parquet_path.exists():
                ddf = dd.read_csv(csv_path, usecols=usecols, dtype=dtype)
                to_parquet_with_progress(ddf, parquet_path)
            return dd.read_parquet(parquet_path)

        # Get and convert records to Parquet format
        raw_record_15 = read_csv_to_parquet(
            "15",
            [
                "USRN",
                "STREET_DESCRIPTION",
                "LOCALITY",
                "TOWN_NAME",
                "ADMINISTRATIVE_AREA",
            ],
            {"USRN": "str"},
        )
        raw_record_21 = read_csv_to_parquet(
            "21",
            [
                "UPRN",
                "LOGICAL_STATUS",
                "BLPU_STATE",
                "X_COORDINATE",
                "Y_COORDINATE",
                "LATITUDE",
                "LONGITUDE",
                "COUNTRY",
            ],
            {"BLPU_STATE": "str", "LOGICAL_STATUS": "str"},
        )
        raw_record_28 = read_csv_to_parquet(
            "28",
            [
                "UPRN",
                "SUB_BUILDING_NAME",
                "BUILDING_NAME",
                "BUILDING_NUMBER",
                "THOROUGHFARE",
                "POST_TOWN",
                "POSTCODE",
            ],
            {
                "BUILDING_NUMBER": "str",
                "THOROUGHFARE": "str",
                "SUB_BUILDING_NAME": "str",
            },
        )
        raw_record_32 = read_csv_to_parquet(
            "32", ["UPRN", "CLASSIFICATION_CODE", "CLASS_SCHEME"], None
        )

        filtered_record_32 = raw_record_32[
            raw_record_32.CLASS_SCHEME.str.contains("AddressBase")
        ]

        rprint(" -> Reading the UPRN <-> USRN reference file")
        cross_ref_file = CROSSREF_DIR / CROSSREF_NAME
        cross_ref = dd.read_csv(
            cross_ref_file,
            usecols=["IDENTIFIER_1", "IDENTIFIER_2"],
            dtype={"IDENTIFIER_1": "str", "IDENTIFIER_2": "str"},
        )
        cross_ref = cross_ref.rename(
            columns={"IDENTIFIER_1": "UPRN", "IDENTIFIER_2": "USRN"}
        )

        rprint(" -> Merging in the STREETDATA")
        merged_usrn = dd.merge(
            cross_ref,
            raw_record_15,
            how="left",
            left_on="USRN",
            right_on="USRN",
        )
        to_parquet_with_progress(
            merged_usrn, MANGLED_DIR / "merged_usrn.parquet"
        )
        merged_usrn = dd.read_parquet(MANGLED_DIR / "merged_usrn.parquet")

        rprint(" -> Concatenating data")
        chunk1 = dd.concat(
            [
                raw_record_28,
                raw_record_21,
                filtered_record_32.drop(columns=["CLASS_SCHEME"]),
            ]
        )
        to_parquet_with_progress(chunk1, MANGLED_DIR / "chunk1.parquet")
        chunk1 = dd.read_parquet(MANGLED_DIR / "chunk1.parquet")

        rprint(" -> Merging all data to one dataframe")

        chunk1["UPRN"] = chunk1["UPRN"].astype(str)

        final_output: dd.DataFrame = dd.merge(
            chunk1, merged_usrn, how="left", left_on="UPRN", right_on="UPRN"
        )

        rprint(f"\n Saving to {OUTPUT_DIR / OUTPUT_NAME}")
        with ProgressBar():
            final_output.to_csv(
                OUTPUT_DIR / OUTPUT_NAME,
                index_label="IGNORE",
                sep="|",
                single_file=True,
            )

    # ------------------------------------------------------------------------ #
    #                                  Phase 3                                 #
    # ------------------------------------------------------------------------ #
    def generate_full_address(self, address: AddressCreate) -> str:
        """Generate full address by concatenating specific fields."""
        fields = [
            address.SUB_BUILDING_NAME.strip(),
            address.BUILDING_NAME.strip(),
            address.BUILDING_NUMBER.strip(),
            address.THOROUGHFARE.strip(),
            address.POST_TOWN.strip(),
            address.POSTCODE.strip(),
            address.ADMINISTRATIVE_AREA.strip(),
        ]
        return ", ".join([field for field in fields if field])

    def create_address(
        self, session: Session, address: AddressCreate
    ) -> Address:
        """Create a new address entry in the database."""
        db_address = Address(
            UPRN=address.UPRN,
            FULL_ADDRESS=self.generate_full_address(address),
            SUB_BUILDING_NAME=address.SUB_BUILDING_NAME,
            BUILDING_NAME=address.BUILDING_NAME,
            BUILDING_NUMBER=address.BUILDING_NUMBER,
            THOROUGHFARE=address.THOROUGHFARE,
            POST_TOWN=address.POST_TOWN,
            POSTCODE=address.POSTCODE,
            ADMINISTRATIVE_AREA=address.ADMINISTRATIVE_AREA,
            LOGICAL_STATUS=address.LOGICAL_STATUS,
            BLPU_STATE=address.BLPU_STATE,
            X_COORDINATE=address.X_COORDINATE,
            Y_COORDINATE=address.Y_COORDINATE,
            LATITUDE=address.LATITUDE,
            LONGITUDE=address.LONGITUDE,
            COUNTRY=address.COUNTRY,
            CLASSIFICATION_CODE=address.CLASSIFICATION_CODE,
            USRN=address.USRN,
            STREET_DESCRIPTION=address.STREET_DESCRIPTION,
            LOCALITY=address.LOCALITY,
            TOWN_NAME=address.TOWN_NAME,
        )
        try:
            session.add(db_address)
            session.commit()
            session.refresh(db_address)
        except IntegrityError:
            session.rollback()
        return db_address

    def process_chunk(self, session: Session, chunk: pd.DataFrame) -> None:
        """Process a chunk of the data."""
        for _, row in chunk.iterrows():
            address = AddressCreate(**row)
            self.create_address(session, address)

    def drop_table(self, engine: Engine) -> None:
        """Drop the addressbase table if it exists."""
        Base.metadata.drop_all(engine, tables=[Address.__table__])

    def phase_three(self) -> None:
        """Read in the prepared CSV file and then store it in our DB."""
        self.show_header(
            ["Phase3", "Load to database", "This may take a LONG time!!"]
        )

        engine = create_engine(self.database_url, echo=False)
        session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )

        # drop the existing table if it exists.
        # this allows updated UPRN's to be imported.
        self.drop_table(engine)

        with engine.begin() as conn:
            Base.metadata.create_all(conn)

        with session_local() as session:
            chunk_size = 2000
            converters = {
                "X_COORDINATE": lambda x: float(x) if x else 0.0,
                "Y_COORDINATE": lambda x: float(x) if x else 0.0,
                "LATITUDE": lambda x: float(x) if x else 0.0,
                "LONGITUDE": lambda x: float(x) if x else 0.0,
            }

            # Estimate the total number of rows
            file_path = OUTPUT_DIR / OUTPUT_NAME
            total_size = file_path.stat().st_size
            sample_size = 1024 * 1024  # 1MB sample size
            with file_path.open() as f:
                sample = f.read(sample_size)
            avg_row_size = len(sample) / sample.count("\n")
            estimated_total_rows = total_size / avg_row_size
            num_chunks = int((estimated_total_rows // chunk_size) + 1)

            console = Console(width=80, color_system="truecolor")

            with Progress(
                SpinnerColumn(),
                *Progress.get_default_columns(),
                expand=True,
                console=console,
            ) as progress:
                task = progress.add_task(
                    "Loading to Database", total=num_chunks
                )
                for chunk in pd.read_csv(
                    OUTPUT_DIR / OUTPUT_NAME,
                    sep="|",
                    dtype={
                        "UPRN": "int",
                        "SUB_BUILDING_NAME": "str",
                        "BUILDING_NAME": "str",
                        "BUILDING_NUMBER": "str",
                        "THOROUGHFARE": "str",
                        "POST_TOWN": "str",
                        "POSTCODE": "str",
                        "LOGICAL_STATUS": "str",
                        "BLPU_STATE": "str",
                        "COUNTRY": "str",
                        "CLASSIFICATION_CODE": "str",
                        "USRN": "str",
                        "STREET_DESCRIPTION": "str",
                        "LOCALITY": "str",
                        "TOWN_NAME": "str",
                        "ADMINISTRATIVE_AREA": "str",
                    },
                    na_filter=False,
                    chunksize=chunk_size,
                    converters=converters,
                ):
                    self.process_chunk(session, chunk)
                    progress.update(task, advance=1)


if __name__ == "__main__":
    mangle = MangleUPRN()
    mangle.run()
