"""Builds the HTML pages (shared header/footer). Run: python3 _tools/build_pages.py

Legal body copy in privacy.html and terms.html is preserved verbatim from those files.
"""
import html
import json
import os
import re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://huddletape.app"
EMAIL = "huddletape.app@gmail.com"
DESC = (
    "Your crew’s prediction-market picks, on a ticker over whatever’s on TV. "
    "HuddleTape doesn’t take or place bets. 21+."
)
OG_ALT = "HuddleTape on a television: a sample ticker of prediction-market picks over the picture. Made-up names and numbers."
CHECK = (
    '<svg class="ck" viewBox="0 0 16 16" aria-hidden="true" width="16" height="16">'
    '<path d="M3.2 8.3 6.4 11.5 12.8 4.4" fill="none" stroke="currentColor" '
    'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)
# Swap REPLACE-ME for the GoatCounter site code after the owner creates an account.
GC = """<script data-goatcounter="https://REPLACE-ME.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
"""
NOTIFY_AUTORESPONSE = (
    "Thanks! HuddleTape beta signups are coming soon, and you'll be the first to know. "
    "— Tailer & the HuddleTape team"
)


def head(title, desc=DESC, path="/", robots="index,follow", extra="", body_class=""):
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
{extra}{GC}</head>
<body{(' class="' + body_class + '"') if body_class else ""}>
<a class="skip" href="#main">Skip to content</a>
"""


def header(cta_href):
    return f"""<header class="top">
  <div class="bar">
    <div class="wrap">
      <a class="brand" href="/" aria-label="HuddleTape home">
        <img class="word" src="/assets/img/wordmark.svg" alt="HuddleTape" width="148" height="30">
      </a>
      <nav class="nav" aria-label="Main">
        <a class="btn btn-primary btn-sm" href="{cta_href}">Get early access</a>
      </nav>
    </div>
  </div>
</header>
"""


FOOT = f"""<footer class="foot">
  <div class="wrap foot-top">
    <div>
      <img class="word" src="/assets/img/wordmark.svg" alt="HuddleTape" width="148" height="30">
      <p class="tag">Prediction-market picks, on your TV.</p>
    </div>
    <nav aria-label="Company">
      <p class="col-label">Company</p>
      <a href="/beta.html">Early access</a>
      <a href="/privacy.html">Privacy</a>
      <a href="/terms.html">Terms</a>
      <a href="mailto:{EMAIL}">Support</a>
    </nav>
  </div>
  <div class="rg-bar">
    <div class="wrap">
      <p><span class="age">21+</span> Play responsibly. Set a budget before kickoff. Problem gambling? Call or text <a href="tel:18006973738">1-800-MY-RESET</a>.</p>
    </div>
  </div>
  <div class="wrap foot-legal">
    <p>Not affiliated with any other company. Pictures show sample data.</p>
    <p>© 2026 HuddleTape</p>
  </div>
</footer>
</body>
</html>
"""


def scorecard():
    return f"""<div class="parlay">
            <div class="parlay-main">
              <p class="who">Kayla</p>
              <p class="title">4-leg parlay</p>
              <p class="chance"><span class="big">48%</span> <span class="word">chance</span> <span class="tick up" aria-hidden="true">▲26</span><span class="sr">, up 26</span></p>
            </div>
            <ol class="plegs">
              <li class="hit">
                <span class="n" aria-hidden="true">1</span>
                <span class="pick">Owls −6.5</span>
                <span class="end">{CHECK}<span class="sr">Hit</span></span>
              </li>
              <li class="hit">
                <span class="n" aria-hidden="true">2</span>
                <span class="pick">Over 47.5</span>
                <span class="end">{CHECK}<span class="sr">Hit</span></span>
              </li>
              <li class="live">
                <span class="n" aria-hidden="true">3</span>
                <span class="pick">Moose −2.5<span class="meta">Q3 · 21–14</span></span>
                <span class="end"><span class="lp">63%</span><span class="tick up" aria-hidden="true">▲5</span><span class="sr">, up 5</span></span>
              </li>
              <li class="live">
                <span class="n" aria-hidden="true">4</span>
                <span class="pick">Gulls +3.5<span class="meta">Q4 · 17–20</span></span>
                <span class="end"><span class="lp">41%</span><span class="tick dn" aria-hidden="true">▼8</span><span class="sr">, down 8</span></span>
              </li>
            </ol>
          </div>"""


def demo():
    label = (
        "Sample data: a television with a game on, and a HuddleTape card over the picture. "
        "Kayla’s 4-leg parlay at 48 percent, up 26. "
        "Owls minus 6.5, hit. Over 47.5, hit. "
        "Moose minus 2.5, live, third quarter 21 to 14, 63 percent, up 5. "
        "Gulls plus 3.5, live, fourth quarter 17 to 20, 41 percent, down 8. "
        "Made-up names and numbers."
    )
    return f"""<figure class="stage">
  <div class="set">
    <div class="tv">
      <div class="screen" role="img" aria-label="{html.escape(label)}">
        <div class="scene" aria-hidden="true">
          <div class="sky"></div>
          <div class="bowl"></div>
          <div class="lamps"></div>
          <div class="turf"><span>20</span><span>30</span><span>40</span><span>50</span><span>40</span></div>
          <div class="vignette"></div>
          <div class="bug"><span class="bug-live">Live</span><span class="bug-team">Owls <b>21</b></span><span class="bug-team">Gulls <b>14</b></span><span class="bug-q">Q3<span>8:42</span></span></div>
          <span class="sample-tag">Sample</span>
        </div>
        <div class="lower" aria-hidden="true">
          {scorecard()}
        </div>
      </div>
      <div class="chin" aria-hidden="true"><span class="led"></span></div>
    </div>
    <div class="stand" aria-hidden="true"></div>
  </div>
  <figcaption>
    <span><b>Sample data.</b> Made-up names and numbers.</span>
  </figcaption>
</figure>"""


def json_ld():
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "name": "HuddleTape",
                "url": URL + "/",
                "description": DESC,
            }
        ],
    }
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + "\n</script>\n"


def form(source):
    return f"""<form class="signup" action="https://formsubmit.co/{EMAIL}" method="POST" aria-describedby="form-note-{source}">
  <input type="hidden" name="_subject" value="New HuddleTape early access signup">
  <input type="hidden" name="_next" value="{URL}/thanks.html">
  <input type="hidden" name="_captcha" value="false">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_autoresponse" value="You&#39;re on the HuddleTape list. Thanks for signing up. We&#39;ll email you when there&#39;s something to try. — HuddleTape">
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
    <input type="text" id="tv-{source}" name="tv_device" maxlength="100" placeholder="The set in your living room">
  </div>
  <div class="check">
    <input type="checkbox" id="age-{source}" name="confirmed_21_plus" value="yes" required>
    <div>
      <label for="age-{source}">I’m 21 or older and I agree to the Terms and the Privacy Policy.</label>
      <p class="hint">Read the <a href="/terms.html">Terms</a> and <a href="/privacy.html">Privacy Policy</a>.</p>
    </div>
  </div>
  <button class="btn btn-primary" type="submit">Join the list</button>
  <p class="fineprint" id="form-note-{source}">We’ll only email you about HuddleTape. Unsubscribe anytime by replying "stop".</p>
</form>"""


def list_block(source, heading="h2"):
    title = f'<{heading} id="list-h">Get early access.</{heading}>' if heading else ""
    return f"""<div class="signup-block" id="list">
  {title}
  {form(source)}
</div>"""


# Previous coming-soon homepage. Not written. The live index is poster_page() below.
INDEX = (
    head("HuddleTape", extra=json_ld())
    + header("#list")
    + f"""<main id="main">
<section class="hero" aria-labelledby="hero-h">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="kicker">Coming soon</p>
      <h1 id="hero-h">Watch it together.</h1>
      <p class="lede">Your crew’s prediction-market picks, on a ticker over whatever’s on TV.</p>
      <p class="plain">HuddleTape doesn’t take or place bets.</p>
    </div>
    {demo()}
    {list_block("home")}
  </div>
</section>
</main>
"""
    + FOOT
)


BETA = (
    head(
        "Get early access",
        "Get on the HuddleTape list. Your crew’s prediction-market picks, on a ticker over whatever’s on TV. 21+.",
        "/beta.html",
    )
    + header("#list")
    + f"""<main id="main">
<section class="band" aria-labelledby="list-h">
  <div class="wrap beta">
    <div>
      <p class="kicker">Coming soon</p>
      <h1 id="list-h">Get early access.</h1>
      <p class="sub">Your crew’s prediction-market picks, on a ticker over whatever’s on TV.</p>
      <p class="plain">HuddleTape doesn’t take or place bets.</p>
    </div>
    {list_block("early-access", heading="")}
  </div>
</section>
</main>
"""
    + FOOT
)

THANKS = (
    head("You're on the list", "Thanks for joining the HuddleTape list.", "/thanks.html", "noindex")
    + header("/beta.html")
    + """<main id="main" class="wrap center-page">
  <div>
    <div class="mascot-frame">
      <img src="/assets/img/tailer.webp" alt="Tailer, the HuddleTape golden retriever" width="220" height="145">
    </div>
    <h1>You’re on the list.</h1>
    <p>We’ll email you when there’s something to try. Tailer is the dog in the room. HuddleTape doesn’t take or place bets.</p>
    <a class="btn btn-primary" href="/">Back to HuddleTape</a>
  </div>
</main>
"""
    + FOOT
)

NOTFOUND = (
    head("Page not found", "That page isn’t here.", "/404.html", "noindex")
    + header("/beta.html")
    + """<main id="main" class="wrap center-page">
  <div>
    <div class="mascot-frame">
      <img src="/assets/img/tailer.webp" alt="Tailer, the HuddleTape golden retriever" width="220" height="145">
    </div>
    <h1>Page not found.</h1>
    <p>Nothing at that address. Tailer is the dog in the room. HuddleTape doesn’t take or place bets.</p>
    <a class="btn btn-primary" href="/">Back to HuddleTape</a>
  </div>
</main>
"""
    + FOOT
)


def legal_body(path):
    with open(os.path.join(SITE, path), encoding="utf-8") as fh:
        src = fh.read()
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
    <p class="draft-banner" role="note">DRAFT — pending attorney review. This document is not final and may change.</p>
    <h1>{title}</h1>
    <p class="meta">Draft dated {updated} · HuddleTape</p>
    {body}
  </div>
</main>
"""
        + FOOT
    )


