from datetime import datetime

from agent.models import Booking, LandlordRequest
from agent.reconcile import find_booking, time_mismatch

BOOKING = Booking("EE-1", "1 Test Road, London W8 4QX",
                  datetime(2026, 10, 20, 8, 0), datetime(2026, 10, 20, 10, 0))


def request_at(hour, minute=0, address="1 Test Road, London W8 4QX"):
    return LandlordRequest("Test Tenant", "07700 900000", address,
                           datetime(2026, 10, 20, hour, minute))


def test_time_inside_window_is_fine():
    assert not time_mismatch(request_at(9), BOOKING)


def test_time_outside_window_is_flagged():
    assert time_mismatch(request_at(13), BOOKING)


def test_window_edges_count_as_inside():
    assert not time_mismatch(request_at(8), BOOKING)
    assert not time_mismatch(request_at(10), BOOKING)


def test_matches_on_postcode_even_if_street_written_differently():
    req = request_at(9, address="1 test rd, w84qx")
    assert find_booking(req, [BOOKING]) is BOOKING
