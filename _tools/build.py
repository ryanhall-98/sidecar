#!/usr/bin/env python3
"""Build the Sidecar marketing site.

Each page body lives in _src/<name>.html and starts with a metadata block:

    <!--
    title: Page title
    description: Meta description
    nav: platform
    -->

Run from the repo root:   python3 _tools/build.py
Output: <name>.html at the repo root (what GitHub Pages serves).
Folders that start with "_" are not published by GitHub Pages.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_src"
SITE = "https://sidecarhq.cc"

PORTAL_SIGNUP = "https://portal.sidecarhq.cc/onboard"
PORTAL_LOGIN = "https://portal.sidecarhq.cc/"
SMS_DEMO = "sms:+18448400637?&amp;body=DEMO"
EMAIL = "ryan@sidecarhq.cc"

MARK = ('<svg class="brand-mark" viewBox="0 0 30 22" aria-hidden="true">'
        '<rect x="0" y="0" width="17" height="22" rx="3" fill="#29252D"/>'
        '<rect x="19.5" y="9" width="10.5" height="13" rx="2.5" fill="#7660A8"/></svg>')


def icon(name, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="assets/icons.svg#i-{name}"/></svg>'


NAV = [
    ("product", "Product"),
    ("inventory", "Inventory"),
    ("marketing", "Marketing"),
    ("integrations", "Integrations"),
    ("customers", "Customers"),
    ("pricing", "Pricing"),
]


def nav(active):
    def cur(key):
        return ' aria-current="page"' if key == active else ""

    links = "".join(f'<li><a class="nav-link" href="{k}.html"{cur(k)}>{label}</a></li>' for k, label in NAV)
    mobile = "".join(f'<li><a href="{k}.html">{label}</a></li>' for k, label in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-nav">
  <div class="wrap nav-inner">
    <a class="brand" href="index.html" aria-label="Sidecar home">{MARK}<span class="brand-word">Sidecar</span></a>
    <nav aria-label="Main">
      <ul class="nav-links">{links}</ul>
    </nav>
    <div class="nav-actions">
      <a class="login" href="{PORTAL_LOGIN}">Log in</a>
      <a class="btn btn-primary btn-sm" href="{PORTAL_SIGNUP}">Start free trial</a>
    </div>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-panel" aria-label="Open menu"><svg class="ic" aria-hidden="true"><use href="assets/icons.svg#i-menu"/></svg></button>
  </div>
  <div class="mobile-panel" id="mobile-panel">
    <ul>
      {mobile}
      <li><a href="about.html">About</a></li>
    </ul>
    <div class="actions">
      <a class="btn btn-primary" href="{PORTAL_SIGNUP}">Start free trial</a>
      <a class="btn btn-quiet" href="{PORTAL_LOGIN}">Log in</a>
      <a class="btn btn-quiet" href="{SMS_DEMO}">Text DEMO to (844) 840-0637</a>
    </div>
  </div>
</header>"""


CLOSER = f"""<section class="closer" aria-labelledby="closer-h">
  <div class="wrap closer-inner">
    <h2 class="display" id="closer-h">Spend less time managing the details.</h2>
    <div class="closer-side">
      <p>Let Sidecar help you understand your business and take care of the work that keeps it running.</p>
      <div class="actions">
        <a class="btn btn-light" href="{PORTAL_SIGNUP}">Start your free trial</a>
      </div>
      <p class="closer-fine">7-day free trial, no credit card. Or <a href="{SMS_DEMO}">text DEMO to (844) 840-0637</a> and try it now.</p>
    </div>
  </div>
</section>"""

FOOTER = f"""<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-about">
        <a class="brand" href="index.html" aria-label="Sidecar home">{MARK}<span class="brand-word">Sidecar</span></a>
        <p>The operations platform for bars and restaurants. Based in New York City.</p>
      </div>
      <div>
        <h2>Product</h2>
        <ul>
          <li><a href="product.html">Product</a></li>
          <li><a href="inventory.html">Inventory</a></li>
          <li><a href="marketing.html">Marketing</a></li>
          <li><a href="integrations.html">Integrations</a></li>
          <li><a href="customers.html">Customers</a></li>
          <li><a href="pricing.html">Pricing</a></li>
        </ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="terms.html">Terms of Service</a></li>
          <li><a href="privacy.html">Privacy Policy</a></li>
        </ul>
      </div>
      <div>
        <h2>Try Sidecar</h2>
        <ul>
          <li><a href="{PORTAL_SIGNUP}">Start a free trial</a></li>
          <li><a href="{PORTAL_LOGIN}">Log in</a></li>
          <li><a href="{SMS_DEMO}">Text DEMO to (844) 840-0637</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-base">
      <span>&copy; <span id="year">2026</span> Sidecar</span>
      <span>Product views on this site use sample data.</span>
    </div>
  </div>
</footer>"""


def head(meta, name):
    path = "" if name == "index" else f"{name}.html"
    canonical = f"{SITE}/{path}"
    title = meta["title"]
    desc = meta["description"]
    robots = '\n<meta name="robots" content="noindex">' if meta.get("noindex") else ""
    if name == "404":
        # GitHub Pages serves 404.html at any missing path; anchor relative links at the root.
        robots += '\n<base href="/">'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">{robots}
<meta name="theme-color" content="#F3F1ED">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Sidecar">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/newsreader.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/geist.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css">
<script src="assets/site.js" defer></script>
</head>"""


META_RE = re.compile(r"^\s*<!--(.*?)-->", re.S)


def parse(text):
    m = META_RE.match(text)
    meta = {}
    if m:
        for line in m.group(1).strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text.strip()


def expand(body):
    # {{icon:name}} shortcuts and shared link tokens
    body = re.sub(r"\{\{icon:([a-z-]+)\}\}", lambda m: icon(m.group(1)), body)
    return (body.replace("{{SIGNUP}}", PORTAL_SIGNUP)
                .replace("{{LOGIN}}", PORTAL_LOGIN)
                .replace("{{SMS}}", SMS_DEMO)
                .replace("{{EMAIL}}", EMAIL)
                .replace("{{MARK}}", MARK)
                .replace("{{CLOSER}}", CLOSER))


def build():
    pages = sorted(SRC.glob("*.html"))
    for p in pages:
        meta, body = parse(p.read_text())
        name = p.stem
        html = "\n".join([
            head(meta, name),
            f'<body data-page="{name}">',
            nav(meta.get("nav", "")),
            '<main id="main">',
            expand(body),
            "</main>",
            FOOTER,
            "</body>",
            "</html>",
            "",
        ])
        (ROOT / f"{name}.html").write_text(html)
        print(f"built {name}.html")


if __name__ == "__main__":
    build()
