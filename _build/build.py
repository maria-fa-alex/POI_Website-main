"""Builds the POI website pages.

Run from anywhere:   python _build/build.py

  templates/   page bodies ({{HEADER:...}}, {{FOOTER}}, {{CTA}} ... are filled in here)
  source/      the original pages: their <head> SEO tags, FAQ answers and policy text are reused
  resources_data.py   the list of sessions shown on the Resources page

The shared header, footer and menu live in this file (header(), FOOTER, NAV).
Output goes straight into the website folder (the parent of _build/).
"""
import re
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent
TEMPLATES = BUILD / "templates"
ORIG = BUILD / "source"
SITE = BUILD.parent
sys.path.insert(0, str(BUILD))

DONATE = "https://www.zeffy.com/en-GB/donation-form/your-words-your-way"
FORM = "https://docs.google.com/forms/d/e/1FAIpQLSfbnTofT5rCoszg3Ss6L62FXiu2O5CAVo17pNzqVoErUJhwug/viewform?usp=header"
VOL_FORM = "https://forms.gle/StdUCLbzCbaD52zS6"
IMG = "assets/images/"

def svg(inner, size=20):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>')

ICONS = {
    "check": svg('<polyline points="20 6 9 17 4 12"/>', 16),
    "video": svg('<polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>'),
    "pin": svg('<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'),
    "mic": svg('<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M19 10v1a7 7 0 0 1-14 0v-1"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="8" y1="22" x2="16" y2="22"/>', 24),
    "heart": svg('<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>', 24),
    "users": svg('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>', 24),
    "calendar": svg('<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>'),
    "star": svg('<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>'),
    "megaphone": svg('<path d="M3 11v2a1 1 0 0 0 1 1h2l5 4V6L6 10H4a1 1 0 0 0-1 1z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M19 5a10 10 0 0 1 0 14"/>'),
    "book": svg('<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>', 24),
    "mail": svg('<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>'),
    "shield": svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>', 30),
    "clock": svg('<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'),
    "shuffle": svg('<polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/><line x1="4" y1="4" x2="9" y2="9"/>', 18),
    "reset": svg('<polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>', 18),
    "search": svg('<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>', 18),
    "gavel": svg('<path d="m14.5 12.5-8 8a2.12 2.12 0 1 1-3-3l8-8"/><path d="m16 16 6-6"/><path d="m8 8 6-6"/><path d="m9 7 8 8"/><path d="m21 11-8-8"/>', 24),
}

LINKEDIN = '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.779-1.75-1.75s.784-1.75 1.75-1.75 1.75.779 1.75 1.75-.784 1.75-1.75 1.75zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>'
INSTAGRAM = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>'
SOCIALS = (f'<div class="socials">'
           f'<a href="https://www.linkedin.com/company/poi-power-of-interest/" target="_blank" rel="noopener noreferrer" class="social-btn" aria-label="POI on LinkedIn">{LINKEDIN}</a>'
           f'<a href="https://www.instagram.com/power_of_interest" target="_blank" rel="noopener noreferrer" class="social-btn" aria-label="POI on Instagram">{INSTAGRAM}</a>'
           f'</div>')

NAV = [("about", "about.html", "Our Story"), ("sessions", "sessions.html", "Sessions"),
       ("resources", "resources.html", "Resources"), ("motions", "motions.html", "Motions"),
       ("volunteering", "volunteering.html", "Volunteer"),
       ("faq", "faq.html", "FAQ"), ("contact", "contact.html", "Contact")]
MOBILE_NAV = [("index", "index.html", "Home")] + NAV[:6] + [("policies", "policies.html", "Policies"), NAV[6]]


