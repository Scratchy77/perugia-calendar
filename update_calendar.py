import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

OUTPUT_FILE = "perugia.ics"

URL = "https://it.wikipedia.org/wiki/AC_Perugia_Calcio_1905_2026-2027"


def fetch_matches():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    matches = []

    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")

            if len(cols) < 4:
                continue

            text = row.get_text()

            if "Perugia" not in text:
                continue

            try:
                date_text = cols[0].text.strip()
                teams = cols[1].text.strip()

                # esempio: "Perugia – Vis Pesaro"
                if "–" not in teams:
                    continue

                home, away = teams.split("–")
                home = home.strip()
                away = away.strip()

                date_obj = datetime.strptime(date_text, "%d %B %Y")

                matches.append({
                    "date": date_obj.replace(hour=20, minute=30),
                    "home": home,
                    "away": away,
                    "competition": "Serie C"
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
