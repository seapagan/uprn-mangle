"""Handle settings for the application."""

from simple_toml_settings import TOMLSettings


class Settings(TOMLSettings):
    """Handle settings for the application."""

    db_user: str
    db_password: str
    db_name: str = "addressbase"
    db_host: str = "localhost"
    db_port: str = "5432"
    db_table: str = "addressbase"