def header(active):
    def links(items):
        out = []
        for key, href, label in items:
            cur = ' class="active" aria-current="page"' if key == active else ''
            out.append(f'<a href="{href}"{cur}>{label}</a>')
        return "\n        ".join(out)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a href="index.html" class="header-brand" aria-label="POI – Power of Interest, home">
      <img src="{IMG}logo_no_words.jpg" alt="" class="header-logo" width="44" height="44" />
      <div class="header-brand-text">
        <span class="brand-title">POI</span>
        <span class="brand-sub">Power of Interest</span>
      </div>
    </a>
    <nav class="nav" aria-label="Main navigation">
      <div class="nav-links">
        {links(NAV)}
      </div>
      <div class="nav-actions">
        <button type="button" class="theme-toggle-btn" aria-label="Toggle colour theme"></button>
        <a href="support.html" class="btn btn-outline-yellow">Support Us</a>
        <a href="sessions.html#sign-up" class="btn btn-primary">Sign Up</a>
      </div>
    </nav>
    <button class="hamburger" id="hamburger" aria-label="Toggle menu" aria-expanded="false" aria-controls="mobile-nav">
      <span></span><span></span><span></span>
    </button>
  </div>
  <nav class="mobile-nav" id="mobile-nav" aria-label="Mobile navigation">
    {links(MOBILE_NAV)}
    <div class="mobile-nav-actions">
      <a href="support.html" class="btn btn-outline-yellow">Support Us</a>
      <a href="sessions.html#sign-up" class="btn btn-primary">Sign Up &rarr;</a>
    </div>
  </nav>
</header>'''


FORMSPREE = "https://formspree.io/f/xykbrlbj"
HONEYPOT = '<input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" />'

FOOTER = f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-newsletter" data-form-wrap>
      <div class="footer-newsletter-copy">
        <h4>Stay in the loop</h4>
        <p>Session breaks, new resources, and news about the 2027 Oxford sessions &mdash; straight to your inbox.</p>
      </div>
      <form class="newsletter-form" action="{FORMSPREE}" method="POST" data-ajax>
        <input type="hidden" name="_subject" value="Mailing List Sign-Up" />
        {HONEYPOT}
        <div class="newsletter-row">
          <label class="sr-only" for="newsletter-email">Email address</label>
          <input class="form-input" type="email" id="newsletter-email" name="Email" required autocomplete="email" placeholder="Your email address" />
          <button type="submit" class="btn btn-primary">Subscribe</button>
        </div>
        <label class="form-check form-check--dark"><input type="checkbox" name="Consent" value="Yes" required /> <span>I&rsquo;m 13 or over (or a parent or guardian) and happy to get emails from POI. You can unsubscribe at any time.</span></label>
        <p class="form-error" role="alert" hidden></p>
      </form>
      <div class="form-success" tabindex="-1" hidden><strong>You&rsquo;re subscribed!</strong> Thanks &mdash; look out for our next update.</div>
    </div>
    <div class="footer-grid">
      <div>
        <div class="footer-brand-row">
          <img src="{IMG}logo_no_words.jpg" alt="POI logo" class="footer-logo" width="52" height="52" />
          <span class="footer-brand-name">POI<small>Power of Interest UK</small></span>
        </div>
        <p class="footer-blurb">A student-founded not-for-profit building confident young speakers through free debate workshops &mdash; online for students worldwide, and in person in Oxford.</p>
        {SOCIALS}
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="about.html">Our Story</a></li>
          <li><a href="sessions.html">Sessions</a></li>
          <li><a href="resources.html">Resources</a></li>
          <li><a href="motions.html">Motion Bank</a></li>
          <li><a href="faq.html">FAQ</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Get Involved</h4>
        <ul>
          <li><a href="sessions.html#sign-up">Sign Up</a></li>
          <li><a href="volunteering.html">Volunteer</a></li>
          <li><a href="support.html">Support Us</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Organisation</h4>
        <ul>
          <li><a href="policies.html">Policies</a></li>
          <li><a href="policies.html#safeguarding">Safeguarding</a></li>
          <li><a href="mailto:contact@poi.org.uk">contact@poi.org.uk</a></li>
          <li><a href="contact.html">Summertown, Oxford</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 POI &ndash; Power of Interest UK. All rights reserved. Company Number: 17391401 (registered with Companies House).</p>
      <p>Proudly based in Oxford, Oxfordshire, England, serving students worldwide &middot; Typeface: <a href="assets/fonts/LICENSE-Sora.txt" target="_blank">Sora (SIL OFL)</a></p>
    </div>
  </div>
</footer>'''

