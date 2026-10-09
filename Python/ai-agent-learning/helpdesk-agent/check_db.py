import sqlite3
from pathlib import Path

db = Path(__file__).resolve().parent / "data" / "helpdesk.db"
conn = sqlite3.connect(db)

rows = conn.execute("SELECT id, user, issue, status FROM tickets").fetchall()
print(f"{len(rows)} ticket(s):")
for r in rows:
    print(f"T-{r[0]:03d} | {r[1]} | {r[2]} | {r[3]}")

conn.close()