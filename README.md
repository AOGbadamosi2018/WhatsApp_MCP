# WhatsApp MCP Server

This project implements an MCP server that provides a tool to send WhatsApp messages via the Twilio API.

## Prerequisites

1. Python 3.10+
2. Twilio account with configured WhatsApp sender
3. FastMCP installed

## Setup

1. Create a `.env` file in the project root with your Twilio credentials:
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_FROM_NUMBER=your_whatsapp_number
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

You can run the server in two ways:

1. Directly with Python (Stdio):
```bash
python whatsapp_server.py
```

2. Using FastMCP CLI (Stdio):
```bash
fastmcp run whatsapp_server.py
```

For a persistent SSE server, uncomment the appropriate line in `whatsapp_server.py` and run:
```bash
python whatsapp_server.py
```

## Usage

The server provides a `send_whatsapp_message` tool that can be called with:
- `to`: Recipient WhatsApp number in E.164 format, prefixed with 'whatsapp:'
- `body`: The text content of the message

Example usage can be found in `client_example.py`
