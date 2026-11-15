"""Run:  python _build/make_ics.py   - writes assets/calendar/poi-sunday-workshop.ics.
Write the recurring Sunday workshop calendar file (RFC 5545: CRLF line endings, 75-octet folding)."""
import sys
from pathlib import Path

out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "assets" / "calendar" / "poi-sunday-workshop.ics"
lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//POI Power of Interest UK//Sessions//EN",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "X-WR-CALNAME:POI Online Debate Workshop",
    "X-WR-TIMEZONE:Europe/London",
    "BEGIN:VTIMEZONE",
    "TZID:Europe/London",
    "X-LIC-LOCATION:Europe/London",
    "BEGIN:DAYLIGHT",
    "TZOFFSETFROM:+0000",
    "TZOFFSETTO:+0100",
    "TZNAME:BST",
    "DTSTART:19700329T010000",
    "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU",
    "END:DAYLIGHT",
    "BEGIN:STANDARD",
    "TZOFFSETFROM:+0100",
    "TZOFFSETTO:+0000",
    "TZNAME:GMT",
    "DTSTART:19701025T020000",
    "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU",
    "END:STANDARD",
    "END:VTIMEZONE",
    "BEGIN:VEVENT",
    "UID:poi-sunday-online-workshop@poi.org.uk",
    "DTSTAMP:20261115T120000Z",
    "DTSTART;TZID=Europe/London:20261122T090000",
    "DTEND;TZID=Europe/London:20261122T093000",
    "RRULE:FREQ=WEEKLY;BYDAY=SU",
    "SUMMARY:POI Online Debate Workshop",
    "DESCRIPTION:Free 30-minute online debate skills workshop from POI – Power "
    "of Interest. Occasional weeks may be skipped – check poi.org.uk for update"
    "s. Not signed up yet? Visit https://poi.org.uk/sessions.html#sign-up",
    "LOCATION:Google Meet (online)",
    "URL:https://poi.org.uk/sessions.html",
    "STATUS:CONFIRMED",
    "TRANSP:OPAQUE",
    "END:VEVENT",
    "END:VCALENDAR",
]


def fold(line):
    data = line.encode("utf-8")
    if len(data) <= 75:
        return [line]
    parts, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        limit = 75 if not parts else 74  # continuation lines start with a space
        if len(cur) + len(b) > limit:
            parts.append(cur.decode("utf-8"))
            cur = b""
        cur += b
    parts.append(cur.decode("utf-8"))
    return [parts[0]] + [" " + p for p in parts[1:]]


folded = [f for l in lines for f in fold(l)]
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(("\r\n".join(folded) + "\r\n").encode("utf-8"))
print("wrote", out, len(folded), "lines; longest", max(len(l.encode()) for l in folded))
