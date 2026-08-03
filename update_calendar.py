import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.transfermarkt.com/ac-perugia-calcio-1905/spielplan/verein/1381"
OUTPUT_FILE = "perugia.ics"


def fetch_matches():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    matches = []

    rows = soup.select("table.items tbody tr")

    for row in rows:
        try:
            date_cell = row.select_one("td.zentriert")
            if not date_cell:
                continue

            date_text = date_cell.text.strip()

            try:
                date_obj = datetime.strptime(date_text, "%b %d, %Y")
            except:
                continue

            home = row.select_one("td:nth-of-type(5)").text.strip()
            away = row.select_one("td:nth-of-type(7)").text.strip()
            competition = row.select_one("td:nth-of-type(2)").text.strip()

            matches.append({
                "date": date_obj,
                "home": home,
                "away": away,
                "competition": competition
            })

        except:
            continue

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
        start = m["date"].strftime("%Y%m%dT203000")
        end = m["date"].strftime("%Y%m%dT223000")

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
