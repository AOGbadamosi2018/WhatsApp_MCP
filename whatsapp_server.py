import os
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException

from fastmcp import FastMCP

# --- Configuration ---
# Load credentials securely from environment variables via .env file
class TwilioSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TWILIO_", env_file=".env")

    account_sid: str = Field(..., description="Your Twilio Account SID")
    auth_token: str = Field(..., description="Your Twilio Auth Token")
    whatsapp_from_number: str = Field(
        ..., description="Your Twilio WhatsApp Sender Number (e.g., +14155238886)"
    )

try:
    settings = TwilioSettings()  # type: ignore[call-arg]
except Exception as e:
    print(f"Error loading Twilio settings: {e}")
    print("Please ensure you have a .env file with TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_WHATSAPP_FROM_NUMBER set.")
    exit(1)

# --- FastMCP Server Setup ---
mcp = FastMCP(
    name="WhatsApp Messenger",
    instructions="Provides a tool to send WhatsApp messages via Twilio.",
    dependencies=["twilio", "pydantic-settings"]
)

# --- Twilio Client Initialization ---
twilio_client = TwilioClient(settings.account_sid, settings.auth_token)

# --- Tool Definition ---
@mcp.tool()
def send_whatsapp_message(
    to: Annotated[str, Field(description="Recipient WhatsApp number in E.164 format, prefixed with 'whatsapp:' (e.g., whatsapp:+15551234567)")],
    body: Annotated[str, Field(description="This message was sent using Twilio and MCP by Abiodun")],
) -> dict:
    """
    Sends a WhatsApp message to the specified recipient using Twilio.

    Args:
        to: The recipient's WhatsApp number, including the 'whatsapp:' prefix.
        body: The message text to send.

    Returns:
        A dictionary indicating success or failure, including the message SID on success.
    """
    if not to.startswith("whatsapp:"):
        return {
            "success": False,
            "error": "Invalid 'to' number format. It must start with 'whatsapp:' followed by the E.164 number (e.g., whatsapp:+15551234567)."
        }

    try:
        message = twilio_client.messages.create(
            from_=f"whatsapp:{settings.whatsapp_from_number}",
            body=body,
            to=to
        )
        print(f"Message sent successfully! SID: {message.sid}")
        return {
            "success": True,
            "message_sid": message.sid,
            "status": message.status
        }
    except TwilioRestException as e:
        print(f"Twilio Error: {e}")
        return {
            "success": False,
            "error": f"Twilio API error: {e.msg}",
            "twilio_code": e.code,
            "status": e.status,
        }
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {
            "success": False,
            "error": f"An unexpected error occurred: {str(e)}"
        }

# --- Run the Server ---
if __name__ == "__main__":
    print(f"WhatsApp From Number: whatsapp:{settings.whatsapp_from_number}")
    print("Starting WhatsApp MCP Server...")
    mcp.run()  # Defaults to stdio transport
    # For a persistent server accessible over the network (e.g., via SSE):
    # mcp.run(transport="sse", port=8050)