PRIVACY = legal("Privacy Policy", "/privacy.html", "October 11, 2026", legal_body("privacy.html"))
TERMS = legal("Terms of Use", "/terms.html", "October 11, 2026", legal_body("terms.html"))

# index.html is the approved option D page, written after that markup is built.
for name, content in {
    "beta.html": BETA,
    "thanks.html": THANKS,
    "404.html": NOTFOUND,
    "privacy.html": PRIVACY,
    "terms.html": TERMS,
}.items():
    with open(os.path.join(SITE, name), "w", encoding="utf-8") as fh:
        fh.write(content)
    print(name, "ok")


# --- Hero options. The live homepage is option D, written at the end of this file. ---
# Underscore folder is unpublished by Jekyll. A, B, and C stay as rejected previews.

PICKS = [
    ("Kayla", "Owls −6.5", "", "71%", ""),
    ("Marcus", "Over 47.5", "", "64%", ""),
    ("Priya", "Moose −2.5", "Q3 · 21–14", "63%", "up"),
    ("Andre", "Gulls +3.5", "Q4 · 17–20", "41%", "dn"),
    ("Lena", "Owls −3", "", "58%", ""),
]
MOVE = {"up": ("▲5", "up 5"), "dn": ("▼8", "down 8")}
TAPE_SR = (
    "Sample data, made-up names and numbers. "
    "Kayla, Owls minus 6.5, 71 percent. "
    "Marcus, over 47.5, 64 percent. "
    "Priya, Moose minus 2.5, third quarter 21 to 14, 63 percent, up 5. "
    "Andre, Gulls plus 3.5, fourth quarter 17 to 20, 41 percent, down 8. "
    "Lena, Owls minus 3, 58 percent."
)


