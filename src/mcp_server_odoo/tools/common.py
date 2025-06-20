import json

from mcp.server.fastmcp import Context


async def search_partners(
    ctx: Context, name: str = "", email: str = "", limit: int = 100
) -> str:
    """
    Retrieve a list of Odoo partners (res.partner model) filtered by name or email.

    A "partner" in Odoo refers to a contact, customer, or supplier. This tool enables
    filtering partners by name or email and returns basic contact information.

    Args:
        name (str): Optional. Filter partners whose names contain this value
                    (case-insensitive).
        email (str): Optional. Filter partners whose emails contain this value.
        limit (int): Optional. Maximum number of results to return. Defaults to 100.

    Returns:
        A JSON-formatted string with a list of dictionaries, each representing a
        partner with fields:
            - name
            - phone
            - mobile
            - email
            - website

    Example Output:
        [
            {
                "name": "Acme Corp",
                "phone": "123456789",
                "mobile": null,
                "email": "info@acme.com",
                "website": "https://acme.com"
            },
            ...
        ]
    """
    model = "res.partner"
    domain = []
    if name:
        domain.append(["name", "ilike", name])
    if email:
        domain.append(["email", "ilike", email])
    fields = ["name", "phone", "mobile", "email", "website"]
    ids = ctx.request_context.lifespan_context.client._search(model, [domain], limit)
    partners = ctx.request_context.lifespan_context.client._read(model, ids, fields)
    return json.dumps(partners, indent=2)


async def search_sales_orders(ctx: Context, limit: int = 100) -> str:
    """
    Retrieve a list of Odoo sales orders (sale.order model) filtered by name or email.

    Args:
        limit (int): Optional. Maximum number of results to return. Defaults to 100.

    Returns:
        A JSON-formatted string with a list of dictionaries, each representing a sale
        order with fields:
            - name
            - date_order
            - payment_term_id
            - partner_id
    """
    model = "sale.order"
    domain = [["state", "in", ["sale"]]]
    fields = ["name", "date_order", "payment_term_id", "partner_id"]
    ids = ctx.request_context.lifespan_context.client._search(model, [domain], limit)
    sales_orders = ctx.request_context.lifespan_context.client._read(model, ids, fields)
    return json.dumps(sales_orders, indent=2)


async def search_quotations(ctx: Context, limit: int = 100) -> str:
    """
    Retrieve a list of Odoo quotations (sale.order model) filtered by name or email.

    Args:
        limit (int): Optional. Maximum number of results to return. Defaults to 100.

    Returns:
        A JSON-formatted string with a list of dictionaries, each representing a
        quotation with fields:
            - name
            - date_order
            - payment_term_id
            - partner_id
    """
    model = "sale.order"
    domain = [["state", "in", ["draft", "draft_sent"]]]
    fields = ["name", "state", "date_order", "payment_term_id", "partner_id"]
    ids = ctx.request_context.lifespan_context.client._search(model, [domain], limit)
    sales_orders = ctx.request_context.lifespan_context.client._read(model, ids, fields)
    return json.dumps(sales_orders, indent=2)


async def search_customer_invoices(ctx: Context, limit: int = 100) -> str:
    """
    Retrieve a list of Odoo customer invoices (account.move model) filtered by name
    or email.

    Args:
        limit (int): Optional. Maximum number of results to return. Defaults to 100.

    Returns:
        A JSON-formatted string with a list of dictionaries, each representing a
        customer invoice with fields:
            - name
            - partner_id
            - invoice_date
            - invoice_date_due
            - currency_id
            - amount_untaxed
            - amount_tax
            - amount_total
    """
    model = "account.move"
    domain = [["move_type", "=", "out_invoice"], ["state", "=", "posted"]]
    fields = [
        "name",
        "partner_id",
        "invoice_date",
        "invoice_date_due",
        "currency_id",
        "amount_untaxed",
        "amount_tax",
        "amount_total",
    ]
    ids = ctx.request_context.lifespan_context.client._search(model, [domain], limit)
    account_move = ctx.request_context.lifespan_context.client._read(model, ids, fields)
    return json.dumps(account_move, indent=2)
