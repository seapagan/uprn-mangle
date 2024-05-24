"""Handle settings for the application."""

import sys

from rich import print as rprint
from simple_toml_settings import TOMLSettings
from simple_toml_settings.exceptions import SettingsNotFoundError


class Settings(TOMLSettings):
    """Handle settings for the application."""

    db_user: str
    db_password: str
    db_name: str = "addressbase"
    db_host: str = "localhost"
    db_port: str = "5432"
    db_table: str = "addressbase"


def get_settings() -> Settings:
    """Get the settings."""
    try:
        settings = Settings.get_instance(
            "uprn_mangle", auto_create=False, local_file=True
        )

    except SettingsNotFoundError:
        rprint(
            "\n[red] -> Settings file not found, please create a settings "
            "file and try again.\n"
        )
        sys.exit(1)
    else:
        return settings
