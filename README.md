# Appointment Confirmation Agent

An AI agent that stops tenants missing electrician visits, built from a real problem at my family's electrical contracting business.

## The problem

We do a lot of work for landlords. A landlord would book a job with us, then tell their tenant a time themselves. Often that time didn't match the one in our diary. The engineer would arrive to an empty flat, or the tenant would wait in for nobody, and everyone was unhappy.

The fix in the business was simple: get the tenant's number from the landlord and text the tenant the real arrival window ourselves. This project automates that end to end.

## What it does

1. **Reads the landlord's email.** Claude extracts the tenant's name, phone number, address and the time the landlord told them, however the email is worded.
2. **Checks it against the diary.** It matches the job by postcode, because landlords write street names in different ways, and flags any time outside the booked arrival window.
3. **Texts the tenant.** It sends a confirmation with the real arrival window through Twilio, or prints it in dry-run mode.
4. **Catches jobs that aren't booked**, so nobody travels to a job that doesn't exist.

```
landlord email ──► extract (Claude) ──► match to diary ──► mismatch? ──► text tenant the real window
```

## Run it

```bash
pip install -r requirements.txt
python main.py        # dry run with the sample emails in data/
pytest                # run the tests
```

It runs without any keys: email extraction falls back to simple pattern matching and texts are printed, not sent. To use the real services, copy `.env.example` to `.env`, add your keys and export them.

## Example output

```
— 02_wrong_time.txt: Daniel Okafor, Flat 3, 77 Quill Street, London W11 2PL
  ⚠ Mismatch: tenant was told Tue 20 Oct 08:30, but job EE-1042 is booked 13:00–15:00. Correcting the tenant now.
  Text to 07700 900456 [dry run (not sent)]:
    Hi Daniel, this is Eamon Electrical. Our engineer will visit Flat 3, 77 Quill Street, London W11 2PL
    on Tuesday 20 October, arriving between 13:00 and 15:00. Reply YES to confirm, or reply to this message to rearrange.
```

All names, addresses and phone numbers in `data/` are made up. The phone numbers use Ofcom's range reserved for fiction.

## What's next

- Read emails straight from the business inbox instead of text files.
- Handle the tenant's reply: confirm the job on YES, alert the office on anything else.
- Send a reminder the evening before.