def tape_item(who, pick, meta, pct, move):
    meta_html = f'<span class="meta">{meta}</span>' if meta else ""
    move_html = ""
    if move:
        glyph, _words = MOVE[move]
        move_html = f'<span class="tick {move}" aria-hidden="true">{glyph}</span>'
    return (
        f'<span class="tape-item"><span class="who">{who}</span>'
        f'<span class="pick">{pick}</span>{meta_html}'
        f'<span class="pct">{pct}</span>{move_html}</span>'
    )


def tape(kind):
    seq = "".join(tape_item(*p) for p in PICKS)
    return (
        f'<div class="tape tape-{kind}" aria-hidden="true"><div class="tape-track">'
        f'<div class="tape-seq">{seq}</div><div class="tape-seq">{seq}</div>'
        f"</div></div>"
    )


def picture(tight=False):
    cls = "pic pic-tight" if tight else "pic"
    return f'''<div class="{cls}" aria-hidden="true"><div class="pic-sky"></div><div class="pic-field"></div><div class="pic-band"></div><div class="pic-lights"></div><div class="pic-vignette"></div><div class="pic-grain"></div><div class="pic-sheen"></div></div>'''


def scorebug():
    return (
        '<div class="bug" aria-hidden="true"><span class="bug-live">Live</span>'
        '<span class="bug-team">Owls <b>21</b></span>'
        '<span class="bug-team">Gulls <b>14</b></span>'
        '<span class="bug-q">Q3<span>8:42</span></span></div>'
        '<span class="sample-tag" aria-hidden="true">Sample</span>'
    )


