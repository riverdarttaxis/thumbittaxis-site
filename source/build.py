"""Builds the ThumbiT website (thumbittaxis.com) into ./site.

Pages: home, executive, privacy, terms, support (help + contact), delete-account, app, 404.
Plain HTML and CSS, no cookies, no tracking. The only script is on /app (the QR code on the drivers'
window stickers points there): it sends an iPhone to the App Store and an Android phone to Google
Play, using nothing but the phone's type. No cookies, nothing stored or sent anywhere.
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

# Where /app sends people (the QR code on the window stickers). Fill in each store link once the
# app is live there; while one is empty, those phones get the website booking page instead.
APP_STORE_URL = "https://apps.apple.com/gb/app/thumbit-taxis/id6822330519"
PLAY_STORE_URL = ""  # "https://play.google.com/store/apps/details?id=com.thumbit.passenger" once live
BOOK_ONLINE_URL = "https://dispatch.thumbittaxis.com/book"

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
.brand img{height:40px;width:auto;display:block}
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
.hero img{width:320px;max-width:100%;height:auto}
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
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:14px}
footer .bar{flex-direction:column;align-items:flex-start;gap:6px;padding:20px 16px 32px}
footer a{color:var(--muted)}
"""

NAV = [("/", "Home"), ("/executive/", "Executive"), ("/support/", "Help"), ("/terms/", "Passenger Terms"), ("/privacy/", "Privacy")]


