"""Builds the HTML pages (shared header/footer). Run: python3 _tools/build_pages.py

Legal body copy in privacy.html and terms.html is preserved verbatim.
"""
import html
import json
import os
import re
import subprocess

import segno

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://huddletape.app"
EMAIL = "huddletape.app@gmail.com"
DESC = (
    "HuddleTape puts your crew’s open bets on a neon ticker over whatever’s on your Google TV. "
    "Join from any phone browser — no app. 30-day free trial, then $1.99/mo or $9.99/yr. 21+."
)
OG_ALT = "HuddleTape wordmark over a TV ticker with a parlay leg rail and Tailer’s gold TAILING tab"


def qr_svg():
    q = segno.make(URL + "/#beta", error="m", micro=False)
    m = q.matrix
    n = len(m)
    d = "".join(f"M{x},{y}h1v1h-1z" for y, row in enumerate(m) for x, v in enumerate(row) if v)
    return (
        f'<svg viewBox="0 0 {n} {n}" role="img" aria-label="QR code linking to the HuddleTape beta signup" '
        f'shape-rendering="crispEdges"><path d="{d}" fill="#0A0614"/></svg>'
    )


def head(title, desc=DESC, path="/", robots="index,follow", extra=""):
    full = title if title.startswith("HuddleTape") else f"{title} · HuddleTape"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0A0614">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="{URL}{path}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="HuddleTape">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{html.escape(full)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{URL}{path}">
<meta property="og:image" content="{URL}/assets/img/og-card.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(OG_ALT)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@HuddleTape">
<meta name="twitter:title" content="{html.escape(full)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{URL}/assets/img/og-card.png">
<meta name="twitter:image:alt" content="{html.escape(OG_ALT)}">
<link rel="preload" href="/assets/fonts/anton.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/barlow-sc-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/barlow-sc-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(beta_href):
    return f"""<header class="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="HuddleTape home">
      <img class="mark" src="/assets/img/mark.svg" alt="" width="38" height="23">
      <img class="word" src="/assets/img/wordmark.svg" alt="HuddleTape" width="108" height="22">
    </a>
    <nav class="nav" aria-label="Main">
      <a class="hide-sm" href="/#how">How it works</a>
      <a class="hide-sm" href="/#why">Why it’s fun</a>
      <a class="hide-sm" href="/#pricing">Pricing</a>
      <a class="hide-sm" href="/#faq">FAQ</a>
      <a class="btn btn-primary btn-sm" href="{beta_href}">Join the beta</a>
    </nav>
  </div>
</header>
"""


FOOT = f"""<footer class="foot">
  <div class="wrap">
    <div class="foot-brand">
      <img class="word" src="/assets/img/wordmark.svg" alt="HuddleTape" width="118" height="24">
      <p>The watch-party ticker for Google TV.</p>
    </div>
    <p class="rg"><b>21+</b> · Play responsibly · Set a budget before kickoff · Problem gambling? Call or text <a href="tel:18004262537">1-800-GAMBLER</a></p>
    <p>HuddleTape doesn't take or place wagers and isn't a sportsbook. Not affiliated with any sportsbook, exchange, team or league. Ticker images show sample data.</p>
    <nav aria-label="Footer">
      <a href="/privacy.html">Privacy</a>
      <a href="/terms.html">Terms</a>
      <a href="/beta.html">Join the beta</a>
      <a href="mailto:{EMAIL}">Support: {EMAIL}</a>
    </nav>
    <p>© 2026 HuddleTape LLC</p>
  </div>
</footer>
</body>
</html>
"""


def card(who, what, right):
    return f'<div class="card"><span class="who">{who}</span><span class="what">{what}</span>{right}</div>'


def ticker_cards():
    rows = [
        card("Big Tex", "Owls to win", '<span class="side">Yes</span><span class="pct">62%</span>'),
        card("Coach Dee", "Gulls +3.5", '<span class="won">Won</span>'),
        card("Momo", "Over 47.5", '<span class="pct">38%</span>'),
        card("Jake", "Moose −2.5", '<span class="side">Yes</span><span class="pct">55%</span>'),
        card("Rio", "Gulls to win", '<span class="pct">44%</span>'),
    ]
    return "".join(rows)


def demo():
    cards = ticker_cards()
    label = (
        "Sample data: a television showing a game, with HuddleTape over the picture. "
        "A gold tab reads TAILING, Sam, above Kayla’s 3-leg parlay at 21 percent: "
        "Owls (hit), Over 47.5 (hit), and Moose −2.5 (live). "
        "A ticker scrolls sample bets for Big Tex, Coach Dee, Momo, Jake, and Rio. "
        "A QR code invites friends to scan and add picks they already have. Room code DEN."
    )
    return f"""<figure class="demo">
  <input class="pause" id="pause-demo" type="checkbox">
  <div class="tv">
    <div class="screen" role="img" aria-label="{html.escape(label)}">
      <div class="scene" aria-hidden="true">
        <div class="sky"></div>
        <div class="stands"></div>
        <div class="lights"><i></i><i></i><i></i><i></i></div>
        <div class="pitch"></div>
        <div class="ball"></div>
        <span class="sample-tag">Sample</span>
        <div class="bug"><span>Owls 17</span><span>Gulls 14</span><b>Q3</b></div>
      </div>
      <div class="lower" aria-hidden="true">
        <div class="feature">
          <div class="gold-tab">
            <img src="/assets/img/tailer.webp" alt="" width="220" height="145">
            <span><b>Tailing</b><i>Sam</i></span>
          </div>
          <div class="slip">
            <div class="slip-top">
              <span class="who">Kayla</span>
              <span class="what">3-leg parlay</span>
              <span class="pct">21%<small>chance</small></span>
            </div>
            <ol class="legs">
              <li class="hit"><span class="rail"></span><span class="leg-name">Owls</span><span class="leg-st">Hit</span></li>
              <li class="hit d2"><span class="rail"></span><span class="leg-name">Over 47.5</span><span class="leg-st">Hit</span></li>
              <li class="live"><span class="rail"></span><span class="leg-name">Moose −2.5</span><span class="leg-st">Live</span></li>
            </ol>
          </div>
        </div>
        <div class="ticker">
          <div class="tk-brand"><img src="/assets/img/mark.svg" alt="" width="26" height="16"></div>
          <div class="tk-rail"><div class="tk-track">{cards}{cards}</div></div>
          <div class="qr">{qr_svg()}<div><div class="q1">Scan to add<br>your picks</div><div class="q2">ROOM</div><div class="q3">DEN</div></div></div>
        </div>
      </div>
    </div>
    <div class="chin" aria-hidden="true"><span class="led"></span></div>
  </div>
  <div class="neck" aria-hidden="true"></div>
  <div class="stand" aria-hidden="true"></div>
  <figcaption>
    <span><b>SAMPLE DATA</b><span class="cap-more"> · Made-up names, teams, and numbers.</span></span>
    <label class="pause-label" for="pause-demo"><span class="when-play">Pause sample</span><span class="when-paused">Play sample</span></label>
  </figcaption>
</figure>"""


FAQS = [
    (
        "Is HuddleTape a sportsbook?",
        "No. HuddleTape doesn’t take, place, or settle wagers, and you can’t bet through it. It shows bets your crew already made somewhere else, so the room can watch together. It isn’t a sportsbook, and it doesn’t give betting advice.",
    ),
    (
        "Do my friends need to download anything?",
        "No. They scan the QR code on the TV and join from any phone browser. No app.",
    ),
    (
        "What does it cost?",
        "The private beta is free. At the Google Play launch, the TV owner gets a 30-day free trial, then $1.99 a month or $9.99 a year. Joining from a phone is free.",
    ),
    (
        "Which TVs does it work on?",
        "Google TV and Android TV. Fire TV, Roku, Apple TV, and Samsung or LG apps aren’t supported yet. A Google TV streamer in any HDMI port works.",
    ),
    (
        "Will everyone see how much I put down?",
        "No. Dollar amounts are off by default. The ticker shows names, picks, and a percent chance. You can hide your picks from the ticker anytime.",
    ),
    (
        "What happens to my screenshots and connected accounts?",
        'Screenshots are read on your phone and never uploaded. If you connect an account, access is read-only and the key is stored only on your TV. See the <a href="/privacy.html">Privacy Policy</a>.',
        "Screenshots are read on your phone and never uploaded. If you connect an account, access is read-only and the key is stored only on your TV. See the Privacy Policy.",
    ),
    (
        "When can I get it?",
        'The private beta opens around Thanksgiving 2026. The public Google Play launch is planned for January 2027. <a href="/beta.html">Join the beta</a> for a host spot.',
        "The private beta opens around Thanksgiving 2026. The public Google Play launch is planned for January 2027. Join the beta for a host spot.",
    ),
]


def faq_html():
    blocks = []
    for item in FAQS:
        q, ans = item[0], item[1]
        blocks.append(f"<details><summary>{q}</summary><p>{ans}</p></details>")
    return "\n    ".join(blocks)


def json_ld():
    entities = [
        {
            "@type": "WebSite",
            "name": "HuddleTape",
            "url": URL + "/",
            "description": DESC,
        },
        {
            "@type": "SoftwareApplication",
            "name": "HuddleTape",
            "applicationCategory": "EntertainmentApplication",
            "operatingSystem": "Google TV, Android TV",
            "offers": {
                "@type": "AggregateOffer",
                "lowPrice": "1.99",
                "highPrice": "9.99",
                "priceCurrency": "USD",
                "offerCount": "2",
                "description": "30-day free trial, then $1.99 per month or $9.99 per year for the TV owner. Joining from a phone is free.",
            },
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item[0],
                    "acceptedAnswer": {"@type": "Answer", "text": item[-1]},
                }
                for item in FAQS
            ],
        },
    ]
    data = {"@context": "https://schema.org", "@graph": entities}
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + "\n</script>\n"


