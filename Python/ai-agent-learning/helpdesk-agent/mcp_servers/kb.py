from mcp.server.fastmcp import FastMCP

mcp = FastMCP("kb")

POLICIES = {
    "refund": "Refunds are allowed within 30 days with a receipt.",
    "laptop": "Laptops are replaced every 3 years. Report faults to IT first.",
    "remote work": "Employees may work remotely up to 2 days per week.",
    "leave": "Annual leave over 5 days needs manager approval.",
}


@mcp.tool()
def search_policy(query: str) -> str:
    """Search company policies by keyword, for example 'refund' or 'remote work'."""  # - Docstring for the tool
    q = query.lower()
    hits = [text for key, text in POLICIES.items() if key in q or q in key]
    return "\n".join(hits) if hits else "No matching policy found."


if __name__ == "__main__":
    mcp.run(transport="stdio")