CTA = '''<section class="section section--tight">
    <div class="container">
      <div class="cta-band reveal">
        <div>
          <h2>Ready to find your voice?</h2>
          <p>Get in touch with our team or register for our next session &mdash; it&rsquo;s free, and no experience is needed.</p>
        </div>
        <div class="cta-band-actions">
          <a href="sessions.html#sign-up" class="btn btn-dark">Join a Session <span class="arrow">&rarr;</span></a>
          <a href="contact.html" class="btn btn-outline">Get In Touch</a>
        </div>
      </div>
    </div>
  </section>'''

MOTIONS = [
    "This House would ban negative campaigning in elections",
    "This House would assign MPs via random lottery",
    "This House would ban the use of AI in schools",
    "This House believes Sports Days should be mandatory for all students who are able to participate",
    "This House would stop granting awards to media that use AI",
    "This House believes that phones should be banned in schools",
    "This House believes history education should prioritise the experiences of everyday people over the actions of great leaders",
    "This House would abolish the death penalty",
]

def ticker():
    one = "".join(f'<span class="ticker-item"><b>Motion</b>{m}</span>' for m in MOTIONS)
    return f'<div class="ticker-group">{one}</div><div class="ticker-group" aria-hidden="true">{one}</div>'

VER = "3.1"
ICON_LINKS = ('<link rel="icon" href="assets/images/favicon-32.png" type="image/png" sizes="32x32" />\n'
              '  <link rel="apple-touch-icon" href="assets/images/apple-touch-icon.png" />')

GCAL = ("https://calendar.google.com/calendar/render?action=TEMPLATE"
        "&amp;text=POI%20Online%20Debate%20Workshop"
        "&amp;dates=20261122T090000/20261122T093000&amp;ctz=Europe/London"
        "&amp;recur=RRULE:FREQ%3DWEEKLY%3BBYDAY%3DSU"
        "&amp;details=Free%2030-minute%20online%20debate%20workshop%20from%20POI%20%E2%80%93%20Power%20of%20Interest.%20"
        "Occasional%20weeks%20may%20be%20skipped%20%E2%80%93%20see%20poi.org.uk%20for%20updates."
        "&amp;location=Google%20Meet%20(online)")
CAL_ROW = ('<div class="cal-row"><span class="cal-label">Add to calendar</span>'
           f'<a class="cal-btn" href="{GCAL}" target="_blank" rel="noopener noreferrer">Google</a>'
           '<a class="cal-btn" href="assets/calendar/poi-sunday-workshop.ics">Apple / Outlook</a></div>')

THEME_INIT = ("<script>document.documentElement.classList.add('js');(function(){try{var t=localStorage.getItem('poi-theme');"
              "if(t==='light'||t==='dark'){document.documentElement.setAttribute('data-theme',t);}}catch(e){}})();</script>")

IMAGES = ["logo.jpg", "logo_no_words.jpg", "founders.jpg", "maria.jpg", "alison.jpg", "alan.jpg", "vivian.jpg",
          "background_chamber.jpg", "background_hall.jpg", "background_library.jpg", "background_room.jpg", "background_study.jpg"]


HEAD_FIXES = {
    "index": [
        ("offering free debate workshops and weekly British Parliamentary sessions in Oxford for secondary school students across the UK.",
         "offering free online debate workshops for secondary school students worldwide and weekly British Parliamentary sessions in Oxford."),
        ("Open to all UK secondary school students.", "Online sessions are open to secondary school students worldwide."),
        ("workshops for secondary school students across the UK, based in Oxford.",
         "workshops for secondary school students worldwide, based in Oxford."),
        ('"areaServed": {\n      "@type": "Country",\n      "name": "United Kingdom"\n    },', '"areaServed": "Worldwide",'),
    ],
    "sessions": [
        ('OfflineEventAttendanceMode",\n      "eventStatus": "https://schema.org/EventScheduled",',
         'OfflineEventAttendanceMode",\n      "eventStatus": "https://schema.org/EventPostponed",'),
    ],
    "about": [
        ("secondary school students in Oxford and across the UK.", "secondary school students in Oxford and around the world."),
        ("to young people across the UK.", "to young people around the world."),
    ],
    "volunteering": [
        ("secondary school students through free debate and public speaking in Oxford and across the UK.",
         "secondary school students through free debate and public speaking in Oxford and around the world."),
    ],
    "contact": [
        ("Based in Oxford, serving students across the UK.", "Based in Oxford, serving students worldwide."),
    ],
}


