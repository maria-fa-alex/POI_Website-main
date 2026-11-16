# POI Website – Resource Protection Rules

Every PDF added to the **Session Resources** page is one of two types. Choose the type
when adding the session to `_build/resources_data.py`.

## 1. Protected – presentation slides & branded materials

POI slide decks, branded curriculum and core training materials.
Add them with **`slides="…"`** in `resources_data.py`.

- **Viewer only:** opened inside the on-page viewer, never as a direct link.
- **No download buttons** on the card or in the viewer.
- **Protection measures:**
  - Privacy shield blurs the slides when the window loses focus or the tab is switched.
  - Text selection, copying, right-click and dragging are disabled.
  - Print and save shortcuts (`Ctrl/Cmd + P`, `Ctrl/Cmd + S`, `PrintScreen`) are blocked.
  - The viewer footer states that this is read-only student material.
  - A semi-transparent "POI UK • Confidential student material" watermark covers the slides.
  - Slides are drawn as high-resolution images so they read well on phones, tablets and computers.

## 2. Unrestricted – informal notes & motion guides

Motion walkthroughs, notes, reading guides and study handouts.
Add them with **`guide="…"`** (and a short `guide_name`) in `resources_data.py`.

- Opened in the same on-page viewer, but with full access:
  - A round download button on the card, plus download and open-in-new-tab buttons in the viewer.
  - Text selection and copying allowed.
  - No privacy shield, so students can take notes in another window.
  - Right-click, printing and saving allowed.
  - The viewer footer states that the material is free to read, print, copy and download.

## 3. If unsure

If it isn't clear whether a new file is official slides (protected) or informal notes
(unrestricted), **check with the POI team before publishing it.**

> Note: these protections discourage casual copying only. Anyone who knows a PDF's web
> address can still open it. For truly members-only files, host them behind real logins
> (e.g. a shared Google Drive folder or Cloudflare Access).