def form(source):
    return f"""<form class="signup" action="https://formsubmit.co/{EMAIL}" method="POST" aria-describedby="form-note-{source}">
  <input type="hidden" name="_subject" value="New HuddleTape beta signup">
  <input type="hidden" name="_next" value="{URL}/thanks.html">
  <input type="hidden" name="_captcha" value="false">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="source" value="{source}">
  <div class="hp" aria-hidden="true">
    <label for="hp-{source}">Leave this field empty</label>
    <input type="text" id="hp-{source}" name="_honey" tabindex="-1" autocomplete="off">
  </div>
  <div class="field">
    <label for="name-{source}">Name</label>
    <input type="text" id="name-{source}" name="name" autocomplete="name" required maxlength="80" placeholder="First name is fine">
  </div>
  <div class="field">
    <label for="email-{source}">Email</label>
    <input type="email" id="email-{source}" name="email" autocomplete="email" inputmode="email" required maxlength="120" placeholder="you@example.com">
  </div>
  <div class="field">
    <label for="tv-{source}">TV or streamer <span class="opt">(optional)</span></label>
    <input type="text" id="tv-{source}" name="tv_device" maxlength="100" placeholder="e.g. Onn 4K, Google TV Streamer" aria-describedby="tv-hint-{source}">
    <span class="hint" id="tv-hint-{source}">Helps us check your setup will work. Fire TV and Roku aren't supported yet.</span>
  </div>
  <div class="check">
    <input type="checkbox" id="age-{source}" name="confirmed_21_plus" value="yes" required>
    <div>
      <label for="age-{source}">I’m 21 or older and I agree to the Terms and the Privacy Policy.</label>
      <p class="hint">Read the <a href="/terms.html">Terms</a> and <a href="/privacy.html">Privacy Policy</a>.</p>
    </div>
  </div>
  <button class="btn btn-primary" type="submit">Join the beta</button>
  <p class="fineprint" id="form-note-{source}">We'll only email you about the HuddleTape beta and launch. Unsubscribe anytime by replying "stop".</p>
</form>"""


