# Ocmand Construction website - playbook

This repository is the live website of Ocmand Construction Co., LLC: https://ocmandconstruction.com

Cloudflare Pages publishes the `main` branch on its own. A push to `main` is live in about a minute, so
**every push to `main` is publishing.** There is no site editor and nothing for Preston to paste anywhere.

On the Ocmand team this is Pixel's work (`website`), checked by Megaphone (`marketing`). Preston Ocmand, the
project manager, approves everything before it goes live. He is not a coder: talk to him in plain words about
what changed on the site, never about files, branches or commits.

## The rule that comes first
**Nothing goes live without Preston's OK.** Make the change, run the check, show him a preview, and push only
after he says to. If he asks for a change and says to publish it in the same breath, that is his OK.

## How the site is put together
- **The repository root is the published site.** Every file there is public at the same address.
- **`_source/build.py` writes every `.html` page**, plus `sitemap.xml`, `robots.txt` and `_redirects`. All page
  text lives in that one file. Never edit a generated `.html` by hand: the next build overwrites it.
- **`styles.css` and `site.js`** in the root are hand-written and edited directly.
- **Images** in the root: `project-NN.jpg` with a half-size `project-NN-800.jpg`, the Bangkok Thai rendering
  (`bangkok-thai-rendering*.jpg`), `og.jpg` (the picture shown when the link is texted or posted), `logo.svg`
  (one file holding three logo layouts: `mark`, `lockup`, `stacked`), `favicon.svg`, `apple-touch-icon.png`.
  The font is `archivo.woff2`, served from the site itself.
- **`_source/` and this file are not part of the public site**: `_redirects` sends both to the home page.
- **Pages:** home, `services` (Markets) and six market pages, `projects`, `approach` (How we work), `about`,
  `contact`, and `404`. Addresses have no `.html` on the live site.
- **Outside services, all already set up:** the two forms on the Contact page send to jobs@ocmandconstruction.com
  through Web3Forms; Google Analytics is in every page head; the sitemap is submitted in Google Search Console.
  None of these need attention after a normal edit.

## Making a change
1. Pull the latest `main` first. Another chat may have changed the site.
2. Edit `_source/build.py` (text, projects, pages), `styles.css` or `site.js`.
3. Run `bash _source/check.sh`. It rebuilds the site, serves it locally the way Cloudflare does, and checks every
   page at seven screen widths plus the menus, photo viewer, forms, redirects and the 404 page.
   It must end with `ISSUES (0)`.
4. Look at what changed, on a desktop and a phone width, with the local server running:
   `python3 _source/serve.py . 8812 &` then
   `node _source/shot.js http://127.0.0.1:8812/about /tmp/about.png 1440 900 full` (and `390 844` for a phone).
5. Show Preston: `python3 _source/make_preview.py` builds a click-through copy of the whole site outside the
   repository and prints how to publish it as an Artifact. For a small text change, a screenshot is enough.
6. When he says to publish: commit and push to `main`.
7. Confirm it on the live site. The cloud shell usually cannot reach the site, so use web fetch or a browser
   tool and add `?t=<anything>` to the address to get past caching. Then tell Preston, in a sentence or two,
   what is now different on the site.

A rebuild with no edits must leave `git status` clean. If it does not, someone edited a generated file by hand:
move that change into `build.py` before doing anything else.

## Common jobs
**Add a completed project.** Needed from Megaphone's project sheet or from Preston: the project name as it
should read, the town, the type of building, one good exterior photo that Ocmand took, and that the owner is
fine being named.
1. `python3 _source/add_photo.py <photo> <number>` - use the next unused number, 15 or higher (retired numbers
   are not reused, so an old cached picture can never show up under a new project).
2. Add a line to the `P` list near the top of `build.py`: number, name, location, type, `'commercial'`, and a
   plain description of the photo for screen readers. The order of `P` is the order on the Projects page.
3. Optional: show it on the home page ("Completed work" uses four photos) or under a market page's
   "Related projects" (the three numbers at the end of each `service(...)` call).

**Change the featured project** (currently the Bangkok Thai center): the `feature()` function in `build.py`.
When the building is finished, replace the rendering with Ocmand's own photos.

**Change wording on a page:** find the page's block in `build.py` (each starts with a `# ====== NAME ======`
line) and edit the text there. Bump `LASTMOD` at the top when page content changes.

**Add a page:** add a `page(...)` call, a link to it in `header()` or `FOOT`, and its address to the `pages` list
at the bottom of `build.py` so it lands in the sitemap and the automated check.

**Retire a page:** remove it, delete its `.html`, and add a line to the `_redirects` text at the bottom of
`build.py` so the old address forwards somewhere sensible.

`project-04.jpg` in the root is an unused commercial photo, waiting on its project name and town.

## What Preston wants the site to be
These are his directions. They outrank general web advice.
- **Commercial work only.** Nothing about houses or residential work anywhere.
- **Email only.** No phone numbers on the site. The one contact address is jobs@ocmandconstruction.com.
- **No chat bot** or other widgets.
- **No personal names or staff bios on the About page.** It speaks as the family and the company: family owned,
  why that is good for clients, why they care. Ask before adding anyone's name anywhere.
- **The license number appears once,** in the small print at the bottom of each page.
- **General, not local.** The company serves Louisiana; the site is not positioned around one city or region.
  A project's own town is fine.
- **Wording is general and confident.** Say that Ocmand plans carefully, checks its work and keeps its
  schedules. Do not list step-by-step procedures or oddly specific technical checks; he called that forced.
- **It should look established and need no upkeep.** Leave out anything that goes stale: dates, "under
  construction", "opening in 2027", "currently", exact year counts ("more than 35 years", not "36 years").
- **Just enough to sound legitimate.** Short pages. Do not pad.
- **The logo is final:** the stepped "OCC" with the company name. Use `logo.svg`; never redraw or restyle it.

## Team rules that also apply here
- **Nothing invented.** No made-up reviews, statistics, awards, client lists or project details. Project
  facts come from Preston or the job's own records. Leave a thing out before guessing at it.
- **Other contractors' sites are for inspiration only** (Preston's direction). Never copy their wording or layout.
- **Pictures are Ocmand's own.** No photos from news sites, listings or other companies. An architect's
  rendering needs the architect's permission and a credit line under it. No recognizable faces without
  permission. Name an owner only with the owner's permission.
- **Never write anything negative** about an architect, owner or subcontractor.

## Look and build
- Navy `#0c2148` and deep navy `#071632`, a thin red rule `#b4202a`, light grey `#eef0f3`, white.
- One typeface, Archivo. Headings are uppercase and condensed; body text is regular width.
- Sections alternate white, light grey and navy. Photos carry a small three-part caption in the style of a
  drawing title block (Project / Location / Type). Reuse the existing section patterns in `build.py` before
  making a new one, so the pages keep reading as one site.
- Plain HTML, CSS and a small script. No frameworks, no build service, no outside scripts beyond Analytics and
  the form service, no outside fonts.

## Do not
- Do not push to `main` to "try something". Use the local server and the preview.
- Do not upload files through the GitHub website; that is how duplicates like `index (1).html` appear.
- Do not rename or remove a page address without a redirect.
- Do not put anything private in this repository. It is public.
- Do not regenerate the logo (`_source/logo/`) unless Preston asks for a logo change.