def process_head(page):
    src = (ORIG / f"{page}.html").read_text(encoding="utf-8")
    src = src.replace(chr(13) + chr(10), chr(10))
    for a, b in HEAD_FIXES.get(page, []):
        assert a in src[: src.index("</head>")], (page, a)
        src = src.replace(a, b)
    if page == "faq":
        for a, b in FAQ_FIXES:
            plain_a = a.replace("<strong>", "").replace("</strong>", "")
            plain_b = (b.replace("<strong>", "").replace("</strong>", "")
                        .replace("&mdash;", "—").replace("&ndash;", "–"))
            head_part = src[: src.index("</head>")]
            assert plain_a in head_part, plain_a
            src = src.replace(plain_a, plain_b, 1)
    head = src[: src.index("</head>")]
    lines = [l for l in head.splitlines() if "fonts.googleapis" not in l and "fonts.gstatic" not in l]
    head = "\n".join(lines)
    head = re.sub(r'<link rel="stylesheet" href="styles\.css\?v=[\d.]+" />',
                  '<meta name="theme-color" content="#0A0F2E" />\n  ' + THEME_INIT +
                  f'\n  <link rel="stylesheet" href="assets/css/styles.css?v={VER}" />', head)
    head = share_tags(head)
    head = head.replace("https://poi.org.uk/logo.jpg", "https://poi.org.uk/assets/images/logo.jpg")
    head = head.replace("https://poi.org.uk/founders.jpg", "https://poi.org.uk/assets/images/founders.jpg")
    if page == "sessions":
        head = weekly_event(head)
    assert '<link rel="icon" href="logo.jpg" type="image/jpeg" />' in head, page
    head = head.replace('<link rel="icon" href="logo.jpg" type="image/jpeg" />', ICON_LINKS)
    return head + "\n</head>\n<body>\n"


SHARE_IMG = "https://poi.org.uk/assets/images/share-card.jpg"
SHARE_TAGS = (f'<meta property="og:image" content="{SHARE_IMG}" />\n'
              '  <meta property="og:image:width" content="1200" />\n'
              '  <meta property="og:image:height" content="630" />\n'
              '  <meta property="og:image:alt" content="POI \u2013 Power of Interest: Your Words. Your Way. Free debate workshops for students." />')


def share_tags(head):
    """Large link-preview card everywhere except Our Story, which keeps the founders photo."""
    head = head.replace('<meta name="twitter:card" content="summary" />', '<meta name="twitter:card" content="summary_large_image" />')
    if "founders.jpg" in head:
        return head
    head = head.replace('<meta property="og:image" content="https://poi.org.uk/logo.jpg" />', SHARE_TAGS)
    head = head.replace('<meta name="twitter:image" content="https://poi.org.uk/logo.jpg" />',
                        f'<meta name="twitter:image" content="{SHARE_IMG}" />')
    return head


def next_uk_sunday(today=None):
    """Next Sunday (UK) and its UTC offset: BST from the last Sunday of March to the last Sunday of October."""
    import datetime as dt
    today = today or dt.date.today()
    day = today + dt.timedelta(days=(6 - today.weekday()) % 7 or 7)

    def last_sunday(year, month):
        d = dt.date(year, month + 1, 1) - dt.timedelta(days=1)
        return d - dt.timedelta(days=(d.weekday() + 1) % 7)
    bst = last_sunday(day.year, 3) <= day < last_sunday(day.year, 10)
    return day, ("+01:00" if bst else "+00:00")