def page(path, title, body, description):
    links = "".join(
        f'<a href="{href}"{" aria-current=page" if href == path else ""}>{label}</a>' for href, label in NAV
    )
    full_title = "ThumbiT – licensed local taxis, booked in a tap" if path == "/" else f"{title} – ThumbiT"
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
<a class="brand" href="/"><img src="/thumbit-logo-on-dark.png" alt="ThumbiT" width="141" height="40"></a>
<nav aria-label="Main">{links}</nav>
</div></header>
<main>
{body}
</main>
<footer><div class="bar">
<div>ThumbiT is a booking app run by Michael Binmore-May, trading as ThumbiT. Journeys are provided by independent, licensed taxi and private hire firms.</div>
<div><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="/terms/">Passenger Terms</a> · <a href="/privacy/">Privacy Policy</a> · <a href="/delete-account/">Delete your account</a></div>
<div>© 2026 ThumbiT</div>
</div></footer>
</body>
</html>
"""


# The Executive page has its own look (dark, with a serif headline), so it is a whole page of its
# own rather than a body dropped into page(). Still plain HTML and CSS: no scripts, no cookies, no
# fonts or pictures fetched from anywhere else. The car is drawn here, not a photograph.
EXEC_CSS = """
:root{--night:#0E1626;--ink:#14213D;--champagne:#D9C7A0;--ivory:#F3EEE3;--slate:#9AA3B5;--rule:#2A3550;--amber:#FFB703}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--night);color:var(--ivory);font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--champagne)}
a:focus-visible{outline:2px solid var(--amber);outline-offset:3px;border-radius:4px}
.wrap{max-width:1040px;margin-inline:auto;padding-inline:24px}
.top{display:flex;align-items:center;gap:16px;flex-wrap:wrap;padding-block:18px}
.top img{height:36px;width:auto;display:block}
.top nav{margin-left:auto;display:flex;gap:2px;flex-wrap:wrap}
.top nav a{color:var(--slate);text-decoration:none;padding:6px 10px;border-radius:8px;font-size:15px}
.top nav a:hover,.top nav a[aria-current=page]{color:var(--ivory)}
h1,h2,h3{font-family:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;font-weight:400;letter-spacing:-.01em;margin:0}
h1{font-size:clamp(40px,7.4vw,84px);line-height:1.02;max-width:13ch}
h2{font-size:clamp(28px,4vw,42px);line-height:1.1;max-width:20ch}
h3{font-size:24px;line-height:1.2}
p{margin:0}
.hero{padding-block:clamp(40px,9vw,112px) 0}
.hero p{font-size:clamp(18px,2.1vw,22px);color:var(--slate);max-width:34em;margin-top:22px}
.actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:32px}
.btn{display:inline-block;text-decoration:none;font-weight:700;padding:14px 24px;border-radius:999px;background:var(--amber);color:var(--ink)}
.btn.quiet{background:transparent;color:var(--ivory);border:1px solid var(--rule)}
.btn.quiet:hover{border-color:var(--champagne)}
.car{display:block;width:100%;height:auto;margin-top:clamp(28px,6vw,72px);color:var(--champagne)}
.road{border-top:1px solid var(--rule)}
section{padding-block:clamp(56px,9vw,112px)}
.types{margin-top:40px;border-top:1px solid var(--rule)}
.type{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:8px 40px;padding:28px 0;border-bottom:1px solid var(--rule)}
.type p{color:var(--slate)}
.type p + p{margin-top:8px;color:var(--ivory)}
.steps{list-style:none;margin:40px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:32px;counter-reset:step}
.steps li{counter-increment:step;border-top:1px solid var(--champagne);padding-top:18px}
.steps li::before{content:counter(step);display:block;font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;font-size:40px;line-height:1;color:var(--champagne);margin-bottom:14px}
.steps h3{font-size:21px}
.steps p{color:var(--slate);margin-top:8px}
.assure{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px 56px;margin-top:40px}
.assure p{color:var(--slate);margin-top:6px}
.firms{background:var(--ivory);color:var(--ink)}
.firms a{color:var(--ink)}
.firms h2{max-width:18ch}
.firms .lead{font-size:20px;color:#4A5268;max-width:36em;margin-top:18px}
.firms ul{margin:32px 0 0;padding:0;list-style:none;border-top:1px solid #D8D0BE;max-width:44em}
.firms li{padding:16px 0;border-bottom:1px solid #D8D0BE}
.firms .btn{background:var(--ink);color:var(--ivory)}
.small{font-size:15px;color:var(--slate);max-width:48em;margin-top:28px}
.firms .small{color:#4A5268}
footer{border-top:1px solid var(--rule);color:var(--slate);font-size:14px;padding-block:24px 36px}
footer div + div{margin-top:6px}
footer a{color:var(--slate)}
@media (max-width:720px){.type{grid-template-columns:1fr}.steps{grid-template-columns:1fr}.assure{grid-template-columns:1fr}}
"""

# A long, low saloon drawn in single lines. Our own drawing: no make or model.
EXEC_CAR = """<svg class="car" viewBox="0 0 1040 200" role="img" aria-label="Line drawing of an executive saloon car" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
<path d="M70 150 H40 C30 150 26 144 28 134 L36 112 C40 102 50 98 66 96 L250 78 C300 46 372 26 470 24 H610 C690 26 752 46 812 78 L960 94 C992 98 1008 110 1010 130 V140 C1010 146 1006 150 998 150 H930"/>
<path d="M330 150 H690"/>
<path d="M270 80 C316 52 380 38 468 36 H604 C676 38 730 52 784 80 Z"/>
<path d="M508 36 V80 M508 80 V146"/>
<path d="M300 84 C292 104 290 126 292 146 M772 84 C784 104 790 126 790 146"/>
<path d="M548 96 H584 M330 96 H366"/>
<circle cx="200" cy="150" r="52"/><circle cx="200" cy="150" r="30"/>
<circle cx="810" cy="150" r="52"/><circle cx="810" cy="150" r="30"/>
<path d="M36 118 H74 M968 106 C984 110 996 118 1002 128"/>
</svg>"""


def executive_page():
    path = "/executive/"
    title = "ThumbiT Executive – executive cars from licensed local firms"
    description = "Executive saloons, luxury cars and executive people carriers from licensed local firms, at a fixed price agreed before you travel."
    links = "".join(
        f'<a href="{href}"{" aria-current=page" if href == path else ""}>{label}</a>' for href, label in NAV
    )
    join = f"mailto:{EMAIL}?subject=ThumbiT%20Executive%20for%20my%20firm"
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="theme-color" content="#0E1626">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="https://{DOMAIN}/og-image.png">
<meta property="og:url" content="https://{DOMAIN}{path}">
<link rel="canonical" href="https://{DOMAIN}{path}">
<style>{EXEC_CSS}</style>
</head>
<body>
<header class="wrap top">
<a href="/"><img src="/thumbit-logo-on-dark.png" alt="ThumbiT" width="127" height="36"></a>
<nav aria-label="Main">{links}</nav>
</header>
<main>
<div class="wrap hero">
<h1>The car you asked for, at the price you agreed.</h1>
<p>ThumbiT Executive is an executive saloon, a luxury car or an executive people carrier from a licensed local firm. You choose the car and see its fixed price before you book.</p>
<div class="actions">
<a class="btn" href="/app/">Book in the ThumbiT app</a>
<a class="btn quiet" href="#firms">For taxi and private hire firms</a>
</div>
{EXEC_CAR}
</div>
<div class="road"></div>

<section class="wrap" aria-labelledby="cars">
<h2 id="cars">Three kinds of car</h2>
<div class="types">
<div class="type"><h3>Executive saloon</h3><div><p>A Mercedes E-Class, BMW 5 Series or similar.</p><p>For the airport, a meeting, or a journey you'd like to be quiet and comfortable.</p></div></div>
<div class="type"><h3>Luxury car or limousine</h3><div><p>A Mercedes S-Class, a limousine, or a wedding and event car.</p><p>For the days that matter: weddings, proms, anniversaries, and guests you want to look after.</p></div></div>
<div class="type"><h3>Executive people carrier</h3><div><p>A Mercedes V-Class or similar.</p><p>For a group travelling together, with room for everyone's luggage.</p></div></div>
</div>
<p class="small">Each firm lists the cars it runs, so the car you see when you book is the kind of car that arrives. Executive cars are offered where a local firm provides them.</p>
</section>

<section class="wrap" aria-labelledby="how">
<h2 id="how">How you book one</h2>
<ol class="steps">
<li><h3>Enter your journey</h3><p>Pickup, destination and when, in the ThumbiT app.</p></li>
<li><h3>Choose your car</h3><p>On the price screen you see each local firm's executive cars, with a fixed price for your journey.</p></li>
<li><h3>Travel</h3><p>Your booking goes to the firm you chose. Follow your driver on the map as they arrive.</p></li>
</ol>
</section>

<section class="wrap" aria-labelledby="know">
<h2 id="know">What you can count on</h2>
<div class="assure">
<div><h3>A fixed price</h3><p>The firm's own price for your journey, shown before you book. It is the price recorded when the journey ends.</p></div>
<div><h3>Licensed firms and drivers</h3><p>Every executive journey is private hire, with a licensed local firm and a licensed driver.</p></div>
<div><h3>The firm you chose</h3><p>An executive booking is offered only to the firm whose car and price you picked.</p></div>
<div><h3>Electric or hybrid, if you prefer</h3><p>On any booking you can say you'd prefer an electric or hybrid car. One is sent when it's free.</p></div>
</div>
<p class="small">A £1.50 booking fee is paid in the app. Your fare is paid to the driver unless the app says otherwise.</p>
</section>

<section class="firms" id="firms" aria-labelledby="firmsh">
<div class="wrap">
<h2 id="firmsh">For firms with executive cars</h2>
<p class="lead">The Executive fleet is an add-on to ThumbiT dispatch. It puts your executive cars in front of local passengers, at prices you set yourself.</p>
<ul>
<li>Mark each car as an executive saloon, a luxury car or limousine, or an executive people carrier.</li>
<li>Set your own price per mile and minimum fare for each kind of car.</li>
<li>Executive bookings are private hire at your agreed price, and are only offered to a driver in the right kind of car.</li>
<li>Your office can add executive bookings on the dispatch desk in the same way.</li>
</ul>
<div class="actions"><a class="btn" href="{join}">Ask about the Executive fleet</a></div>
<p class="small">The Executive fleet is switched on for each firm by ThumbiT. Email <a href="mailto:{EMAIL}">{EMAIL}</a> and we'll talk it through.</p>
</div>
</section>
</main>
<footer><div class="wrap">
<div>ThumbiT is a booking app run by Michael Binmore-May, trading as ThumbiT. Journeys are provided by independent, licensed taxi and private hire firms.</div>
<div><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="/terms/">Passenger Terms</a> · <a href="/privacy/">Privacy Policy</a> · <a href="/delete-account/">Delete your account</a></div>
<div>© 2026 ThumbiT</div>
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

    for name in ["favicon.png", "apple-touch-icon.png", "og-image.png", "thumbit-icon-192.png", "thumbit-logo-on-dark.png", "thumbit-logo-on-light.png"]:
        shutil.copy(os.path.join(LOGO, name), os.path.join(OUT, name))

    home = f"""
<section class="hero">
<picture><source srcset="/thumbit-logo-on-dark.png" media="(prefers-color-scheme: dark)"><img src="/thumbit-logo-on-light.png" alt="ThumbiT" width="320" height="91"></picture>
<h1 class="sr">ThumbiT</h1>
<p class="lead">Licensed local taxis, booked in a tap.</p>
<p><a class="cta" href="/support/">How it works</a><a class="cta secondary" href="mailto:{EMAIL}">Contact us</a></p>
<p><a class="cta" href="{APP_STORE_URL}">Download on the App Store</a></p>
<p><em>The Android app is coming soon to Google Play.</em></p>
</section>
<div class="cards">
<div class="card"><h3>Licensed local drivers</h3><p>Every trip is with a licensed local taxi or private hire firm.</p></div>
<div class="card"><h3>See your price first</h3><p>Fares use the official council tariff for your pickup area.</p></div>
<div class="card"><h3>Pay the driver</h3><p>Only a £1.50 booking fee is paid in the app. Pay your fare by cash or card.</p></div>
<div class="card"><h3>Safety built in</h3><p>Track your driver, share your trip and use Emergency SOS.</p></div>
</div>
"""
    write("index.html", page("/", "Home", home, "Book licensed local taxis in a tap with the ThumbiT app."))

    for slug, title, desc in [
        ("privacy", "Privacy Policy", "How ThumbiT collects, uses and protects your personal data."),
        ("terms", "Passenger Terms", "The terms that apply when you book a taxi with ThumbiT."),
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
    write("support/index.html", page("/support/", "Help", support, "Help with the ThumbiT taxi booking app, and how to contact us."))

    delete = f"""
<h1>Delete your account</h1>
<p class="lead">You can delete your ThumbiT account at any time.</p>
<h2>In the app</h2>
<ol>
<li>Open the ThumbiT app and tap <strong>Settings</strong>.</li>
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
    write("delete-account/index.html", page("/delete-account/", "Delete your account", delete, "How to delete your ThumbiT account and data."))

    store_buttons = "".join(
        f'<a class="cta" href="{html.escape(url)}">{label}</a>'
        for url, label in [(APP_STORE_URL, "Download on the App Store"), (PLAY_STORE_URL, "Get it on Google Play")]
        if url
    )
    app_page = f"""
<section class="hero">
<picture><source srcset="/thumbit-logo-on-dark.png" media="(prefers-color-scheme: dark)"><img src="/thumbit-logo-on-light.png" alt="ThumbiT" width="320" height="91"></picture>
<h1>Get the ThumbiT app</h1>
<p class="lead">Licensed local taxis, booked in a tap.</p>
<p>{store_buttons}<a class="cta{' secondary' if store_buttons else ''}" href="{BOOK_ONLINE_URL}">Book online now</a></p>
</section>
<script>
(function () {{
  var ua = navigator.userAgent || "";
  var ios = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && "ontouchend" in document);
  var android = /Android/.test(ua);
  var go = ios ? {json.dumps(APP_STORE_URL)} : android ? {json.dumps(PLAY_STORE_URL)} : "";
  if (go) location.replace(go);
}})();
</script>
"""
    write("app/index.html", page("/app/", "Get the app", app_page, "Get the ThumbiT taxi app for iPhone or Android, or book online."))

    write("executive/index.html", executive_page())

    write("404.html", page("/404", "Page not found", '<h1>Page not found</h1><p class="lead">Sorry, that page doesn\'t exist.</p><p><a class="cta" href="/">Go to the home page</a></p>', "Page not found"))
    write("CNAME", f"{DOMAIN}\n")
    write(".nojekyll", "")
    print("built", OUT)


if __name__ == "__main__":
    main()
