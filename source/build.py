"""Builds the Thumbit website (thumbittaxis.com) into ./site.

Pages: home, privacy, terms, support (help + contact), delete-account, 404.
Plain HTML and CSS, no cookies, no scripts, no tracking.
"""
import html
import json
import os
import shutil
import sys

import markdown

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SRC, "..", "docs")
LOGO = SRC  # logo images are kept next to this script
EMAIL = "support@thumbittaxis.com"
DOMAIN = "thumbittaxis.com"

CSS = """
:root{--bg:#F8F8F5;--surface:#FFFFFF;--ink:#14213D;--muted:#5B6275;--line:#E4E4DE;
--amber:#FFB703;--amber-ink:#8A5300;--graphite:#0C0D10;--soft:#FFF4D6}
@media (prefers-color-scheme:dark){:root{--bg:#0C0D10;--surface:#16181D;--ink:#F5F5F4;
--muted:#A8A29E;--line:#2A2D34;--amber-ink:#FFC94D;--soft:#2A2310}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--amber-ink)}
a:focus-visible{outline:3px solid var(--amber);outline-offset:2px;border-radius:4px}
header{background:var(--graphite);color:#F5F5F4}
.bar{max-width:880px;margin:0 auto;padding:14px 16px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px;color:#F5F5F4;text-decoration:none;font-weight:800;font-size:20px;letter-spacing:-.01em}
.brand img{width:36px;height:36px;border-radius:9px}
nav{margin-left:auto;display:flex;gap:4px;flex-wrap:wrap}
nav a{color:#D6D3D1;text-decoration:none;padding:6px 10px;border-radius:8px;font-size:15px}
nav a:hover,nav a[aria-current=page]{background:#23262D;color:#fff}
main{max-width:760px;margin:0 auto;padding:32px 16px 56px}
h1{font-size:34px;line-height:1.15;letter-spacing:-.02em;margin:0 0 6px}
h2{font-size:22px;margin:36px 0 8px;letter-spacing:-.01em}
h3{font-size:18px;margin:24px 0 6px}
p,li{color:var(--ink)}
em{color:var(--muted)}
.lead{font-size:20px;color:var(--muted);margin:0 0 24px}
.table-wrap{overflow-x:auto;margin:12px 0 20px;border:1px solid var(--line);border-radius:12px;background:var(--surface)}
table{border-collapse:collapse;width:100%;min-width:520px;font-size:15px}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}
tr:last-child td{border-bottom:0}
th{background:var(--soft);font-weight:700}
.hero{text-align:center;padding:24px 0 8px}
.hero img{width:112px;height:112px;border-radius:26px;box-shadow:0 10px 30px rgba(0,0,0,.18)}
.hero h1{font-size:46px;margin-top:20px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin:28px 0}
.card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:18px}
.card h3{margin:0 0 4px}
.card p{margin:0;color:var(--muted);font-size:15px}
.cta{display:inline-block;background:var(--amber);color:#14213D;font-weight:800;text-decoration:none;padding:14px 22px;border-radius:14px;margin:6px}
.cta.secondary{background:transparent;color:var(--ink);border:1px solid var(--line)}
details{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:10px 0}
summary{cursor:pointer;font-weight:700}
details p{margin:10px 0 2px}
.note{background:var(--soft);border-radius:12px;padding:14px 16px;margin:16px 0}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:14px}
footer .bar{flex-direction:column;align-items:flex-start;gap:6px;padding:20px 16px 32px}
footer a{color:var(--muted)}
"""

NAV = [("/", "Home"), ("/support/", "Help"), ("/terms/", "Passenger Terms"), ("/privacy/", "Privacy")]


def page(path, title, body, description):
    links = "".join(
        f'<a href="{href}"{" aria-current=page" if href == path else ""}>{label}</a>' for href, label in NAV
    )
    full_title = "Thumbit – licensed local taxis, booked in a tap" if path == "/" else f"{title} – Thumbit"
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="theme-color" content="#0C0D10">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="https://{DOMAIN}/og-image.png">
<meta property="og:url" content="https://{DOMAIN}{path}">
<link rel="canonical" href="https://{DOMAIN}{path}">
<style>{CSS}</style>
</head>
<body>
<header><div class="bar">
<a class="brand" href="/"><img src="/thumbit-mark.png" alt="" width="36" height="36">Thumbit</a>
<nav aria-label="Main">{links}</nav>
</div></header>
<main>
{body}
</main>
<footer><div class="bar">
<div>Thumbit is a booking app run by Michael Binmore-May, trading as Thumbit. Journeys are provided by independent, licensed taxi and private hire firms.</div>
<div><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="/terms/">Passenger Terms</a> · <a href="/privacy/">Privacy Policy</a> · <a href="/delete-account/">Delete your account</a></div>
<div>© 2026 Thumbit</div>
</div></footer>
</body>
</html>
"""


def md(text):
    out = markdown.markdown(text, extensions=["tables", "sane_lists"])
    return out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")


def write(rel, content):
    dest = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w") as f:
        f.write(content)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    for name in ["favicon.png", "apple-touch-icon.png", "og-image.png", "thumbit-mark.png", "thumbit-icon-192.png"]:
        shutil.copy(os.path.join(LOGO, name), os.path.join(OUT, name))

    home = f"""