def weekly_event(head):
    """The online workshop runs every Sunday: give Google the next date plus the weekly schedule."""
    day, off = next_uk_sunday()
    old = ('"startDate": "2026-09-20T09:00:00+01:00",\n      "endDate": "2026-09-20T09:30:00+01:00",')
    assert old in head, "online event dates not found"
    new = (f'"startDate": "{day.isoformat()}T09:00:00{off}",\n      "endDate": "{day.isoformat()}T09:30:00{off}",\n'
           '      "eventSchedule": {\n'
           '        "@type": "Schedule",\n'
           '        "repeatFrequency": "P1W",\n'
           '        "byDay": "https://schema.org/Sunday",\n'
           '        "startTime": "09:00:00",\n'
           '        "endTime": "09:30:00",\n'
           '        "scheduleTimezone": "Europe/London"\n'
           '      },')
    head = head.replace(old, new)
    head = head.replace('"description": "Free 30-minute online debate skills webinar for secondary school students. Perfect for beginners learning British Parliamentary debate."',
                        '"description": "Free 30-minute online debate skills webinar for secondary school students, held every Sunday at 9:00 AM UK time on Google Meet. Perfect for beginners learning British Parliamentary debate."')
    return head


def lazy_images(body):
    """Lazy-load every image except the header logo and the first illustration/photo on the page."""
    seen_first = False
    def repl(m):
        nonlocal seen_first
        tag = m.group(0)
        if "header-logo" in tag or "loading=" in tag:
            return tag
        if not seen_first and ("background_" in tag or "founders" in tag):
            seen_first = True
            return tag.replace("<img ", '<img fetchpriority="high" ', 1)
        return tag.replace("<img ", '<img loading="lazy" decoding="async" ', 1)
    return re.sub(r"<img [^>]+>", repl, body)


ITEM_RE = re.compile(
    r'<div class="accordion-item"(?: id="([^"]+)")?>\s*<button class="accordion-trigger">\s*<span>(.*?)</span>\s*'
    r'<div class="accordion-icon"></div>\s*</button>\s*<div class="accordion-content">\s*<div class="accordion-body">(.*?)</div>\s*</div>\s*</div>',
    re.S)


def clean_body(html):
    html = re.sub(r'\s+style="[^"]*"', "", html)
    html = re.sub(r"\n\s+", "\n", html.strip())
    return html


def render_item(item_id, title, body, num=None):
    idattr = f' id="{item_id}"' if item_id else ""
    label = f'<span class="accordion-num">{num}</span>{title}' if num else title
    body = "\n".join("              " + l for l in clean_body(body).splitlines())
    return (f'            <div class="accordion-item"{idattr}>\n'
            f'              <button class="accordion-trigger" aria-expanded="false"><span>{label}</span><span class="accordion-icon" aria-hidden="true"></span></button>\n'
            f'              <div class="accordion-content"><div class="accordion-body">\n{body}\n              </div></div>\n'
            f'            </div>')


FAQ_FIXES = [
    ("for secondary school students across the United Kingdom.",
     "for secondary school students &mdash; our online sessions are open to students anywhere in the world."),
    ("from <strong>Year 7 to Year 13</strong>.", "from <strong>Year 7 to Year 13</strong> (roughly ages 11&ndash;18), wherever you live."),
    ("Online sessions are held over Google Meet every Sunday morning.",
     "Online sessions are held over Google Meet every Sunday at 9:00 AM UK time, and you can join from anywhere."),
    ("at 9:00 AM via Google Meet.", "at 9:00 AM UK time via Google Meet."),
    ("allowing students nationwide to participate", "allowing students from anywhere in the world to participate"),
    ("will begin <strong>after October half term 2026</strong>.", "will begin in <strong>2027</strong> &mdash; exact dates to be confirmed."),
]


def faq_parts():
    src = (ORIG / "faq.html").read_text(encoding="utf-8")
    for a, b in FAQ_FIXES:
        assert a in src, a
        src = src.replace(a, b)
    items = ITEM_RE.findall(src)
    assert len(items) == 13, len(items)
    g1 = "\n".join(render_item(i, t, b) for i, t, b in items[:8])
    g2 = "\n".join(render_item(i, t, b) for i, t, b in items[8:])
    return {"FAQ_GROUP_1": g1, "FAQ_GROUP_2": g2, "FAQ_COUNT_1": "8", "FAQ_COUNT_2": "5"}


