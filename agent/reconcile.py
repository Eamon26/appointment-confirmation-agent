"""Step 2: match the landlord's request to our diary and catch time mismatches.

This is the check that would have prevented the original problem: a tenant
told one time while the engineer is booked for another.
"""

import csv
import re
from datetime import datetime
from pathlib import Path

from .models import Booking, LandlordRequest


def load_bookings(path: Path) -> list[Booking]:
    with open(path, newline="") as f:
        return [
            Booking(
                job_id=row["job_id"],
                address=row["address"],
                window_start=datetime.fromisoformat(row["window_start"]),
                window_end=datetime.fromisoformat(row["window_end"]),
            )
            for row in csv.DictReader(f)
        ]


def _postcode(address: str) -> str:
    """UK postcodes are the most reliable thing to match on; landlords write the street differently."""
    match = re.search(r"[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}", address.upper())
    return match.group(0).replace(" ", "") if match else address.upper().strip()


def find_booking(request: LandlordRequest, bookings: list[Booking]) -> Booking | None:
    wanted = _postcode(request.address)
    return next((b for b in bookings if _postcode(b.address) == wanted), None)


def time_mismatch(request: LandlordRequest, booking: Booking) -> bool:
    """True when the landlord told the tenant a time outside our arrival window."""
    told = request.time_told_to_tenant
    if told is None:
        return False  # nothing was promised, so there is nothing to contradict
    return not (booking.window_start <= told <= booking.window_end)
