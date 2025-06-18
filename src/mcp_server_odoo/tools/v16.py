from mcp.server.fastmcp import Context

from mcp_server_odoo.tools import common


async def search_partners(
    ctx: Context, name: str = "", email: str = "", limit: int = 100
) -> str:
    return await common.search_partners(ctx, name, email, limit)


search_partners.__doc__ = common.search_partners.__doc__


async def search_quotations(ctx: Context, limit: int = 100) -> str:
    return await common.search_quotations(ctx, limit)


search_quotations.__doc__ = common.search_quotations.__doc__


async def search_sales_orders(ctx: Context, limit: int = 100) -> str:
    return await common.search_sales_orders(ctx, limit)


search_sales_orders.__doc__ = common.search_sales_orders.__doc__


async def search_customer_invoices(ctx: Context, limit: int = 100) -> str:
    return await common.search_customer_invoices(ctx, limit)


search_customer_invoices.__doc__ = common.search_customer_invoices.__doc__
