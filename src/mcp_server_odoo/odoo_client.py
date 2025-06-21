import logging
import xmlrpc.client
from typing import Any, cast

logger = logging.getLogger(__name__)


class OdooClient:
    def __init__(self, url: str, username: str, password: str, db: str) -> None:
        """Istantiate the Odoo XML-RPC client.

        Args:
            url: The base_url of the Odoo instance.
            username: The username to use for authentication.
            password: The password to use for authentication.
            db: The database to use.
        """
        self._url = url
        self._username = username
        self._password = password
        self._db = db
        self._common = xmlrpc.client.ServerProxy(f"{self._url}/2/common")
        self._models = xmlrpc.client.ServerProxy(f"{self._url}/2/object")
        self._uid: int | None = None

    def login(self) -> None:
        """Authenticate to remote instance via XML-RPC.

        Raises:
            ConnectionError: In case authenticate() call fails.
        """
        try:
            uid = self._common.authenticate(
                self._db, self._username, self._password, {}
            )
            if not uid:
                raise ConnectionError(
                    "Authentication failed. Are ODOO_DATABASE, ODOO_USERNAME and "
                    "ODOO_PASSWORD set correctly?"
                )
            self._uid = cast(int, uid)
        except Exception as ex:
            raise ex

    def _search(self, model: str, domain: list, limit: int) -> list[int]:
        """Search for all records of model matching given domain.

        The number of elements to return is limited up to 'limit'.

        Args:
            model: The model name, for example 'res_partner'.
            domain: The search domain, for example '[[["name", "ilike", "foo"]]]'.
            limit: The maximum number of records to return.
        """
        method = "search"
        logger.info(
            "Executing '%s' method on model '%s'",
            method,
            model,
        )
        ids = self._models.execute_kw(
            self._db,
            self._uid,
            self._password,
            model,
            method,
            domain,
            {"limit": limit},
        )
        return cast(list[int], ids)

    def _read(self, model: str, ids: list[int], fields: list[str]) -> list[Any]:
        """Retrieve records data.

        Args:
            model: The model name, for example 'res_partner'.
            ids: A list of record ID to fetch.
            fields: The model fields to include in each record.
        """
        method = "read"
        logger.info(
            "Executing '%s' method on model '%s'",
            method,
            model,
        )
        records = self._models.execute_kw(
            self._db,
            self._uid,
            self._password,
            model,
            method,
            [ids],
            {"fields": fields},
        )
        return cast(list[Any], records)
