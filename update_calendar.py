import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

OUTPUT_FILE = "perugia.ics"

URL = "https://www.google.com/search?q=perugia+calcio+partite"


def fetch_matches():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    matches = []

    # Google mostra partite in blocchi con classi particolari
    for div in soup.find_all("div"):
        text = div.get_text()

        if "Perugia" in text and "-" in text:
            try:
                parts = text.split("\n")

                for p in parts:
                    if "Perugia" in p and "-" in p:
                        teams = p.strip()

                        if " - " not in teams:
                            continue

                        home, away = teams.split(" - ")

                        matches.append({
                            "date": datetime.now(),
                            "home": home,
                            "away": away,
                            "competition": "Match"
                        })

            except:
                continue

    # fallback
    if not matches:
        return [
            {
                "date": datetime(2026, 8, 25, 20, 30),
                "home": "Perugia",
                "away": "Vis Pesaro",
                "competition": "Serie C"
            }
        ]

    return matches


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
        end = (m["date"] + timedelta(hours=2)).strftime("%Y%m%dT%H%M%S")

        uid = f"{m['home']}-{m['away']}-{m['date'].strftime('%Y%m%d')}"

        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{start}",
            f"DTEND:{end}",
            f"SUMMARY:{m['home']} vs {m['away']}",
            f"DESCRIPTION:{m['competition']}",
            "END:VEVENT"
        ])

    lines.append("END:VCALENDAR")

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(lines))


def main():
    matches = fetch_matches()
    create_ics(matches)


if __name__ == "__main__":
    main()
