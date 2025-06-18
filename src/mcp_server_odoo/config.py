import os

from dotenv import load_dotenv

DEFAULT_ODOO_VERSION = "18"
DEFAULT_ODOO_BASE_URL = "http://localhost:8069"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_TRANSPORT_PROTOCOL = "sse"
DEFAULT_TOOLS_TO_REGISTER = "search_partners,search_quotations,search_sales_orders"
DEFAULT_HOST = "127.0.0.1"


load_dotenv(override=True)


class ConfigError(ValueError):
    def __init__(self, message) -> None:
        super().__init__(message)


class Config:
    def __init__(self) -> None:
        self._odoo_base_url = os.getenv("ODOO_BASE_URL", DEFAULT_ODOO_BASE_URL)
        try:
            self._odoo_database = os.environ["ODOO_DATABASE"]
        except KeyError:
            raise ConfigError(
                "You must indicate a database to connect to using the ODOO_DATABASE "
                "environment variable... Exiting"
            )
        try:
            self._odoo_username = os.environ["ODOO_USERNAME"]
        except KeyError:
            raise ConfigError(
                "You must indicate a username to use for authentication to using the "
                "ODOO_USERNAME environment variable... Exiting"
            )
        try:
            self._odoo_password = os.environ["ODOO_PASSWORD"]
        except KeyError:
            raise ConfigError(
                "You must indicate a password to use for authentication to using the "
                "ODOO_PASSWORD environment variable... Exiting"
            )
        self._odoo_version = os.getenv("ODOO_VERSION", DEFAULT_ODOO_VERSION)
        if not 16 <= int(self._odoo_version) <= 18:
            raise NotImplementedError(
                f"The specified version of Odoo ('{self._odoo_version}') "
                "is not supported"
            )
        else:
            self._odoo_version = str(int(self._odoo_version))
        self._log_level = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)
        self._log_format = os.getenv("LOG_FORMAT", DEFAULT_LOG_FORMAT)
        self._transport_protocol = os.getenv(
            "TRANSPORT_PROTOCOL", DEFAULT_TRANSPORT_PROTOCOL
        )
        self._host = os.getenv("HOST", DEFAULT_HOST)
        self._tools_to_register = os.getenv(
            "TOOLS_TO_REGISTER", DEFAULT_TOOLS_TO_REGISTER
        )
        self._ext_directories = os.getenv("EXT_DIRECTORIES", "")
        self._xmlrpc_url = f"{self._odoo_base_url}/xmlrpc"

    @property
    def odoo_base_url(self) -> str:
        return self._odoo_base_url

    @property
    def odoo_username(self) -> str:
        return self._odoo_username

    @property
    def odoo_password(self) -> str:
        return self._odoo_password

    @property
    def odoo_version(self) -> str:
        return self._odoo_version

    @property
    def odoo_database(self) -> str:
        return self._odoo_database

    @property
    def log_level(self) -> str:
        return self._log_level

    @property
    def log_format(self) -> str:
        return self._log_format

    @property
    def transport_protocol(self) -> str:
        return self._transport_protocol

    @property
    def host(self) -> str:
        return self._host

    @property
    def tools_to_register(self) -> str:
        return self._tools_to_register

    @property
    def ext_directories(self) -> str:
        return self._ext_directories

    @property
    def xmlrpc_url(self) -> str:
        return self._xmlrpc_url