def opt_signup(source):
    return f'''<section class="opt-signup" aria-labelledby="list-h">
  <div class="wrap opt-signup-grid">
    <h2 id="list-h">Get early access.</h2>
    {form(source)}
  </div>
</section>'''


def opt_page(key, title, desc, body):
    css = '<link rel="stylesheet" href="/assets/options.css">\n'
    return (
        head(title, desc, f"/_options/{key}.html", "noindex,nofollow", extra=css, body_class=f"opt opt-{key}")
        + header("#list")
        + f'<main id="main">\n{body}\n{opt_signup("option-" + key)}\n</main>\n'
        + FOOT
    )


A_LABEL = (
    "Sample data: a television in a dark room, with a game on. "
    "Owls 21, Gulls 14, third quarter, 8:42. "
    + TAPE_SR
)
B_LABEL = "Sample data: a ticker of prediction-market picks. " + TAPE_SR
C_LABEL = (
    "Sample data: the bottom of a broadcast. "
    "Priya’s pick, Moose minus 2.5, third quarter 21 to 14, 63 percent, up 5. "
    "Tailer has put the name Jordan on that pick. "
    + TAPE_SR
)

OPT_A = opt_page(
    "a",
    "Option A",
    "Your crew’s prediction-market picks, in a ticker along the bottom of the screen. HuddleTape doesn’t take or place bets. 21+.",
    f'''<section class="room" aria-labelledby="hero-h">
  <div class="wrap room-grid">
    <div class="hero-copy">
      <p class="kicker">Coming soon</p>
      <h1 id="hero-h">Under the<br>picture.</h1>
      <p class="lede">Your crew’s prediction-market picks, in a ticker along the bottom of the screen.</p>
      <p class="plain">HuddleTape doesn’t take or place bets.</p>
    </div>
    <figure class="setpiece">
      <div class="bezel">
        <div class="screen" role="img" aria-label="{html.escape(A_LABEL)}">
          {picture()}
          {scorebug()}
          {tape("glass")}
        </div>
      </div>
      <figcaption><b>Sample data.</b> Made-up names and numbers.</figcaption>
    </figure>
  </div>
</section>''',
)

OPT_B = opt_page(
    "b",
    "Option B",
    "Your crew’s prediction-market picks: a name, the chance, and the score. HuddleTape doesn’t take or place bets. 21+.",
    f'''<section class="poster" aria-labelledby="hero-h">
  <div class="wrap poster-copy">
    <p class="kicker">Coming soon</p>
    <h1 id="hero-h">Read the <span class="ink">tape.</span></h1>
  </div>
  <div class="crawl" role="img" aria-label="{html.escape(B_LABEL)}">
    {tape("band")}
  </div>
  <div class="wrap poster-sub">
    <p class="lede">Your crew’s prediction-market picks: a name, the chance, and the score.</p>
    <p class="plain">HuddleTape doesn’t take or place bets.</p>
    <p class="sample-note"><b>Sample data.</b> Made-up names and numbers.</p>
  </div>
</section>''',
)

