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

    def _search_records(
        self, model: str, domain: list, fields: list[str], limit: int
    ) -> list[Any]:
        """Perform a search on records of a target model.

        Args:
            model: The model name, for example 'res_partner'.
            domain: The search domain, for example '[[["id", "=", 2]]]'.
            fields: The model fields to include in each record.
            limit: The maximum number of records to return.
        """
        method = "search"
        logger.info(
            "Executing method %s with model=%s, domain=%s, limit=%s",
            method,
            model,
            domain,
            limit,
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
        records = self._models.execute_kw(
            self._db,
            self._uid,
            self._password,
            model,
            "read",
            [ids],
            {"fields": fields},
        )
        return cast(list[Any], records)
