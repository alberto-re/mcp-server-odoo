FROM ghcr.io/astral-sh/uv:python3.10-alpine

ADD . /mcp
WORKDIR /mcp
RUN uv sync --locked

CMD ["uv", "run", "mcp-server-odoo"]
