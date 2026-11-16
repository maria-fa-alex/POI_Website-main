# POI website – build tools

The website itself is plain HTML in the folder above this one. These tools rebuild
those pages so the shared parts (header, menu, footer) stay identical everywhere.

This folder is **not published**: GitHub Pages skips folders that start with `_`.

For the big picture (publishing to GitHub Pages and where every setting lives)
see the main [README](../README.md).

You need Python 3 (and Pillow only for the share image: `pip install pillow`).
Run every command from the website folder (`POI_Website-main-main`).

## Rebuild all pages

```
python _build/build.py
```

Rebuilding overwrites the `.html` pages, so make changes in `_build/` (not in the
built pages), then rebuild.

## Common jobs

| I want to… | Edit | Then run |
|---|---|---|
| Add a new session to **Resources** | Put the PDFs in `docs/slides/`, add an entry at the bottom of `_build/resources_data.py` | `python _build/build.py` |
| Change a page's wording | `_build/templates/<page>.body.html` | `python _build/build.py` |
| Change the **menu, header or footer** | `NAV`, `header()` and `FOOTER` in `_build/build.py` | `python _build/build.py` |
| Add a motion to the **Motion Bank** | `MOTION_BANK` in `_build/build.py` | `python _build/build.py` |
| Change the sign-up / volunteer form links | `FORM` / `VOL_FORM` in `build.py` (the forms themselves are Google Forms) | `python _build/build.py` |
| Change FAQ answers or policy text | `_build/source/faq.html`, `_build/source/policies.html` | `python _build/build.py` |
| Change the weekly calendar file | `_build/make_ics.py` | `python _build/make_ics.py` |
| Change the link-preview image | `_build/make_share_card.py` | `python _build/make_share_card.py` |

Styles live in `assets/css/styles.css` and scripts in `assets/js/main.js`. Edit those
directly; no rebuild needed. After changing them, bump `VER` in `build.py` and
rebuild so visitors' browsers load the new versions.

## Resource protection rules (full version: `RESOURCE_RULES.md`)

- `slides` in `resources_data.py` = POI-branded slide decks → **protected**
  (viewer only, watermark, no download).
- `guide` = motion walkthroughs / notes → **unrestricted** (read, print, download).
- If unsure which a new file is, ask before publishing.

## Other notes

- The online workshop's Google event data uses the next Sunday from the day you
  build, so rebuilding now and then keeps it fresh.
- Visitor statistics are off until a GoatCounter code is added at
  `GOATCOUNTER_CODE` in `assets/js/main.js`.
- Student sign-up and volunteer applications use Google Forms (`FORM`, `VOL_FORM` in `build.py`).
- The contact page links to the Google Form in `CONTACT_FORM` in `build.py` (empty = email button).
- No mailing list for now; if one is added later it must be for ages 16+.
