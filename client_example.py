import asyncio
from fastmcp import Client

# Replace with the actual recipient number
RECIPIENT_WHATSAPP_NUMBER = "whatsapp:+12345678912"  # Must include whatsapp: prefix

async def main():
    # Connect to the server running via stdio
    async with Client("whatsapp_server.py") as client:
        print("Listing available tools...")
        tools = await client.list_tools()
        print(f"Found tools: {[t.name for t in tools]}")

        if any(t.name == "send_whatsapp_message" for t in tools):
            print(f"\nSending message to {RECIPIENT_WHATSAPP_NUMBER}...")
            try:
                result = await client.call_tool(
                    "send_whatsapp_message",
                    {
                        "to": RECIPIENT_WHATSAPP_NUMBER,
                        "body": "Hello from FastMCP! This is a message from Abiodun , sent through MCP 🚀"
                    }
                )
                print("\nTool Call Result:")
                print(result[0])  # Result is usually a list of content parts
            except Exception as e:
                print(f"\nError calling tool: {e}")
        else:
            print("send_whatsapp_message tool not found.")

if __name__ == "__main__":
    asyncio.run(main())
