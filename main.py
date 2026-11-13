"""Run the agent over every landlord email in data/landlord_emails/.

    python main.py            # dry run: prints the report and the texts it would send
"""

from pathlib import Path

from agent.extract import extract_request
from agent.notify import compose_message, send_sms
from agent.reconcile import find_booking, load_bookings, time_mismatch

DATA = Path(__file__).parent / "data"


def run() -> None:
    bookings = load_bookings(DATA / "bookings.csv")

    for email_file in sorted((DATA / "landlord_emails").glob("*.txt")):
        request = extract_request(email_file.read_text())
        booking = find_booking(request, bookings)
        print(f"\n— {email_file.name}: {request.tenant_name}, {request.address}")

        if booking is None:
            print("  ⚠ No matching job in the diary. Check with the landlord before anyone travels.")
            continue

        if time_mismatch(request, booking):
            told = request.time_told_to_tenant.strftime("%a %d %b %H:%M")
            print(f"  ⚠ Mismatch: tenant was told {told}, but job {booking.job_id} is booked "
                  f"{booking.window_start:%H:%M}–{booking.window_end:%H:%M}. Correcting the tenant now.")
        else:
            print(f"  ✓ Times agree with job {booking.job_id}.")

        text = compose_message(request, booking)
        status = send_sms(request.tenant_phone, text)
        print(f"  Text to {request.tenant_phone} [{status}]:\n    {text}")


if __name__ == "__main__":
    run()
