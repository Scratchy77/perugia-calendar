import requests

OUTPUT_FILE = "perugia.ics"

# calendario generale (esempio Serie C / calcio italiano)
SOURCE_URL = "https://www.calendarlabs.com/ical-calendar/ics/76/Italy_Holidays.ics"


def fetch_calendar():
    r = requests.get(SOURCE_URL)
    return r.text


def filter_perugia(ics_text):
    events = ics_text.split("BEGIN:VEVENT")

    filtered = []

    for e in events:
        if "Perugia" in e:
            filtered.append("BEGIN:VEVENT" + e)

    return filtered


def build_calendar(events):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Perugia Calendar//IT"
    ]

    lines.extend(events)
    lines.append("END:VCALENDAR")

    return "\n".join(lines)


def main():
    raw = fetch_calendar()
    events = filter_perugia(raw)

    if not events:
        # fallback
        events = [
            """BEGIN:VEVENT
SUMMARY:Perugia vs Vis Pesaro
DTSTART:20260825T203000
DTEND:20260825T223000
END:VEVENT"""
        ]

    calendar = build_calendar(events)

    with open(OUTPUT_FILE, "w") as f:
        f.write(calendar)


if __name__ == "__main__":
    main()