def beta_block(source, heading="h2"):
    return f"""<section class="sec" id="beta" aria-labelledby="beta-h">
  <div class="wrap beta">
    <div>
      <p class="kicker">Thanksgiving 2026</p>
      <{heading} id="beta-h">Join the private beta</{heading}>
      <p class="intro">A small group of Google TV hosts, then the Google Play launch in January 2027. You get the room. The crew joins free.</p>
      <ul class="perks">
        <li>Early access for your whole crew</li>
        <li>Free during the beta</li>
        <li>A direct line to the team — tell us what the tape should do next</li>
      </ul>
    </div>
    {form(source)}
  </div>
</section>"""


INDEX = (
    head("HuddleTape · Your crew’s bets, live on the TV", extra=json_ld())
    + header("#beta")
    + f"""<main id="main">
<section class="hero" aria-labelledby="hero-h">
  <div class="wrap hero-grid">
    <div class="hero-lead">
      <p class="eyebrow">21+ · Watch-party ticker</p>
      <h1 id="hero-h">Your crew’s bets, <em>live on the TV.</em></h1>
      <p class="lede">Friends add the bets they already have from any phone browser — no app. A neon ticker floats over whatever’s on.</p>
    </div>
    {demo()}
    <div class="hero-rest">
      <div class="cta-row">
        <a class="btn btn-primary" href="#beta">Join the beta</a>
        <a class="btn btn-ghost" href="#how">How it works</a>
      </div>
      <p class="assure">Shows bets. Never takes them.</p>
      <ul class="chips">
        <li>No phone app</li>
        <li>30-day free trial</li>
        <li>Guests join free</li>
      </ul>
    </div>
  </div>
</section>

<section class="sec" id="how" aria-labelledby="how-h">
  <div class="wrap">
    <p class="kicker">Three steps</p>
    <h2 id="how-h">How it works</h2>
    <p class="intro">Nobody has to pass a phone around the couch.</p>
    <ol class="steps">
      <li>
        <span class="n">01</span>
        <h3>Open a room</h3>
        <p>Put HuddleTape on your Google TV or Android TV. The ticker sits on the bottom edge, over the game, a stream, or multiview.</p>
      </li>
      <li>
        <span class="n">02</span>
        <h3>The crew scans in</h3>
        <p>The QR on the TV opens a page in any phone browser. No app to download, and no account to set up.</p>
      </li>
      <li>
        <span class="n">03</span>
        <h3>Open bets hit the tape</h3>
        <p>Add a screenshot of a slip you already have, or pull open bets from a connected account. Names, picks, and a percent scroll with the room.</p>
      </li>
    </ol>
    <ul class="devices">
      <li><b>On the TV</b> Google TV and Android TV.</li>
      <li><b>In the room</b> Any phone browser. No app.</li>
      <li><b>Not yet</b> Fire TV, Roku, Apple TV, and Samsung or LG apps. A Google TV streamer in an HDMI port covers those sets.</li>
    </ul>
  </div>
</section>

<section class="sec" id="why" aria-labelledby="why-h">
  <div class="wrap">
    <p class="kicker">On the glass</p>
    <h2 id="why-h">Why it’s fun</h2>
    <p class="intro">The jokes land on the biggest screen in the house. Tailer handles the introductions.</p>
    <div class="why">
      <article>
        <div class="why-vis" aria-hidden="true">
          <div class="gold-tab">
            <img src="/assets/img/tailer.webp" alt="" width="220" height="145">
            <span><b>Tailing</b><i>Sam</i></span>
          </div>
          <div class="mini-slip"><span>Big Tex</span><span class="dim">Owls to win</span><span class="pct">62%</span></div>
        </div>
        <h3>Tailer names you</h3>
        <p>Tail a friend’s bet and a gold tab rises over it with your name. Nothing gets placed. It’s a name on the glass.</p>
      </article>
      <article>
        <div class="why-vis" aria-hidden="true">
          <div class="mini-slip"><span>Kayla</span><span class="dim">3-leg parlay</span><span class="pct">21%</span></div>
          <div class="why-legs">
            <span><i></i>Owls<em>Hit</em></span>
            <span><i></i>Over 47.5<em>Hit</em></span>
            <span class="wait"><i></i>Moose −2.5<em>Live</em></span>
          </div>
        </div>
        <h3>Every leg, in lights</h3>
        <p>A parlay keeps a rail. Each leg lights up when it hits, so the couch can follow without crowding one phone.</p>
      </article>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="band-h">
  <div class="wrap band-inner">
    <div>
      <p class="kicker">Founding hosts</p>
      <h2 id="band-h">Get the ticker on your TV first.</h2>
      <p>Private beta around Thanksgiving 2026. Google Play in January 2027.</p>
    </div>
    <a class="btn btn-primary" href="#beta">Join the beta</a>
  </div>
</section>

<section class="sec" id="pricing" aria-labelledby="price-h">
  <div class="wrap">
    <p class="kicker">After the trial</p>
    <h2 id="price-h">The TV owner pays. The crew doesn’t.</h2>
    <p class="intro">30 days free, then one small subscription for the set that hosts the room. Joining from a phone is free.</p>
    <div class="price-grid">
      <article class="price price-year">
        <h3>Yearly</h3>
        <p class="amt">$9.99<span class="per">/yr</span></p>
        <p class="trial">30-day free trial</p>
        <ul>
          <li>For the TV that hosts the room</li>
          <li>$9.99 for the year, versus $23.88 monthly</li>
        </ul>
      </article>
      <article class="price">
        <h3>Monthly</h3>
        <p class="amt">$1.99<span class="per">/mo</span></p>
        <p class="trial">30-day free trial</p>
        <ul>
          <li>Same ticker, billed each month</li>
          <li>Cancel anytime in Google Play</li>
        </ul>
      </article>
    </div>
    <p class="guest"><b>Joining from a phone is $0.</b> Any browser, no app, no trial to use up. The subscription is only for the TV owner.</p>
    <p class="fine">The private beta is free for hosts. The prices above start with the Google Play launch in January 2027, billed through Google Play after the trial. HuddleTape doesn’t take or place bets — this pays for the TV display.</p>
    <a class="btn btn-primary" href="#beta">Join the beta</a>
  </div>
</section>

<section class="sec" id="faq" aria-labelledby="faq-h">
  <div class="wrap">
    <p class="kicker">Straight answers</p>
    <h2 id="faq-h">FAQ</h2>
    <div class="faq">
    {faq_html()}
    </div>
  </div>
</section>

{beta_block("home")}
</main>
"""
    + FOOT
)


