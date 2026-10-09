import os
import asyncio
import traceback
import uuid
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

load_dotenv()
print("1. Started. Key loaded:", bool(os.getenv("OPENCODE_API_KEY")))

SESSION_ID=str(uuid.uuid4())

async def main():
    llm = ChatOpenAI(
    model="deepseek-v4-flash",
    temperature=0,
    api_key=os.environ.get("OPENCODE_API_KEY"),
    base_url="https://opencode.ai/zen/go/v1",
    default_headers={
        "x-opencode-session": SESSION_ID,
        "User-Agent": "helpdesk-agent/1.0",
    },
    )

    print("2. Testing the model alone...")
    print("Model Says:", llm.invoke("Say hello in 3 words").content)
    print("3. Starting MCP Server and Loading tools...")

    client = MultiServerMCPClient({
    "tickets": {"command": sys.executable, "args": ["mcp_servers/tickets.py"], "transport": "stdio"},
    "hr":      {"command": sys.executable, "args": ["mcp_servers/hr.py"],      "transport": "stdio"},
    "kb":      {"command": sys.executable, "args": ["mcp_servers/kb.py"],      "transport": "stdio"},
    })

    tools = await client.get_tools()
    print("Tools found:", [t.name for t in tools])

    print("4. Running the agent...")
    agent = create_agent(llm, tools)
    q = "My laptop screen is flickering. I am user ravi. Please raise a ticket."
    result = await agent.ainvoke({"messages": [("user", q)]})
    for m in result["messages"]:
        print(f"[{m.type}] {m.content}")

try:
    asyncio.run(main())
except Exception:
    traceback.print_exc()

print("5. Finished.")


