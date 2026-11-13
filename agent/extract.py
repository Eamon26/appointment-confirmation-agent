"""Step 1: turn a landlord's free-text email into a structured LandlordRequest.

With an ANTHROPIC_API_KEY set, Claude reads the email, so it copes with any
wording. Without a key, a simple pattern-matching fallback handles emails
written in the sample format, so the project still runs offline and in tests.
"""

import json
import os
import re
from datetime import datetime

from .models import LandlordRequest

PROMPT = """You extract booking details from a landlord's email to an electrical contractor.
Return only a JSON object with these keys:
  tenant_name (string), tenant_phone (string, digits and spaces only),
  address (string, first line and postcode),
  time_told_to_tenant (ISO 8601 date-time the landlord says they gave the tenant, or null).
Today's date is {today}. Resolve phrases like "next Tuesday at 10" to a full date-time.

Email:
{email}"""


def extract_request(email_text: str) -> LandlordRequest:
    if os.getenv("ANTHROPIC_API_KEY"):
        return _extract_with_claude(email_text)
    return _extract_with_patterns(email_text)


def _extract_with_claude(email_text: str) -> LandlordRequest:
    import anthropic  # imported here so the offline mode needs no packages

    client = anthropic.Anthropic()
    reply = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5"),
        max_tokens=400,
        messages=[{
            "role": "user",
            "content": PROMPT.format(today=datetime.now().date().isoformat(), email=email_text),
        }],
    )
    text = reply.content[0].text
    data = json.loads(text[text.index("{"): text.rindex("}") + 1])  # tolerate stray words around the JSON
    when = data.get("time_told_to_tenant")
    return LandlordRequest(
        tenant_name=data["tenant_name"],
        tenant_phone=data["tenant_phone"],
        address=data["address"],
        time_told_to_tenant=datetime.fromisoformat(when) if when else None,
    )


def _extract_with_patterns(email_text: str) -> LandlordRequest:
    def field(label: str) -> str:
        match = re.search(rf"^{label}:\s*(.+)$", email_text, re.IGNORECASE | re.MULTILINE)
        return match.group(1).strip() if match else ""

    when = field("Told tenant")
    return LandlordRequest(
        tenant_name=field("Tenant"),
        tenant_phone=field("Phone"),
        address=field("Address"),
        time_told_to_tenant=datetime.strptime(when, "%d/%m/%Y %H:%M") if when else None,
    )
