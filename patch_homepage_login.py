"""Adds a Log in link to sidecarhq.cc (desktop nav + phones). Run from ~/Desktop/FIles/sidecar."""
import pathlib, sys

p = pathlib.Path("index.html")
s = p.read_text()

if "nav-login" in s:
    print("Already patched."); sys.exit(0)

edits = [
    # Desktop: Log in sits next to Start Free Trial
    ('      <a href="https://portal.sidecarhq.cc/onboard" class="nav-cta">Start Free Trial</a>\n    </div>',
     '      <a href="https://portal.sidecarhq.cc" class="nav-login">Log in</a>\n'
     '      <a href="https://portal.sidecarhq.cc/onboard" class="nav-cta">Start Free Trial</a>\n    </div>\n'
     '    <a href="https://portal.sidecarhq.cc" class="nav-login-m">Log in</a>'),
    # Styles
    (".nav-links a:hover { color:var(--text); }",
     ".nav-links a:hover { color:var(--text); }\n"
     ".nav-links a.nav-login { color:var(--text); font-weight:600; }\n"
     ".nav-login-m { display:none; color:var(--text); text-decoration:none; font-size:14px; font-weight:600; padding:8px 14px; border:1px solid rgba(255,255,255,0.18); border-radius:8px; }"),
    # Phones: nav links are hidden, so show the standalone Log in button
    ("  .nav-links { display:none; }",
     "  .nav-links { display:none; }\n  .nav-login-m { display:inline-block; }"),
]

for old, new in edits:
    if s.count(old) != 1:
        print(f"STOP: expected 1 match, found {s.count(old)}:\n  {old[:80]}"); sys.exit(1)
    s = s.replace(old, new)

p.write_text(s)
print("Patched index.html")
