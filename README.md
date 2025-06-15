# mcp-server-odoo

An extensible [Model Context Protocol](https://modelcontextprotocol.io) server that provides integration between [Odoo](https://www.odoo.com) and LLMs.

**Beware: the project is in very early development. Expect rough edges. We welcome any feedback!**

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Configuration

The MCP server is configured using environment variables.

The easiest way to set these up is to copy the `.env.example` file to `.env` and
edit the values for your environment.

Here's an example of how a typical `.env` looks like:

```
ODOO_BASE_URL=http://localhost:8069
ODOO_DATABASE=odoo
ODOO_USERNAME=admin
ODOO_PASSWORD=admin
ODOO_VERSION=18
LOG_LEVEL=INFO
TRANSPORT_PROTOCOL=sse
TOOLS_TO_REGISTER=search_partners,search_quotations,search_sales_orders
EXT_DIRECTORIES=
```

### Configuration options

1. ODOO_BASE_URL: the base url of your Odoo instance
2. ODOO_DATABASE: the database name to connect to
3. ODOO_USERNAME: the username to use for authentication
4. ODOO_PASSWORD: the password to use for authentication
5. ODOO_VERSION: major version of your Odoo server (currently supports versions 16, 17 and 18)
6. LOG_LEVEL: desired logging level (see [Python logging levels](https://docs.python.org/3/library/logging.html#logging-levels))
7. TRANSPORT_PROTOCOL: the [MCP transport protocol](https://modelcontextprotocol.io/docs/concepts/transports) to use. Valid values are `stdio` for local-only communication or `sse` / `streamable-http` for remote communication
8. TOOLS_TO_REGISTER: a comma-separated list of tools to expose to the MCP client. Tools can be chosen from those included within this project (see directory `src/mcp_server_odoo/tools`), or custom ones provided by external files (see `EXT_DIRECTORIES`)
9. EXT_DIRECTORIES: optional comma-separated list of paths to search for additional tools that can be loaded at runtime

## Run the server

```sh
uv run mcp-server-odoo
```

## Integrations

### Connecting to Claude Desktop

1. Edit the [Claude for Desktop](https://claude.ai/download) configuration file.
  - In MacOS the configuration is located at `~/Library/Application Support/Claude/claude_desktop_config.json`.
  - In Windows the configuration is located at `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the server configuration under the mcpServers section.

```json
{
  "mcpServers": {
    "mcp-server-odoo": {
      "command": "uv",
      "args": [
        "--directory",
        "/full/path/to/mcp-server-odoo",
        "run",
        "mcp-server-odoo"
      ]
    }
  }
}
```
3. Remember to set the environment variable TRANSPORT_PROTOCOL to 'stdio'.

4. Restart Claude for Desktop.