OPT_C = opt_page(
    "c",
    "Option C",
    "Your name on a friend’s prediction-market pick, with the chance and the score. HuddleTape doesn’t take or place bets. 21+.",
    f'''<section class="glasshero" aria-labelledby="hero-h">
  <div class="glass-grid">
    <div class="hero-copy">
      <p class="kicker">Coming soon</p>
      <h1 id="hero-h">Their pick.<br>Your name.</h1>
      <p class="lede">Your name on a friend’s prediction-market pick, with the chance and the score.</p>
      <p class="plain">HuddleTape doesn’t take or place bets.</p>
    </div>
    <figure class="frame">
      <div class="screen screen-bleed" role="img" aria-label="{html.escape(C_LABEL)}">
        {picture(tight=True)}
        <div class="topbugs" aria-hidden="true">
          {scorebug()}
        </div>
        <div class="stack" aria-hidden="true">
          <div class="l3">
            <div class="l3-copy">
              <p class="l3-who">Priya</p>
              <p class="l3-pick">Moose −2.5</p>
              <p class="l3-meta">Q3 · 21–14</p>
            </div>
            <div class="l3-stat">
              <p class="l3-pct">63%</p>
              <p class="l3-move"><span class="tick up">▲5</span></p>
            </div>
            <div class="l3-support">
              <img src="/assets/img/tailer.webp" alt="" width="220" height="145">
              <span class="l3-with">with</span>
              <span class="l3-you">Jordan</span>
            </div>
          </div>
          {tape("glass")}
        </div>
      </div>
    </figure>
  </div>
  <p class="wrap sample-note"><b>Sample data.</b> Made-up names and numbers.</p>
</section>''',
)

MOTTO = "Your picks. Your screen. Your moment."


def htc(who, color, pick, pct, tick, direction, stake):
    return (
        f'<article class="htc" style="--who:{color}">'
        f'<div class="htc-main">'
        f'<p class="htc-tag">Game</p>'
        f'<p class="htc-who">{who}</p>'
        f'<p class="htc-pick">{pick}</p>'
        f'<p class="htc-chance"><span class="num">{pct}</span><span class="word">chance</span>'
        f'<span class="tick {direction}">{tick}</span></p>'
        f'<p class="htc-stake">{stake}</p>'
        f'</div></article>'
    )


def leg(n, pick, pct, tick, direction):
    return (
        f'<li><span class="n">{n}</span><span class="pk">{pick}</span>'
        f'<span class="end"><span class="lp">{pct}</span><span class="tick {direction}">{tick}</span></span></li>'
    )


def htc_parlay():
    return f'''<article class="htc htc-parlay" style="--who:#FF3EA5">
      <div class="htc-main">
        <p class="htc-tag">Game</p>
        <p class="htc-who">Priya</p>
        <p class="htc-pick">4-leg parlay</p>
        <p class="htc-chance"><span class="num">50%</span><span class="word">chance</span><span class="tick up">▲26</span></p>
        <p class="htc-stake">$5 → $20 · now $10</p>
      </div>
      <ol class="htc-legs">
        {leg(1, "Joss 1+ H", "60%", "▲2", "up")}
        {leg(2, "Maren 1+ H", "63%", "▲4", "up")}
        {leg(3, "Ellis 5+ K", "83%", "▲5", "up")}
        {leg(4, "Nova 13+ K", "62%", "▼8", "dn")}
      </ol>
    </article>'''


def htc_seq():
    cards = [
        htc("Kayla", "#F0C14A", "Owls −6.5", "71%", "▲4", "up", "$8 → $15 · now $11"),
        htc_parlay(),
        htc("Marcus", "#2DE2FF", "Over 47.5", "64%", "▲12", "up", "$5 → $9 · now $7"),
        htc("Andre", "#B6FF3B", "Gulls +3.5", "41%", "▼8", "dn", "$10 → $19 · now $6"),
        htc("Lena", "#FFE7A8", "Moose −3", "58%", "▲1", "up", "$6 → $11 · now $8"),
    ]
    return "".join(cards)


D_LABEL = (
    "Sample data. A slim tape of HuddleTape cards. "
    "Kayla, Owls minus 6.5, 71 percent chance, up 4. "
    "Priya’s 4-leg parlay, 50 percent chance, up 26. "
    "Joss 1 plus hits, 60 percent, up 2. Maren 1 plus hits, 63 percent, up 4. "
    "Ellis 5 plus strikeouts, 83 percent, up 5. Nova 13 plus strikeouts, 62 percent, down 8. "
    "Marcus, over 47.5, 64 percent, up 12. "
    "Andre, Gulls plus 3.5, 41 percent, down 8. "
    "Lena, Moose minus 3, 58 percent, up 1. Made-up names and numbers."
)

