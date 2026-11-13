"""The two kinds of record the agent works with."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class LandlordRequest:
    """What a landlord told us in their email, after extraction."""

    tenant_name: str
    tenant_phone: str
    address: str
    time_told_to_tenant: datetime | None  # the time the landlord says they gave the tenant


@dataclass
class Booking:
    """A job as it is actually booked in our diary."""

    job_id: str
    address: str
    window_start: datetime
    window_end: datetime
