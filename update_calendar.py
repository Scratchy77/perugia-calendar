```python
import requests
from datetime import datetime, timedelta
import os
from zoneinfo import ZoneInfo

OUTPUT_FILE = "perugia.ics"

API_KEY = os.getenv("SCRAPINGBEE_API_KEY")

URL = "https://api.sofascore.com/api/v1/team/2698/events/next/0"


def fetch_matches():
    scrape_url = f"https://app.scrapingbee.com/api/v1/?api_key={API_KEY}&url={URL}"

    try:
        r = requests.get(scrape_url)
        print("STATUS:", r.status_code)

        if r.status_code != 200:
            print(r.text[:200])
            return []

        data = r.json()

        matches = []
        now = datetime.now(ZoneInfo("Europe/Rome"))

        for m in data.get("events", []):
            try:
                home = m["homeTeam"]["name"]
                away = m["awayTeam"]["name"]

                timestamp = m["startTimestamp"]

                # UTC → Europe/Rome
                date_utc = datetime.fromtimestamp(
                    timestamp,
                    tz=ZoneInfo("UTC")
                )

                date_local = date_utc.astimezone(
                    ZoneInfo("Europe/Rome")
                )

                # Solo partite future
                if date_local < now:
                    continue

                # Casa / trasferta
                is_home = "perugia" in home.lower()
                icon = "🏠" if is_home else "✈️"

                matches.append({
                    "date": date_local,
                    "home": home,
                    "away": away,
                    "competition": m.get(
                        "tournament", {}
                    ).get("name", "Partita"),
                    "icon": icon
                })

            except Exception as e:
                print("Errore evento:", e)
                continue

        print("MATCHES:", len(matches))
        return matches

    except Exception as e:
        print("ERRORE GENERALE:", e)
        return []


def create_ics(matches):

    if not matches:
        matches = [
            {
                "date": datetime(
                    2026, 8, 25, 20, 30,
                    tzinfo=ZoneInfo("Europe/Rome")
                ),
                "home": "Perugia",
                "away": "Vis Pesaro",
                "competition": "Serie C",
                "icon": "🏠"
            }
        ]

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Perugia Calcio//Calendario//IT",
        "CALSCALE:GREGORIAN",
        "X-WR-TIMEZONE:Europe/Rome"
    ]

    for m in matches:

        start = m["date"].strftime("%Y%m%dT%H%M%S")
        end = (
            m["date"] + timedelta(hours=2)
        ).strftime("%Y%m%dT%H%M%S")

        uid = (
            f"{m['home']}-{m['away']}-"
            f"{m['date'].strftime('%Y%m%d')}"
        )

        description = (
            f"{m['competition']}\\n"
            f"Forza Grifo! 🤍❤️\\n"
            f"Se sei soddisfatto del servizio, "
            f"offrimi un caffè ☕\\n"
            f"👉 Offrimi un caffè – 1 €\\n"
            f"https://paypal.me/Scratchy77/1"
        )

        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{start}",
            f"DTEND:{end}",
            f"SUMMARY:{m['icon']} {m['home']} vs {m['away']} ({m['competition']})",
            f"DESCRIPTION:{description}",

            "BEGIN:VALARM",
            "TRIGGER:-PT1H",
            "ACTION:DISPLAY",
            "DESCRIPTION:Partita tra poco",
            "END:VALARM",

            "END:VEVENT"
        ])

    lines.append("END:VCALENDAR")

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
        newline=""
    ) as f:
        f.write("\r\n".join(lines))


def main():
    matches = fetch_matches()
    create_ics(matches)


if __name__ == "__main__":
    main()
```