POLICY_CATS = [("Safeguarding &amp; Student Welfare", "welfare", 0, 5),
               ("Governance &amp; Accountability", "governance", 5, 10),
               ("People, Volunteers &amp; Conduct", "people", 10, 15),
               ("Operations, Data &amp; Safety", "operations", 15, 22)]


def policy_parts():
    src = (ORIG / "policies.html").read_text(encoding="utf-8")
    items = ITEM_RE.findall(src)
    assert len(items) == 22, len(items)
    groups, nav = [], []
    for n, (name, slug, a, b) in enumerate(POLICY_CATS, 1):
        rendered = []
        for _id, title, body in items[a:b]:
            num, _, label = title.partition("&bull;")
            body = body.replace("Policies%202026/", "docs/policies/")
            rendered.append(render_item(None, label.strip(), body, num.strip()))
        groups.append(f'''          <div class="qa-group reveal" id="{slug}">
            <div class="qa-group-head">
              <span class="eyebrow">Category 0{n}</span>
              <h2>{name}</h2>
            </div>
            <div class="accordion">
{chr(10).join(rendered)}
            </div>
          </div>''')
        nav.append(f'<a href="#{slug}">{name.split(" &amp;")[0].split(",")[0]} <small>{b - a}</small></a>')
    script = re.search(r"(<script>\s*\(function \(\) \{\s*var overlay.*?</script>)", src, re.S).group(1)
    return {"POLICY_GROUPS": "\n\n".join(groups), "POLICY_NAV": "\n          ".join(nav), "POLICY_SCRIPT": script}


def render_resource_card(d, latest=False):
    from resource_icons import TAG_SLIDES, TAG_GUIDE, TAG_ONLINE, BTN_DOC, BTN_DOWNLOAD
    n = f"{d['num']:02d}"
    tags, links = [], []
    if d.get("slides"):
        tags.append(f'<span class="resource-tag resource-tag--slides">{TAG_SLIDES} Slides</span>')
        suffix = " (Slides)" if d.get("guide") else ""
        links.append(f'<button type="button" class="btn btn-primary resource-btn open-viewer-btn" '
                     f'data-viewer-src="docs/slides/{d["slides"]}" data-viewer-title="Session {n}: {d["title"]}{suffix}">'
                     f'{BTN_DOC} View Slides</button>')
    if d.get("guide"):
        tags.append(f'<span class="resource-tag resource-tag--guide">{TAG_GUIDE} Motion Guide</span>')
        links.append(f'<div class="resource-action-group">'
                     f'<button type="button" class="btn btn-primary resource-btn open-viewer-btn" '
                     f'data-viewer-src="docs/slides/{d["guide"]}" data-viewer-title="Session {n}: Motion Walkthrough \u2013 {d["guide_name"]}" '
                     f'data-viewer-unrestricted="true">{BTN_DOC} View Motion Guide</button>'
                     f'<a href="docs/slides/{d["guide"]}" download="POI_{d["guide"]}" class="resource-btn-circle" '
                     f'aria-label="Download Motion Guide (PDF)" title="Download Motion Guide (PDF)">{BTN_DOWNLOAD}</a></div>')
    tags.append(f'<span class="resource-tag resource-tag--online">{TAG_ONLINE} Online</span>')
    cls = "resource-card resource-card--latest" if latest else "resource-card"
    return (f'            <!-- Session {d["num"]} Card -->\n'
            f'            <div class="{cls}">\n'
            f'              <div class="resource-card-header"><span class="resource-session-num">Session {n}</span>'
            f'<span class="resource-date">{d["date"]}</span></div>\n'
            f'              <h3>{d["title"]}</h3>\n'
            f'              <p>{d["description"]}</p>\n'
            f'              <div class="resource-tags">{"".join(tags)}</div>\n'
            f'              <div class="resource-links">{"".join(links)}</div>\n'
            f'            </div>')


