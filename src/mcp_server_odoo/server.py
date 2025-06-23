import importlib
import importlib.util
import logging
import sys
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator

from mcp.server.fastmcp import FastMCP

from mcp_server_odoo.config import Config
from mcp_server_odoo.odoo_client import OdooClient

MCP_SERVER_NAME = "mcp-server-odoo"


config = Config()

logging.basicConfig(level=config.log_level, format=config.log_format)
logger = logging.getLogger(__name__)


@dataclass
class AppContext:
    client: OdooClient


@asynccontextmanager
async def app_lifespan(_: FastMCP) -> AsyncIterator[AppContext]:
    try:
        odoo_client = OdooClient(
            config.xmlrpc_url,
            config.odoo_username,
            config.odoo_password,
            config.odoo_database,
        )
        odoo_client.login()
        logger.info(f"Connected successfully to Odoo at {config.xmlrpc_url}")
        yield AppContext(client=odoo_client)
    except Exception as ex:
        logger.error(f"Failed to connect to Odoo {ex}")
        raise


class OdooMCP:
    def __init__(self) -> None:
        self._mcp = FastMCP(MCP_SERVER_NAME, lifespan=app_lifespan, host=config.host)
        self._register_capabilities()

    def _register_capabilities(self) -> None:
        """Register capabilities (tools, resources, prompts, ...) available at runtime.

        At the moment only tools are supported (see the tools documentation at
        https://modelcontextprotocol.io/docs/concepts/tools).

        Tools to expose must be configured from the user by setting the
        TOOLS_TO_REGISTER environment variable.
        """
        for tool in config.tools_to_register.split(","):
            tool_registered = False
            for ext_dir in config.ext_directories.split(","):
                file_path = Path(ext_dir) / "tools.py"
                if not file_path.is_file():
                    continue
                module_name = f"{file_path.stem}_{hash(file_path)}"
                spec = importlib.util.spec_from_file_location(
                    module_name, str(file_path)
                )
                if spec is None or spec.loader is None:
                    raise RuntimeError("Invalid source file at '%s'", file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                try:
                    self._mcp.add_tool(getattr(module, tool))
                    logger.info(f"registering tool '{tool}' (from {file_path})")
                    tool_registered = True
                except AttributeError:
                    pass

            if tool_registered:
                continue

            module_path = f"mcp_server_odoo.tools.v{config.odoo_version}"
            module = importlib.import_module(module_path)
            try:
                self._mcp.add_tool(getattr(module, tool))
                logger.info(f"registering tool '{tool}' (from {module_path})")
                tool_registered = True
            except AttributeError:
                pass

            if not tool_registered:
                logger.warning(
                    f"Tool '{tool}' not found. Check spelling and "
                    f"EXT_DIRECTORIES ({config.ext_directories})"
                )

    def run(self) -> None:
        logger.info("starting Odoo MCP server")
        self._mcp.run(transport=config.transport_protocol)
