from datetime import datetime

OUTPUT_FILE = "perugia.ics"

def create_ics():
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Perugia Calcio//Calendario//IT",
        "CALSCALE:GREGORIAN",
        "X-WR-TIMEZONE:Europe/Rome",

        "BEGIN:VEVENT",
        "UID:test-event-1",
        f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
        "DTSTART:20260815T203000",
        "DTEND:20260815T223000",
        "SUMMARY:Perugia vs Ternana",
        "DESCRIPTION:Test evento",
        "LOCATION:Stadio Renato Curi",
        "END:VEVENT",

        "END:VCALENDAR"
    ]

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    create_ics()