def resources_parts():
    from resources_data import SESSIONS
    src = (ORIG / "resources.html").read_text(encoding="utf-8")
    for d in SESSIONS:
        for key in ("slides", "guide"):
            if d.get(key):
                assert (SITE / "docs" / "slides" / d[key]).exists(), f"missing PDF: docs/slides/{d[key]}"
    ordered = sorted(SESSIONS, key=lambda d: d["num"], reverse=True)   # newest first
    cards = "\n\n".join(render_resource_card(d, latest=(i == 0)) for i, d in enumerate(ordered))
    marker = "<!-- Placeholder: More Sessions Coming -->"
    placeholder = re.search(re.escape(marker) + r'(.*?</div>.*?</div>.*?</div>)', src, re.S).group(1)
    grid = '<div class="resources-grid">\n\n' + cards + "\n\n            " + marker + placeholder + "\n          </div>"
    modal_start = src.index("<!-- ===== EMBEDDED RESOURCE VIEWER MODAL ===== -->")
    modal = src[modal_start: src.index("</main>", modal_start)].rstrip()
    scripts = src[src.index('<script src="js/pdf.min.js"></script>'): src.index("</body>")].rstrip()

    def fix(t):
        return (t.replace('"slides/', '"docs/slides/')
                 .replace("'js/pdf.worker.min.js'", "'assets/js/pdf.worker.min.js'")
                 .replace('src="js/pdf.min.js"', 'src="assets/js/pdf.min.js"')
                 .replace('<script src="main.js"></script>', '<script src="assets/js/main.js?v=3.0"></script>'))
    return {"RESOURCES_GRID": "        " + grid, "RESOURCES_MODAL": "  " + fix(modal), "RESOURCES_SCRIPTS": fix(scripts)}


def build(page, extra=None):
    body = (TEMPLATES / f"{page}.body.html").read_text(encoding="utf-8")
    subs = {"SIGNUP": (TEMPLATES / "signup.partial.html").read_text(encoding="utf-8"),
            "VOLUNTEER_APPLY": (TEMPLATES / "volunteer-apply.partial.html").read_text(encoding="utf-8"),
            "HEADER:" + page: header(page), "FOOTER": FOOTER, "CTA": CTA, "TICKER": ticker(),
            "SOCIALS": SOCIALS, "DONATE": DONATE, "DONATE_PLAIN": DONATE, "FORM": FORM, "VOL_FORM": VOL_FORM,
            "FORMSPREE": FORMSPREE, "HONEYPOT": HONEYPOT, "CAL_ROW": CAL_ROW}
    subs.update(extra or {})
    for k, v in subs.items():
        body = body.replace("{{" + k + "}}", v)
    body = re.sub(r"\{\{ICON:(\w+)\}\}", lambda m: ICONS[m.group(1)], body)
    for name in IMAGES:
        body = body.replace(f'src="{name}"', f'src="{IMG}{name}"')
    body = body.replace('<script src="main.js?v=3.0"></script>', '<script src="assets/js/main.js?v=3.0"></script>')
    body = body.replace("assets/js/main.js?v=3.0", f"assets/js/main.js?v={VER}")
    body = lazy_images(body)
    left = re.findall(r"\{\{[^}]+\}\}", body)
    assert not left, (page, left)
    head = NEW_HEADS[page]() if page in NEW_HEADS else process_head(page)
    out = head + "\n" + body.rstrip() + "\n</body>\n</html>\n"
    if page == "404":  # served from any URL depth, so links must be root-relative
        out = re.sub(r'(href|src)="(?!https?:|mailto:|#|/)([^"]+)"', r'\1="/\2"', out)
    (SITE / f"{page}.html").write_text(out, encoding="utf-8", newline="\n")
    print("built", page, len(out))


def page404_head():
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Page Not Found | POI – Power of Interest UK</title>
  <meta name="robots" content="noindex" />
  <meta name="theme-color" content="#0A0F2E" />
  {THEME_INIT}
  <link rel="stylesheet" href="assets/css/styles.css?v={VER}" />
  {ICON_LINKS}