<section class="hero">
<img src="/thumbit-icon-192.png" alt="Thumbit app icon" width="112" height="112">
<h1>Thumbit</h1>
<p class="lead">Licensed local taxis, booked in a tap.</p>
<p><a class="cta" href="/support/">How it works</a><a class="cta secondary" href="mailto:{EMAIL}">Contact us</a></p>
<p><em>The Thumbit app for iPhone is coming soon to the App Store.</em></p>
</section>
<div class="cards">
<div class="card"><h3>Licensed local drivers</h3><p>Every trip is with a licensed local taxi or private hire firm.</p></div>
<div class="card"><h3>See your price first</h3><p>Fares use the official council tariff for your pickup area.</p></div>
<div class="card"><h3>Pay the driver</h3><p>Only a £1.50 booking fee is paid in the app. Pay your fare by cash or card.</p></div>
<div class="card"><h3>Safety built in</h3><p>Track your driver, share your trip and use Emergency SOS.</p></div>
</div>
"""
    write("index.html", page("/", "Home", home, "Book licensed local taxis in a tap with the Thumbit app."))

    for slug, title, desc in [
        ("privacy", "Privacy Policy", "How Thumbit collects, uses and protects your personal data."),
        ("terms", "Passenger Terms", "The terms that apply when you book a taxi with Thumbit."),
    ]:
        text = open(os.path.join(SRC, f"{slug}.md")).read()
        write(f"{slug}/index.html", page(f"/{slug}/", title, md(text), desc))

    faq = json.load(open(os.path.join(SRC, "faq.json")))
    items = "".join(
        f"<details><summary>{html.escape(q['q'])}</summary><p>{html.escape(q['a'])}</p></details>" for q in faq
    )
    support = f"""
<h1>Help</h1>
<p class="lead">Answers to common questions, and how to reach us.</p>
<h2>Contact us</h2>
<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a>. We aim to reply within 5 working days.</p>
<p>In the app you can also use <strong>Settings → Report a problem</strong>. For anything about a trip that's booked, open it in <strong>My bookings</strong> and tap the button to call the taxi firm.</p>
<div class="note"><strong>In an emergency, call 999.</strong> During a trip, the Emergency SOS button on your trip screen lets you call 999 or send a silent alert with your location.</div>
<h2>Questions</h2>
{items}
<h2>Your account</h2>
<p><a href="/delete-account/">How to delete your account</a> · <a href="/privacy/">Privacy Policy</a> · <a href="/terms/">Passenger Terms</a></p>
"""
    write("support/index.html", page("/support/", "Help", support, "Help with the Thumbit taxi booking app, and how to contact us."))

    delete = f"""
<h1>Delete your account</h1>
<p class="lead">You can delete your Thumbit account at any time.</p>
<h2>In the app</h2>
<ol>
<li>Open the Thumbit app and tap <strong>Settings</strong>.</li>
<li>Tap <strong>Delete my account</strong>.</li>
<li>Tap <strong>Yes, delete my account</strong> to confirm.</li>
</ol>
<h2>By email</h2>
<p>If you can't use the app, email <a href="mailto:{EMAIL}?subject=Delete%20my%20account">{EMAIL}</a> from the email address on your account, or tell us your mobile number, and we'll delete it for you.</p>
<h2>What happens next</h2>
<ul>
<li>Your account, saved places, family profiles and trusted contacts are erased after 30 days. Sign in before then if you change your mind.</li>
<li>Please cancel any upcoming bookings first.</li>
<li>Booking and payment records we must keep by law are kept for 6 years, then deleted. See our <a href="/privacy/">Privacy Policy</a>.</li>
</ul>
"""
    write("delete-account/index.html", page("/delete-account/", "Delete your account", delete, "How to delete your Thumbit account and data."))

    write("404.html", page("/404", "Page not found", '<h1>Page not found</h1><p class="lead">Sorry, that page doesn\'t exist.</p><p><a class="cta" href="/">Go to the home page</a></p>', "Page not found"))
    write("CNAME", f"{DOMAIN}\n")
    write(".nojekyll", "")
    print("built", OUT)


if __name__ == "__main__":
    main()
