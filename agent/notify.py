"""Step 3: tell the tenant the real arrival window, by text.

With Twilio credentials set, messages are actually sent. Without them, the
agent runs in dry-run mode and only prints what it would send.
"""

import os

from .models import Booking, LandlordRequest


def compose_message(request: LandlordRequest, booking: Booking) -> str:
    first_name = request.tenant_name.split()[0] if request.tenant_name else "there"
    day = booking.window_start.strftime("%A %d %B")
    start = booking.window_start.strftime("%H:%M")
    end = booking.window_end.strftime("%H:%M")
    return (
        f"Hi {first_name}, this is Eamon Electrical. Our engineer will visit "
        f"{request.address} on {day}, arriving between {start} and {end}. "
        f"Reply YES to confirm, or reply to this message to rearrange."
    )


def send_sms(to_number: str, body: str) -> str:
    sid, token, sender = (os.getenv(k) for k in ("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_FROM_NUMBER"))
    if not (sid and token and sender):
        return "dry run (not sent)"
    from twilio.rest import Client  # only needed when really sending

    message = Client(sid, token).messages.create(to=to_number, from_=sender, body=body)
    return f"sent ({message.sid})"