BETA = (
    head(
        "Join the beta",
        "Sign up for the HuddleTape private beta: a neon watch-party ticker for Google TV. Hosts around Thanksgiving 2026. 21+.",
        "/beta.html",
    )
    + header("#beta")
    + f"<main id=\"main\">\n{beta_block('beta-page', 'h1')}\n</main>\n"
    + FOOT
)

THANKS = (
    head("You're on the list", "Thanks for joining the HuddleTape beta.", "/thanks.html", "noindex")
    + header("/beta.html")
    + """<main id="main" class="wrap center-page">
  <div>
    <div class="mascot-frame">
      <img src="/assets/img/tailer.webp" alt="Tailer, the HuddleTape golden retriever" width="220" height="145">
    </div>
    <h1>You’re on the list.</h1>
    <p>Thanks for signing up. We’ll email you when a host spot opens, around Thanksgiving. Your crew joins from their phones — no app, and free.</p>
    <a class="btn btn-primary" href="/">Back to HuddleTape</a>
  </div>
</main>
"""
    + FOOT
)

NOTFOUND = (
    head("Page not found", "This page fumbled.", "/404.html", "noindex")
    + header("/beta.html")
    + """<main id="main" class="wrap center-page">
  <div>
    <div class="mascot-frame">
      <img src="/assets/img/tailer.webp" alt="" width="220" height="145">
    </div>
    <h1>This page fumbled.</h1>
    <p>Nothing on the tape at that address.</p>
    <a class="btn btn-primary" href="/">Back to HuddleTape</a>
  </div>
</main>
"""
    + FOOT
)