</head>
<body>
'''


MOTION_BANK = [
    # (motion, topics, session label, date note, walkthrough guide in Session Resources?)
    ("This House Would stop granting awards to media that use AI", ["Culture &amp; Media", "Technology"], "Session 07", "15 Nov 2026", True),
    ("This House supports vandalising cultural artifacts as a form of environmental protest", ["Environment", "Culture &amp; Media"], "Session 07", "Example from the Weighing slides", False),
    ("This House Would abolish the death penalty", ["Justice"], "Session 06", "8 Nov 2026", True),
    ("This House Would abolish prison as a punishment for non-violent crimes", ["Justice"], "Session 05", "18 Oct 2026", True),
    ("This House Believes that phones should be banned in schools", ["Education", "Technology"], "Session 04", "11 Oct 2026", True),
    ("This House Would not force students to learn a foreign language", ["Education"], "Session 03", "4 Oct 2026", True),
    ("This House Would ban the use of AI in schools", ["Education", "Technology"], "Session 02", "27 Sep 2026", True),
    ("This House would ban negative campaigning in elections", ["Politics"], None, None, False),
    ("This House would assign MPs via random lottery", ["Politics"], None, None, False),
    ("This House believes that history education should prioritise the experiences of everyday people over the actions of great leaders", ["Education"], None, None, False),
    ("This House believes Sports Days should be mandatory for all students who are able to participate", ["Education"], None, None, False),
]


def slug(t):
    return re.sub(r"[^a-z]+", "-", t.replace("&amp;", "and").lower()).strip("-")


def motion_parts():
    topics = []
    for _, ts, *_ in MOTION_BANK:
        for t in ts:
            if t not in topics:
                topics.append(t)
    chips = ['<button type="button" class="chip active" data-topic="all" aria-pressed="true">All</button>']
    chips += [f'<button type="button" class="chip" data-topic="{slug(t)}" aria-pressed="false">{t}</button>' for t in topics]
    cards = []
    for text, ts, sess, date, guide in MOTION_BANK:
        top = (f'<span class="tag tag--yellow">{sess}</span><span class="motion-date">{date}</span>' if sess
               else '<span class="tag">Practice motion</span>')
        tags = "".join(f'<span class="motion-topic">{t}</span>' for t in ts)
        guide_html = f'<a class="motion-guide" href="resources.html">{ICONS["check"]} Guide available</a>' if guide else ""
        cards.append(
            f'        <article class="motion-card" data-topics="{" ".join(slug(t) for t in ts)}">\n'
            f'          <div class="motion-card-top">{top}</div>\n'
            f'          <p class="motion-text">{text}</p>\n'
            f'          <div class="motion-topics">{tags}</div>\n'
            f'          <div class="motion-actions">\n'
            f'            <button type="button" class="motion-practise">Practise this &rarr;</button>\n'
            f'            {guide_html}\n'
            f'          </div>\n'
            f'        </article>')
    return {"TOPIC_CHIPS": "\n          ".join(chips), "MOTION_CARDS": "\n".join(cards)}


def new_page_head(title, description, path, og_title=None):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="POI – Power of Interest UK" />
  <meta property="og:title" content="{og_title or title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="https://poi.org.uk/{path}" />
  {SHARE_TAGS}
  <meta property="og:locale" content="en_GB" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{SHARE_IMG}" />
  <link rel="canonical" href="https://poi.org.uk/{path}" />
  <meta name="theme-color" content="#0A0F2E" />
  {THEME_INIT}
  <link rel="stylesheet" href="assets/css/styles.css?v={VER}" />
  {ICON_LINKS}
</head>
<body>
'''


def motions_head():
    return new_page_head("Motion Bank &amp; Prep Timer | POI – Power of Interest UK",
                         "Browse every debate motion from POI's free online workshops, plus practice motions, with a built-in 15-minute British Parliamentary prep timer. Open to secondary school students worldwide.",
                         "motions.html", "Motion Bank &amp; Prep Timer | POI")


def support_head():
    return new_page_head("Support Us | POI – Power of Interest UK",
                         "Help keep debate free. Support POI's Your Words. Your Way. campaign on Zeffy with zero platform fees, volunteer your time, or share our work.",
                         "support.html", "Support POI – Keep Debate Free")


NEW_HEADS = {"404": lambda: page404_head(), "motions": motions_head, "support": support_head}


build("index")
build("404")
build("motions", motion_parts())
build("support")
build("sessions")
build("about")
build("volunteering")
build("contact")
build("faq", faq_parts())
build("policies", policy_parts())
build("resources", resources_parts())