def notify_section():
    auto = html.escape(NOTIFY_AUTORESPONSE, quote=True)
    return f"""<section class="notify" aria-labelledby="notify-h">
  <p class="notify-line" id="notify-h">Be the first to get notified when beta signups go live.</p>
  <form class="signup notify-form" id="notify-form" action="https://formsubmit.co/{EMAIL}" method="POST" aria-describedby="form-note-notify">
    <input type="hidden" name="_subject" value="HuddleTape notify-me signup">
    <input type="hidden" name="_next" value="{URL}/notified.html">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_template" value="table">
    <input type="hidden" name="_autoresponse" value="{auto}">
    <input type="hidden" name="source" value="notify-me">
    <div class="hp" aria-hidden="true">
      <label for="hp-notify">Leave this field empty</label>
      <input type="text" id="hp-notify" name="_honey" tabindex="-1" autocomplete="off">
    </div>
    <div class="notify-row">
      <div class="field">
        <label for="email-notify">Email</label>
        <input type="email" id="email-notify" name="email" autocomplete="email" inputmode="email" required maxlength="120" placeholder="you@example.com">
      </div>
      <button class="btn btn-primary" type="submit">Notify me</button>
    </div>
    <p class="fineprint" id="form-note-notify">We’ll only email you about HuddleTape.</p>
  </form>
</section>"""


NOTIFY_EVENT = """<script>
document.getElementById("notify-form").addEventListener("submit", function () {
  var gc = window.goatcounter;
  if (gc && typeof gc.count === "function") {
    gc.count({
      path: "notify-me-submit",
      title: "HuddleTape notify-me signup",
      event: true
    });
  }
});
</script>
"""


def poster_page(path, robots):
    return (
        head(
            MOTTO,
            MOTTO,
            path,
            robots,
            extra='<link rel="stylesheet" href="/assets/options.css">\n',
            body_class="opt opt-d",
        )
        + f'''<main class="poster" id="main">
  <div class="brandlock">
    <img class="sigil" src="/assets/img/mark.svg" alt="" width="560" height="340">
    <img class="name" src="/assets/img/wordmark.svg" alt="HuddleTape" width="483" height="98">
  </div>
  <div class="glassbox" role="img" aria-label="{html.escape(D_LABEL)}">
    <div class="ht-rail" aria-hidden="true">
      <div class="ht-track"><div class="ht-seq">{htc_seq()}</div><div class="ht-seq">{htc_seq()}</div></div>
    </div>
  </div>
  <div class="lines">
    <h1>
      <span class="phrase">Your picks.</span>
      <span class="phrase">Your screen.</span>
      <span class="phrase accent">Your moment.</span>
    </h1>
    <p class="tuned">Stay tuned.</p>
  </div>
  {notify_section()}
</main>
<footer class="legal-slim">
  <p><span class="age">21+</span> Play responsibly. Set a budget before kickoff. Problem gambling? Call or text <a href="tel:18006973738">1-800-MY-RESET</a>. <a href="/privacy.html">Privacy</a> <a href="/terms.html">Terms</a></p>
</footer>
{NOTIFY_EVENT}</body>
</html>
'''
    )


def notified_page():
    return (
        head(
            "You're on the list",
            "We’ll email you when beta signups go live.",
            "/notified.html",
            "noindex",
            extra='<link rel="stylesheet" href="/assets/options.css">\n',
            body_class="opt opt-d",
        )
        + """<main class="poster" id="main">
  <div class="brandlock">
    <img class="sigil" src="/assets/img/mark.svg" alt="" width="560" height="340">
    <img class="name" src="/assets/img/wordmark.svg" alt="HuddleTape" width="483" height="98">
  </div>
  <div class="lines">
    <h1>You’re on the list.</h1>
    <p class="notify-thanks">We’ll email you when beta signups go live.</p>
    <a class="btn btn-primary" href="/">Back to HuddleTape</a>
  </div>
</main>
<footer class="legal-slim">
  <p><span class="age">21+</span> Play responsibly. Set a budget before kickoff. Problem gambling? Call or text <a href="tel:18006973738">1-800-MY-RESET</a>. <a href="/privacy.html">Privacy</a> <a href="/terms.html">Terms</a></p>
</footer>
</body>
</html>
"""
    )


OPT_D = poster_page("/_options/d.html", "noindex,nofollow")
with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as fh:
    fh.write(poster_page("/", "index,follow"))
print("index.html ok")
with open(os.path.join(SITE, "notified.html"), "w", encoding="utf-8") as fh:
    fh.write(notified_page())
print("notified.html ok")

opt_dir = os.path.join(SITE, "_options")
os.makedirs(opt_dir, exist_ok=True)
for name, content in {"a.html": OPT_A, "b.html": OPT_B, "c.html": OPT_C, "d.html": OPT_D}.items():
    with open(os.path.join(opt_dir, name), "w", encoding="utf-8") as fh:
        fh.write(content)
    print("_options/" + name, "ok")