def legal_body(path):
    src = subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=SITE, text=True)
    m = re.search(r'<p class="meta">.*?</p>\s*(.*)\s*</div>\s*</main>', src, re.S)
    if not m:
        raise SystemExit(f"could not preserve legal copy from {path}")
    return m.group(1).strip()


def legal(title, path, updated, body):
    desc = f"HuddleTape {title.lower()}: draft pending attorney review."
    return (
        head(title + " (Draft)", desc, path, "noindex")
        + header("/beta.html")
        + f"""<main id="main" class="legal">
  <div class="wrap">
    <p class="draft-banner" role="note">DRAFT — pending attorney review. This document is not final and may change before HuddleTape launches.</p>
    <h1>{title}</h1>
    <p class="meta">Draft dated {updated} · HuddleTape LLC</p>
    {body}
  </div>
</main>
"""
        + FOOT
    )


PRIVACY = legal("Privacy Policy", "/privacy.html", "October 9, 2026", legal_body("privacy.html"))
TERMS = legal("Terms of Use", "/terms.html", "October 9, 2026", legal_body("terms.html"))

for name, content in {
    "index.html": INDEX,
    "beta.html": BETA,
    "thanks.html": THANKS,
    "404.html": NOTFOUND,
    "privacy.html": PRIVACY,
    "terms.html": TERMS,
}.items():
    with open(os.path.join(SITE, name), "w", encoding="utf-8") as fh:
        fh.write(content)
    print(name, "ok")
