import sqlite3
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PythonTicketsMCPServer");

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "helpdesk.db"
DB_PATH.parent.mkdir(exist_ok=True)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS tickets ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "user TEXT, issue TEXT, status TEXT DEFAULT 'open')"
    )
    return conn

@mcp.tool()
def create_ticket(user:str, issue:str) -> str:
    """Create an IT support ticket for a user. Returns the Ticket ID."""  # - Docstring for the tool
    conn = get_conn()
    cur = conn.execute("INSERT INTO tickets (user, issue) VALUES (?, ?)", (user, issue))
    conn.commit()
    tid = f"T-{cur.lastrowid:03d}"
    conn.close()
    return f"Created {tid} for {user} : {issue}"

@mcp.tool()
def get_ticket(ticket_id:str) -> str:
    """Get the status of a ticket by its ID, for example: T-001. """  # - Docstring for the tool
    try:
        num = int(ticket_id.upper().replace("T-", ""))
    except ValueError:
        return f"Invalid ticket ID: {ticket_id}"
    conn = get_conn()
    row = conn.execute(
        "SELECT id, user, issue, status FROM tickets WHERE id = ?", (num,)
    ).fetchone()
    conn.close()
    if not row:
        return f"Ticket {ticket_id} not found"
    return f"T-{row[0]:03d} | user: {row[1]} | issue: {row[2]} | status: {row[3]}"


if __name__ == "__main__":
    mcp.run(transport="stdio")