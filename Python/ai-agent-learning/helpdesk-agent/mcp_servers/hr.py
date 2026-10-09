from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hr")

LEAVE = {
    "Pandula":  {"annual": 14, "sick": 7},
    "Erandi": {"annual": 3,  "sick": 5},
}


@mcp.tool()
def get_leave_balance(user: str) -> str:
    """Get the remaining annual and sick leave days for an employee."""  # - Docstring for the tool
    b = LEAVE.get(user.lower())
    if not b:
        return f"No employee named {user}"
    return f"{user}: {b['annual']} annual days, {b['sick']} sick days left"


@mcp.tool()
def apply_leave(user: str, days: int) -> str:
    """Apply for annual leave. Deducts the days from the balance."""  # - Docstring for the tool
    b = LEAVE.get(user.lower())
    if not b:
        return f"No employee named {user}"
    if days > b["annual"]:
        return f"Not enough leave. {user} has only {b['annual']} days."
    b["annual"] -= days
    return f"Approved {days} days for {user}. Remaining: {b['annual']}"


if __name__ == "__main__":
    mcp.run(transport="stdio")