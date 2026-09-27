import requests
from datetime import datetime, timedelta
import os
from zoneinfo import ZoneInfo

OUTPUT_FILE = "perugia.ics"
API_KEY = os.getenv("SCRAPINGBEE_API_KEY")
URL = "https://api.sofascore.com/api/v1/team/2698/events/next/0"


def fetch_matches():
    if not API_KEY:
        raise RuntimeError("SCRAPINGBEE_API_KEY non impostata")

    try:
        r = requests.get(
            "https://app.scrapingbee.com/api/v1/",
            params={
                "api_key": API_KEY,
                "url": URL,
                "premium_proxy": "true",
                "render_js": "false",
            },
            timeout=90,
        )
        print("STATUS:", r.status_code)
        if r.status_code != 200:
            print(r.text[:500])
            raise RuntimeError(f"ScrapingBee ha restituito HTTP {r.status_code}")

        data = r.json()
        if not isinstance(data, dict) or not isinstance(data.get("events"), list):
            raise ValueError("Risposta SofaScore senza lista events valida")

        matches = []
        now = datetime.now(ZoneInfo("Europe/Rome"))

        for m in data["events"]:
            try:
                home = m["homeTeam"]["name"]
                away = m["awayTeam"]["name"]
                timestamp = m["startTimestamp"]

                date_utc = datetime.fromtimestamp(
                    timestamp,
                    tz=ZoneInfo("UTC")
                )
                date_local = date_utc.astimezone(
                    ZoneInfo("Europe/Rome")
                )

                if date_local < now:
                    continue

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
        if not matches:
            raise RuntimeError("Nessuna partita futura trovata: calendario non modificato")
        return matches

    except Exception as e:
        print("ERRORE GENERALE:", e)
        raise


def create_ics(matches):
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

        competition = m["competition"].replace(
            "Knockout stage",
            "– Knockout stage"
        )

        description = (
            f"{competition}\\n\\n"
            f"Forza Grifo 🤍❤️\\n\\n"
            f"Se sei soddisfatto del calendario, offrimi un caffè ☕\\n"
            f"https://paypal.me/Scratchy77/1"
        )

        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{start}",
            f"DTEND:{end}",
            f"SUMMARY:{m['icon']} {m['home']} vs {m['away']} ({competition})",
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
