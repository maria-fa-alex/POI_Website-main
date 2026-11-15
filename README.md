# POI – Power of Interest UK · Website

The website for **POI – Power of Interest**, live at **https://poi.org.uk**.
It is a plain static site (HTML, CSS and JavaScript – no framework) hosted on **GitHub Pages**.

This file explains how the site is organised, how to change things safely, how to
publish to GitHub Pages, and what still needs doing.

> Detailed "how do I change X" steps for the build tools are in [`_build/README.md`](_build/README.md).

---

## Contents

1. [How the site is organised](#1-how-the-site-is-organised)
2. [Preview the site on your computer](#2-preview-the-site-on-your-computer)
3. [Making changes](#3-making-changes)
4. [Where every setting lives](#4-where-every-setting-lives)
5. [Publishing to GitHub Pages](#5-publishing-to-github-pages)
6. [To-do list – what still needs doing](#6-to-do-list--what-still-needs-doing)
7. [Regular maintenance](#7-regular-maintenance)
8. [Resource protection rules](#8-resource-protection-rules)
9. [If something goes wrong](#9-if-something-goes-wrong)

---

## 1. How the site is organised

```
POI_Website-main-main/
├── index.html            Home
├── about.html            Our Story (mission, founders, board)
├── sessions.html         Sessions + student sign-up form (#sign-up)
├── resources.html        Members' Session Resources (password gate + slide viewer)
├── motions.html          Motion Bank + 15-minute prep timer
├── volunteering.html     Volunteer roles + application form (#apply)
├── support.html          Support Us (explains donations, links to Zeffy)
├── faq.html              FAQs
├── policies.html         Policies + safeguarding contact pop-up
├── contact.html          Contact form
├── 404.html              "Page not found" page (GitHub Pages uses it automatically)
│
├── assets/
│   ├── css/styles.css    ALL styling (colours, layout, light/dark mode)
│   ├── js/main.js        ALL site behaviour (menu, theme, forms, timer, local time…)
│   ├── js/pdf*.js        PDF viewer library used on the Resources page
│   ├── fonts/            Sora font (+ licence)
│   ├── images/           Logos, photos, illustrations, icons, share-card.jpg
│   └── calendar/         poi-sunday-workshop.ics ("Add to calendar" file)
├── docs/
│   ├── slides/           Session slide decks + motion walkthrough PDFs
│   └── policies/         Policy PDFs
│
├── _build/               Tools that generate the .html pages + RESOURCE_RULES.md (NOT published)
├── CNAME                 Custom domain for GitHub Pages: poi.org.uk  – do not delete
├── robots.txt            Search-engine rules (hides resources.html and slides)
├── sitemap.xml           Page list for search engines
└── _config.yml           Tells GitHub Pages which notes files not to publish
```

**Important:** the `.html` pages are *generated* by `_build/build.py`. If you edit an
`.html` page directly, the change will be lost the next time someone rebuilds.
Edit the files in `_build/` instead, then rebuild (see section 3).

The original, pre-redesign files are backed up outside this folder in
`Documents/POI/_original_backup/` (not part of the website).

---

## 2. Preview the site on your computer

You need **Python 3**. From the `POI_Website-main-main` folder run:

```
python -m http.server 8765
```

Then open **http://localhost:8765** in a browser. Press `Ctrl + C` to stop.

Things that only work on the live site: the 404 page, the `.ics` calendar file
opening straight in a calendar app, link previews, and visitor statistics.

---

## 3. Making changes

### The golden rule
1. Edit the right file (see the table below).
2. Rebuild: `python _build/build.py` (run from `POI_Website-main-main`).
3. Preview locally (section 2).
4. Publish (section 5).

### Quick reference

| I want to… | Edit this | Then |
|---|---|---|
| Change wording on a page | `_build/templates/<page>.body.html` | rebuild |
| Change the menu, header or footer | `NAV`, `header()`, `FOOTER` in `_build/build.py` | rebuild |
| Add a session to **Resources** | Put PDFs in `docs/slides/`, add an entry to `_build/resources_data.py` | rebuild |
| Add a motion to the **Motion Bank** | `MOTION_BANK` in `_build/build.py` | rebuild |
| Change an FAQ answer | `_build/source/faq.html` (the visible answer **and** the matching text in the `FAQPage` data near the top) | rebuild |
| Change policy text / add a policy PDF | `_build/source/policies.html` + PDF in `docs/policies/` | rebuild |
| Change the sign-up form | `_build/templates/signup.partial.html` | rebuild |
| Change the volunteer form | `_build/templates/volunteer-apply.partial.html` | rebuild |
| Change colours, spacing, fonts | `assets/css/styles.css` | bump `VER` in `build.py`, rebuild |
| Change behaviour (menu, timer, forms…) | `assets/js/main.js` | bump `VER` in `build.py`, rebuild |
| Change a page's Google title/description | the `<head>` of `_build/source/<page>.html` (for motions/support/404: `build.py`) | rebuild |
| Replace an image | overwrite the file in `assets/images/` with the **same name** | — |
| Change the link-preview image | `_build/make_share_card.py` | `python _build/make_share_card.py` |
| Change the "Add to calendar" file | `_build/make_ics.py` **and** `GCAL` in `build.py` | `python _build/make_ics.py`, rebuild |
| Change the Resources password | see [section 9](#changing-the-resources-password) | rebuild |

**Why bump `VER`?** Browsers keep old copies of `styles.css` and `main.js`. Raising
`VER` (e.g. `3.1` → `3.2`) in `_build/build.py` and rebuilding makes every visitor
load the new version.

---

## 4. Where every setting lives

### Session times (currently Sundays 9:00–9:30 AM UK time)
If the time ever changes, update **all** of these, then rebuild:

| Place | File |
|---|---|
| Home hero label + pathway step | `_build/templates/index.body.html` (text **and** `data-uk-start` / `data-uk-end`) |
| Sessions "Learn" card + pathway | `_build/templates/sessions.body.html` (text **and** `data-uk-*`) |
| Sign-up section + checkbox | `_build/templates/signup.partial.html` (text **and** `data-uk-*`) |
| Volunteer availability option | `_build/templates/volunteer-apply.partial.html` |
| FAQ answers | `FAQ_FIXES` in `_build/build.py` and `_build/source/faq.html` |
| Google event data | `weekly_event()` in `_build/build.py` |
| Google Calendar button | `GCAL` in `_build/build.py` |
| Apple/Outlook calendar file | `_build/make_ics.py` (then run it) |

The `data-uk-start="09:00"` values drive the automatic "That's 4:00 AM in New York"
conversion – keep them in 24-hour UK time. `data-weekday="0"` means Sunday.

In-person Oxford sessions: Wednesdays 16:30–18:00, in `_build/templates/sessions.body.html`.

### "Starting 2027" (in-person Oxford sessions)
When exact dates are confirmed, update the wording in:
`index.body.html`, `sessions.body.html`, `signup.partial.html`, `volunteer-apply.partial.html`,
`support.body.html`, the footer mailing-list text in `build.py`, and the FAQ text in `FAQ_FIXES`.
Also update the in-person event in `_build/source/sessions.html` (its `startDate`) and remove the
`"sessions"` entry in `HEAD_FIXES` in `build.py` that marks it as *postponed*.

### Links, accounts and contact details

| Setting | Where |
|---|---|
| Formspree form address (all forms) | `FORMSPREE` in `_build/build.py` |
| Zeffy donation link | `DONATE` in `_build/build.py` (+ fallback in `assets/js/main.js`) |
| LinkedIn / Instagram | `SOCIALS` in `_build/build.py` |
| Contact emails | `_build/templates/contact.body.html`, `about.body.html`, `FOOTER` in `build.py` |
| Safeguarding lead pop-up | `_build/templates/policies.body.html` |
| Visitor statistics (GoatCounter) | `GOATCOUNTER_CODE` in `assets/js/main.js` |
| Copyright year | `FOOTER` in `_build/build.py` |
| Company number / address text | `FOOTER` in `_build/build.py` and page `<head>` data in `_build/source/` |
| Asset version (cache busting) | `VER` in `_build/build.py` |

---

## 5. Publishing to GitHub Pages

### One-time setup (check these in the repository on GitHub)
- **Settings → Pages → Source:** "Deploy from a branch", branch `main` (or your default), folder **`/ (root)`**.
- **Custom domain:** `poi.org.uk` – this is stored in the `CNAME` file. Never delete or rename `CNAME`.
- **Enforce HTTPS:** ticked.
- The repository root must be the **contents** of `POI_Website-main-main` (where `index.html` is).
- **Do not add a `.nojekyll` file.** GitHub Pages' default processing is what keeps
  `_build/` and the notes files private. With `.nojekyll`, `_build/` would be published.

### Every time you publish – checklist
- [ ] Made the change in `_build/` (or `assets/`), not directly in a generated `.html` page
- [ ] Ran `python _build/build.py` with no errors
- [ ] If CSS/JS changed: bumped `VER` in `build.py` before building
- [ ] Previewed locally: checked the changed page in light **and** dark mode and at phone width
- [ ] New page? Added it to `sitemap.xml` and the menu/footer if needed
- [ ] New PDF? It's in `docs/slides/` or `docs/policies/` and the link works
- [ ] Committed **both** the `_build/` changes and the regenerated `.html` files
- [ ] Pushed – GitHub Pages usually updates within 1–2 minutes
- [ ] Checked the live page (hard refresh: `Ctrl + Shift + R`)

### After a big change
- **Link previews** (WhatsApp/LinkedIn/Facebook) are cached by those sites. Refresh them with
  LinkedIn Post Inspector and the Facebook Sharing Debugger.
- **Search engines:** submit `https://poi.org.uk/sitemap.xml` in Google Search Console.

---

## 6. To-do list – what still needs doing

These need a person (an account, a decision or content). Tick them off as you go.

### Forms & data
- [ ] **Test every form on the live site** (sign-up, volunteer, contact, mailing list) and confirm
      they arrive in Formspree. The first submission from a new page may trigger a Formspree
      confirmation email – check spam.
- [ ] **Formspree limits:** the free plan allows about 50 submissions a month *across all forms*.
      Upgrade or create separate forms if sign-ups grow (then update `FORMSPREE` in `build.py`).
- [ ] **Update the Privacy / GDPR policy** to cover the new data collected: student sign-ups
      (age, country, time zone, school year), parent/guardian details for under-13s,
      volunteer applications, and the mailing list.
- [ ] **Compare the new volunteer form with the old Google Form** questions (the old form needed a
      sign-in to view) and add anything missing.
- [ ] Decide what happens to existing sign-ups still in the old Google Forms.

### Accounts to set up
- [ ] **Visitor statistics:** create a free GoatCounter account (no cookies, no banner needed) and
      put the code in `GOATCOUNTER_CODE` in `assets/js/main.js`.
- [ ] **Mailing list tool** (e.g. Buttondown or Mailchimp) to actually send newsletters. Until then,
      addresses are collected in Formspree and need copying across by hand.

### Security
- [ ] **The Resources password is not real security.** It stops casual copying only – anyone with a
      PDF's address can open it, and the check runs in the visitor's browser. If slides must be
      truly members-only, move them behind real logins (e.g. a shared Google Drive folder,
      Cloudflare Access, or a host with password protection). GitHub Pages cannot do this itself.

### Content
- [ ] Confirm the **"What your donation helps with"** wording on the Support page.
- [ ] Add **dates for the 2027 Oxford sessions** when known (see section 4).
- [ ] Replace the **"2nd Draft" policy PDFs** in `docs/policies/` with final versions when approved
      (keep the same filenames, or update the links in `_build/source/policies.html`).
- [ ] Add **student or parent quotes** and **session photos** (with consent under the photography policy).
- [ ] Consider adding **session recordings** to Resources (e.g. unlisted YouTube links).
- [ ] When a weekend session is skipped, tell students by email/social media (the site no longer
      shows a "next session" line).

---

## 7. Regular maintenance

**After every session**
- Add the slides/guide PDFs and a `resources_data.py` entry; add the motion to `MOTION_BANK`.
- Ask if unsure whether a file is protected slides or an unrestricted guide (section 8).
- Rebuild and publish.

**Every few weeks**
- Rebuild once (`python _build/build.py`) so Google's "next session" date stays current.

**Each term**
- Check the FAQ, session times and the 2027 Oxford wording are still correct.

**Each January**
- Update the copyright year in `FOOTER` (`_build/build.py`), rebuild, publish.

---

## 8. Resource protection rules

(Full rules: [`_build/RESOURCE_RULES.md`](_build/RESOURCE_RULES.md).)

| Type | In `resources_data.py` | Behaviour |
|---|---|---|
| POI-branded slide decks | `slides=` | **Protected:** in-page viewer only, watermark, no download, copy/print blocked |
| Motion walkthroughs, notes, guides | `guide=` | **Unrestricted:** viewer + download button; reading, printing, copying allowed |

If it's unclear which a new file is, **ask before publishing**.

---

## 9. If something goes wrong

**A change disappeared after rebuilding** – it was made directly in a generated `.html` file.
Make it again in `_build/` and rebuild.

**`build.py` stops with an `AssertionError`** – it checks its inputs on purpose. The message names
what it couldn't find, usually a PDF listed in `resources_data.py` that isn't in `docs/slides/`, or
text in `_build/source/` that was edited and no longer matches.

**Styles or scripts look old on the live site** – bump `VER` in `build.py`, rebuild, publish, then
hard-refresh (`Ctrl + Shift + R`).

**The custom domain stopped working** – check `CNAME` still contains `poi.org.uk` and the domain
is still set under Settings → Pages.

**Something is broken and you need the old version** – restore the files from your previous GitHub
commit, or from `Documents/POI/_original_backup/` for the pre-redesign site.

### Changing the Resources password
The page stores a SHA-256 *fingerprint* of the password, not the password itself.
1. Create the fingerprint of the new password:
   `python -c "import hashlib; print(hashlib.sha256('NEW PASSWORD'.encode()).hexdigest())"`
2. In `_build/source/resources.html`, replace the value of `const HASH = '…'` with the new one.
3. Rebuild and publish, then share the new password with students in the session chat.
