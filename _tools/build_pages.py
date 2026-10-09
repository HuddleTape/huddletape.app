"""Builds the HTML pages (shared header/footer). Run: python3 _tools/build_pages.py  (not deployed)"""
import os, segno, html
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'https://huddletape.app'
EMAIL = 'huddletape.app@gmail.com'
DESC = ("HuddleTape puts your crew's picks on a neon ticker over whatever's on your Google TV. "
        "Friends scan a QR to join from their phone. No app needed. Private beta this fall. 21+.")

# QR -> beta signup (the demo TV's QR actually works)
def qr_svg():
    q = segno.make(URL + '/#beta', error='m', micro=False)
    m = q.matrix; n = len(m)
    d = ''.join(f'M{x},{y}h1v1h-1z' for y, row in enumerate(m) for x, v in enumerate(row) if v)
    return (f'<svg viewBox="0 0 {n} {n}" role="img" aria-label="QR code linking to the HuddleTape beta signup" '
            f'shape-rendering="crispEdges"><path d="{d}" fill="#0A0614"/></svg>')

def head(title, desc=DESC, path='/', robots='index,follow'):
    full = title if title.startswith('HuddleTape') else f'{title} · HuddleTape'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{full}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0A0614">
<link rel="canonical" href="{URL}{path}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="HuddleTape">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{URL}{path}">
<meta property="og:image" content="{URL}/assets/img/og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="HuddleTape wordmark over a neon ticker of sample picks on a TV">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@HuddleTape">
<meta name="twitter:title" content="{full}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{URL}/assets/img/og-card.png">
<link rel="preload" href="/assets/fonts/anton.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/barlow-sc-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="HuddleTape home">
      <img class="mark" src="/assets/img/mark.svg" alt="" width="38" height="23">
      <img class="word" src="/assets/img/wordmark.svg" alt="HuddleTape" width="108" height="22">
    </a>
    <nav class="nav" aria-label="Main">
      <a class="hide-sm" href="/#how">How it works</a>
      <a class="hide-sm" href="/#faq">FAQ</a>
      <a class="btn btn-primary btn-sm" href="/#beta">Join the beta</a>
    </nav>
  </div>
</header>
'''

FOOT = f'''<footer class="foot">
  <div class="wrap row">
    <div>
      <img class="word" src="/assets/img/wordmark.svg" alt="HuddleTape" width="118" height="24">
      <p>The watch-party ticker for Google TV.</p>
    </div>
    <div>
      <p class="rg"><b>21+</b> · Play responsibly · Problem gambling? Call or text <a href="tel:18006973738">1-800-MY-RESET</a></p>
      <p>HuddleTape doesn't take or place wagers and isn't a sportsbook. Not affiliated with any sportsbook, exchange, team or league. Ticker images show sample data.</p>
      <nav aria-label="Footer">
        <a href="/privacy.html">Privacy</a>
        <a href="/terms.html">Terms</a>
        <a href="/#beta">Join the beta</a>
        <a href="mailto:{EMAIL}">Support: {EMAIL}</a>
      </nav>
      <p>© 2026 HuddleTape LLC</p>
    </div>
  </div>
</footer>
</body>
</html>
'''

def card(who, what, right, hot=False, extra=''):
    return f'<div class="card{" hot" if hot else ""}"><span class="who">{who}</span><span class="what">{what}</span>{right}{extra}</div>'

def ticker_cards():
    pct = lambda side, p, ch, cls='up': (f'<span class="side{" no" if side == "NO" else ""}">{side}</span>' if side else '') + f'<span class="pct">{p}</span><span class="ch">chance</span><span class="{cls}">{ch}</span>'
    return ''.join([
        card('BIG TEX', 'Owls to win', pct('YES', '62%', '▲9'), hot=True, extra='<span class="tagpill">SAM</span>'),
        card('COACH DEE', 'Gulls +3.5', '<span class="won">WON</span>'),
        card('KAYLA', '3-pick combo', '<span class="dots" aria-hidden="true"><i class="ok"></i><i class="ok"></i><i></i></span>' + pct('', '21%', '▲4')),
        card('MOMO', 'Over 47.5 pts', pct('', '38%', '▼2', 'dn')),
        card('JAKE', 'Moose −2.5', pct('YES', '55%', '▲1')),
    ])

def demo():
    cards = ticker_cards()
    return f'''<figure class="demo">
  <div class="tv">
    <div class="screen" role="img" aria-label="Sample data: a TV showing a game with the HuddleTape ticker along the bottom. Cards scroll by for Big Tex (Owls to win, 62% chance), Coach Dee (Gulls +3.5, stamped WON), Kayla (3-pick combo, 21%), Momo (Over 47.5, 38%) and Jake (Moose −2.5, 55%). Tailer the dog trots past carrying a name tag, and a QR code invites friends to scan and add their picks.">
      <div class="crowd"></div>
      <div class="lights" aria-hidden="true"><i></i><i></i><i></i></div>
      <div class="field"></div><div class="ball"></div>
      <span class="sample-tag" aria-hidden="true">SAMPLE DATA</span>
      <div class="tailer-run" aria-hidden="true"><div class="dog"></div><span class="tagpill">SAM</span></div>
      <div class="ticker" aria-hidden="true">
        <div class="tk-brand"><img src="/assets/img/mark.svg" alt=""></div>
        <div class="tk-rail"><div class="tk-track">{cards}{cards}</div></div>
        <div class="qr">{qr_svg()}<div><div class="q1">Scan to add<br>your picks</div><div class="q2">ROOM</div><div class="q3">FARM</div></div></div>
      </div>
    </div>
  </div>
  <figcaption><b>SAMPLE DATA</b> · Made-up names, teams and numbers. Your game stays on screen.</figcaption>
</figure>'''

TV_ICO = '<svg class="ico" viewBox="0 0 54 54" aria-hidden="true"><rect x="4" y="8" width="46" height="30" rx="4" fill="none" stroke="#2DE2FF" stroke-width="3"/><path d="M10 31h34" stroke="#FF3EA5" stroke-width="3" stroke-linecap="round"/><path d="M19 46h16" stroke="#2DE2FF" stroke-width="3" stroke-linecap="round"/></svg>'
QR_ICO = '<svg class="ico" viewBox="0 0 54 54" aria-hidden="true"><g fill="none" stroke="#B6FF3B" stroke-width="3"><rect x="6" y="6" width="16" height="16" rx="2"/><rect x="32" y="6" width="16" height="16" rx="2"/><rect x="6" y="32" width="16" height="16" rx="2"/></g><g fill="#B6FF3B"><rect x="32" y="32" width="6" height="6"/><rect x="42" y="42" width="6" height="6"/><rect x="42" y="32" width="6" height="6"/><rect x="32" y="42" width="6" height="6"/></g></svg>'
TK_ICO = '<svg class="ico" viewBox="0 0 54 54" aria-hidden="true"><rect x="3" y="18" width="48" height="18" rx="4" fill="none" stroke="#FF3EA5" stroke-width="3"/><path d="M9 27h10M23 27h14M41 27h5" stroke="#F5F0FF" stroke-width="3" stroke-linecap="round"/></svg>'

def form(source):
    return f'''<form class="signup" action="https://formsubmit.co/{EMAIL}" method="POST" aria-describedby="form-note-{source}">
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
    <input type="email" id="email-{source}" name="email" autocomplete="email" required maxlength="120" placeholder="you@example.com">
  </div>
  <div class="field">
    <label for="tv-{source}">TV or streamer <span class="opt">(optional)</span></label>
    <input type="text" id="tv-{source}" name="tv_device" maxlength="100" placeholder="e.g. Onn 4K, Google TV Streamer" aria-describedby="tv-hint-{source}">
    <span class="hint" id="tv-hint-{source}">Helps us check your setup will work. Fire TV and Roku aren't supported yet.</span>
  </div>
  <label class="check" for="age-{source}">
    <input type="checkbox" id="age-{source}" name="confirmed_21_plus" value="yes" required>
    <span>I'm 21 or older and agree to the <a href="/terms.html">Terms</a> and <a href="/privacy.html">Privacy Policy</a>.</span>
  </label>
  <button class="btn btn-primary" type="submit">Join the beta</button>
  <p class="fineprint" id="form-note-{source}">We'll only email you about the HuddleTape beta and launch. Unsubscribe anytime by replying "stop".</p>
</form>'''

def beta_section(source, heading_tag='h2'):
    return f'''<section class="sec" id="beta" aria-labelledby="beta-h">
  <div class="wrap beta">
    <div>
      <{heading_tag} id="beta-h">Join the <span class="pk">private beta</span></{heading_tag}>
      <p class="intro" style="margin-bottom:0">We're opening HuddleTape to a small group of Google TV hosts around Thanksgiving, then launching on Google Play in January 2027. Grab a spot and help shape it.</p>
      <ul class="perks">
        <li>Early access for you and your whole crew</li>
        <li>Free during the beta</li>
        <li>A direct line to the team: tell us what to build next</li>
      </ul>
    </div>
    {form(source)}
  </div>
</section>'''

INDEX = head('HuddleTape · Your crew\u2019s bets, live on the TV') + f'''<main id="main">
<section class="hero" aria-labelledby="hero-h">
  <div class="wrap">
    <div>
      <span class="eyebrow">Watch-party ticker for Google TV</span>
      <img class="hero-word" src="/assets/img/wordmark.svg" alt="HuddleTape" width="420" height="85">
      <h1 id="hero-h">Your crew’s bets, <em>live on the TV.</em></h1>
      <p class="lede">HuddleTape floats a neon ticker over whatever’s on. Friends scan a QR, join in their browser, and the whole room sweats every pick together. Wins get a quiet WON stamp. Losses crack and fall. Tailer shows up when someone rides along.</p>
      <div class="cta-row">
        <a class="btn btn-primary" href="#beta">Join the beta</a>
        <a class="btn btn-ghost" href="#how">How it works</a>
      </div>
      <ul class="chips" aria-label="Highlights">
        <li>No phone app needed</li><li>Join from any phone browser</li><li>Google TV &amp; Android TV</li>
      </ul>
    </div>
    {demo()}
  </div>
</section>

<section class="sec" id="how" aria-labelledby="how-h">
  <div class="wrap">
    <h2 id="how-h">How it <span class="pk">works</span></h2>
    <p class="intro">Three steps, and nobody passes a phone around.</p>
    <ol class="steps">
      <li><span class="n">1</span>{TV_ICO}<h3>Put it on the TV</h3><p>Open HuddleTape on your Google TV and start a room. The ticker sits along the bottom of the screen, over the game.</p></li>
      <li><span class="n">2</span>{QR_ICO}<h3>Scan the QR code</h3><p>Friends point their phone camera at the code on the TV and join in the browser. No app, no account to set up.</p></li>
      <li><span class="n">3</span>{TK_ICO}<h3>Your picks scroll live</h3><p>Drop in a screenshot of the picks you already made and watch them ride the ticker with a live % chance.</p></li>
    </ol>
  </div>
</section>

<section class="sec" id="features" aria-labelledby="feat-h">
  <div class="wrap">
    <h2 id="feat-h">Built to be <span class="pk">watched</span></h2>
    <p class="intro">Everybody’s sweat, one screen. The game stays front and center.</p>
    <div class="features">
      <article class="feat">
        <div class="vis" aria-hidden="true"><div class="phone-ico"></div><span class="arrow">→</span><div class="mini"><span>KAYLA</span><span style="color:var(--muted);font-weight:500">3-pick combo</span></div></div>
        <h3>Screenshot import</h3>
        <p>Snap the slip you already have and HuddleTape reads the picks for you. Screenshots are read on your phone and never uploaded.</p>
      </article>
      <article class="feat">
        <div class="vis" aria-hidden="true"><div class="mini"><span>BIG TEX</span><span class="side">YES</span><span class="pct">62%</span><span class="up">▲9</span></div></div>
        <h3>Live % chance</h3>
        <p>Every pick shows a live chance that moves as the game does, so the room knows exactly where things stand.</p>
      </article>
      <article class="feat">
        <div class="vis" aria-hidden="true"><div class="tailer-wag"></div><span class="tagpill" style="font:700 .9rem/1 Chakra,sans-serif;color:var(--lime);border:2px solid var(--cyan);border-radius:99px;padding:.35rem .7rem;box-shadow:0 0 10px rgba(45,226,255,.6)">SAM</span></div>
        <h3>Meet Tailer</h3>
        <p>Riding along with a friend’s pick? Tailer, our golden retriever, trots across the ticker and drops your name tag on it.</p>
      </article>
      <article class="feat half">
        <div class="vis" aria-hidden="true"><span class="pill-won">WON</span><span class="crack">Over 47.5</span></div>
        <h3>Quiet wins, dramatic losses</h3>
        <p>A settled winner gets a small WON stamp and a soft glow. A miss cracks and falls off the ticker. No confetti blocking the replay.</p>
      </article>
      <article class="feat wide">
        <div class="vis" aria-hidden="true"><div class="layers"><div class="app"><span>ANY APP</span></div><div class="bar"><i style="width:22%"></i><i style="width:14%;background:var(--lime)"></i><i style="width:30%"></i></div></div></div>
        <h3>Works over any app</h3>
        <p>The ticker floats over live TV, streaming apps and multiview. Keep watching what you want; HuddleTape just rides along at the bottom.</p>
      </article>
    </div>
  </div>
</section>

<section class="sec" id="compat" aria-labelledby="compat-h">
  <div class="wrap">
    <div class="compat">
      <div>
        <h2 id="compat-h">Built for <span class="pk">Google TV</span></h2>
        <p>HuddleTape runs on Google TV and Android TV devices that allow “Display over other apps.” Friends only need a phone with a camera and a web browser.</p>
        <p>Got another kind of TV? A Google TV streamer plugs into any HDMI port and you’re in.</p>
      </div>
      <ul class="yesno">
        <li class="y"><b>✓</b>Google TV streamers and TVs</li>
        <li class="y"><b>✓</b>Android TV devices</li>
        <li class="y"><b>✓</b>Guests: any phone browser, no app</li>
        <li class="n"><b>—</b>Fire TV, Roku, Apple TV and Samsung/LG smart-TV apps: not supported yet</li>
      </ul>
    </div>
  </div>
</section>

<section class="sec" id="faq" aria-labelledby="faq-h">
  <div class="wrap">
    <h2 id="faq-h">Questions, <span class="pk">answered</span></h2>
    <div class="faq">
      <details><summary>Is HuddleTape a sportsbook?</summary><p>No. HuddleTape doesn’t take, place or settle wagers, and you can’t bet through it. It’s a watch-party display that shows picks your crew already made somewhere else, for fun and conversation.</p></details>
      <details><summary>Do my friends need to download anything?</summary><p>No. They scan the QR code on the TV and join from their phone’s web browser.</p></details>
      <details><summary>What does it cost?</summary><p>The beta is free. At launch, the TV host gets a 30-day free trial, then a small subscription. Final pricing will be posted before launch. Guests never pay.</p></details>
      <details><summary>Which TVs does it work on?</summary><p>Google TV and Android TV devices. Fire TV, Roku, Apple TV and Samsung/LG apps aren’t supported yet. A Google TV streamer on any HDMI TV works great.</p></details>
      <details><summary>Will everyone see how much I put down?</summary><p>Dollar amounts are off by default, so the ticker shows names, picks and % chance. You can hide your picks from the ticker anytime.</p></details>
      <details><summary>What happens to my screenshots and account info?</summary><p>Screenshots are read on your phone and never uploaded. If you connect an account, access is read-only and the key is stored only on your TV. See the <a href="/privacy.html">Privacy Policy</a>.</p></details>
      <details><summary>When can I get it?</summary><p>The private beta starts around Thanksgiving 2026, and the public Google Play launch is planned for January 2027. <a href="#beta">Join the beta</a> to get in early.</p></details>
    </div>
  </div>
</section>

{beta_section('home')}
</main>
''' + FOOT

BETA = head('Join the beta', 'Sign up for the HuddleTape private beta: a neon watch-party ticker for Google TV. 21+.', '/beta.html') + f'''<main id="main">
{beta_section('beta-page', 'h1')}
</main>
''' + FOOT

THANKS = head("You're on the list", "Thanks for joining the HuddleTape beta.", '/thanks.html', 'noindex') + '''<main id="main" class="wrap center-page">
  <div>
    <img src="/assets/img/tailer.png" alt="Tailer, the HuddleTape golden retriever, wagging his tail" width="220" height="145" style="margin:0 auto">
    <h1>You’re on the list.</h1>
    <p>Thanks for signing up for the HuddleTape beta. We’ll email you when your spot opens, around Thanksgiving. Tell your crew: every room needs a host.</p>
    <a class="btn btn-ghost" href="/">Back to HuddleTape</a>
  </div>
</main>
''' + FOOT

NOTFOUND = head('Page not found', 'This page fumbled.', '/404.html', 'noindex') + '''<main id="main" class="wrap center-page">
  <div>
    <h1>This page fumbled.</h1>
    <p>We couldn’t find that page.</p>
    <a class="btn btn-primary" href="/">Back to HuddleTape</a>
  </div>
</main>
''' + FOOT

def legal(title, path, updated, body):
    return head(title + ' (Draft)', f'HuddleTape {title.lower()}: draft pending attorney review.', path, 'noindex') + f'''<main id="main" class="legal">
  <div class="wrap">
    <p class="draft-banner" role="note">DRAFT — pending attorney review. This document is not final and may change before HuddleTape launches.</p>
    <h1>{title}</h1>
    <p class="meta">Draft dated {updated} · HuddleTape LLC</p>
    {body}
  </div>
</main>
''' + FOOT

PRIVACY = legal('Privacy Policy', '/privacy.html', 'October 9, 2026', f'''
<p>HuddleTape LLC (“HuddleTape,” “we,” “us”) makes a watch-party app for Google TV and Android TV, a phone-browser join page for guests, and this website. This policy explains what we collect, why, and the choices you have. We wrote it in plain English on purpose.</p>

<h2>The short version</h2>
<ul>
  <li><strong>We don’t sell your data</strong>, and we don’t share it for cross-context advertising.</li>
  <li><strong>Screenshots stay on your phone.</strong> They’re read on your device and never uploaded to us.</li>
  <li><strong>Connected accounts are read-only.</strong> Any key you add is stored only on your TV, not on our servers.</li>
  <li>We collect a small amount of usage and crash data to keep the app working.</li>
  <li>HuddleTape is for adults 21 and older.</li>
</ul>

<h2>What we collect</h2>
<p><strong>Beta signup (this website).</strong> When you join the beta, we receive your name, email address, the TV or streamer model if you give it, and your confirmation that you’re 21 or older. The form is delivered to our email through a form-forwarding service (FormSubmit), which processes it under its own privacy policy.</p>
<p><strong>In a watch party.</strong> To show the ticker, the TV and guests’ phones exchange what’s needed for the room: the room code, the display name and color each guest picks, and the picks guests choose to add (for example, the selection, the % chance and whether it settled). Dollar amounts are hidden unless the person who added the pick turns them on. Room data is kept only as long as needed to run the party and is not used to build a profile of you.</p>
<p><strong>Screenshots.</strong> When you import a screenshot, the text is read on your phone in the browser. The image itself is never uploaded to HuddleTape. Only the picks you confirm are sent to the room.</p>
<p><strong>Connected accounts.</strong> If you choose to connect an account from another service to pull in your open picks, the connection is read-only: HuddleTape can’t place, change or cancel anything. The key or credential is stored only on your TV. We don’t receive it, and you can remove it at any time in the TV app’s settings.</p>
<p><strong>Analytics and crash reports.</strong> The apps and website may collect standard, limited usage data (like which screens are used, device model, OS version, app version and approximate region) and crash reports, through providers such as Google’s Firebase. We use this to fix bugs and improve the product, not to advertise to you.</p>
<p><strong>Purchases.</strong> Subscriptions are handled by Google Play. We get confirmation of your subscription status, not your payment card details.</p>
<p><strong>Support.</strong> If you email us, we keep the conversation so we can help you.</p>

<h2>How we use it</h2>
<ul>
  <li>To run watch parties and show the ticker.</li>
  <li>To run the beta: inviting you, sending setup instructions and asking for feedback.</li>
  <li>To fix crashes, keep the service secure and improve features.</li>
  <li>To send occasional product updates about the beta and launch. You can opt out anytime.</li>
  <li>To comply with the law and enforce our <a href="/terms.html">Terms</a>.</li>
</ul>

<h2>Sharing</h2>
<p>We share data only with service providers that help us run HuddleTape (for example hosting, form delivery, email, analytics and crash reporting), under contracts or terms that limit their use of it; when the law requires it; or as part of a merger or sale of the business, in which case this policy still applies to your data. <strong>We don’t sell personal information.</strong> Anything you put on the ticker is visible to the people in the room and anyone who can see the TV, so choose what you share.</p>

<h2>Retention</h2>
<p>We keep beta signup info until the beta and launch are over or you ask us to delete it. Analytics and crash data are kept in limited form for as long as they’re useful for fixing and improving the product. Room data is short-lived.</p>

<h2>Your choices and rights</h2>
<ul>
  <li>Ask us for a copy of your data, or to correct or delete it, by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</li>
  <li>Unsubscribe from beta emails at any time.</li>
  <li>Remove a connected account key from the TV app at any time.</li>
  <li>Hide your picks from the ticker, or leave the room.</li>
</ul>
<p>Depending on where you live (for example Texas or California), you may have additional rights under state privacy law. We’ll honor them, and we won’t treat you differently for using them.</p>

<h2>Age</h2>
<p>HuddleTape is only for people 21 and older. We don’t knowingly collect information from anyone under 21. If you believe someone under 21 has given us information, contact us and we’ll delete it.</p>

<h2>Security</h2>
<p>We use reasonable safeguards to protect information, but no system is perfectly secure.</p>

<h2>Changes</h2>
<p>We’ll update this page when our practices change and note the date at the top. For significant changes, we’ll give notice in the app or by email.</p>

<h2>Contact</h2>
<p>HuddleTape LLC · Texas, USA · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
''')

TERMS = legal('Terms of Use', '/terms.html', 'October 9, 2026', f'''
<p>These terms are an agreement between you and HuddleTape LLC (“HuddleTape,” “we,” “us”) for using the HuddleTape TV app, the guest join page and this website (together, the “Service”). By using the Service, you agree to them.</p>

<h2>1. You must be 21 or older</h2>
<p>You must be at least 21 years old to use HuddleTape, including as a guest. By using it, you confirm that you are.</p>

<h2>2. What HuddleTape is, and isn’t</h2>
<p>HuddleTape is a <strong>social and entertainment</strong> display for watching sports with friends. It shows picks that you and your friends already made elsewhere on a ticker on your TV.</p>
<ul>
  <li><strong>HuddleTape is not a sportsbook, exchange or gambling service.</strong> It does not accept, place, broker or settle wagers, hold funds, or pay out winnings.</li>
  <li><strong>You can’t bet through HuddleTape.</strong> Any account you connect is read-only.</li>
  <li>HuddleTape doesn’t give betting advice, tips or recommendations, and nothing in the Service is one.</li>
  <li>HuddleTape is not affiliated with, endorsed by or sponsored by any sportsbook, exchange, team or league.</li>
</ul>
<p>You are responsible for following the laws where you live, and the rules of any service you use separately.</p>

<h2>3. No guarantees</h2>
<p>Percent chances, prices, scores and results shown on the ticker come from third-party sources or from what users enter, may be delayed or wrong, and are for entertainment only. Don’t rely on them for any decision. The Service is provided <strong>“as is” and “as available,”</strong> without warranties of any kind, to the fullest extent the law allows. We don’t guarantee that it will be uninterrupted, error-free or available on every device.</p>

<h2>4. Your content and your room</h2>
<p>You’re responsible for what you add to a room, including display names and picks. Don’t post anything unlawful, harassing or that you don’t have the right to share, and don’t add someone else’s picks without their OK. The host can remove guests and content. Anything on the TV can be seen by people in the room.</p>

<h2>5. Accounts and keys</h2>
<p>If you connect an account from another service, you confirm you’re allowed to, and you can remove the connection at any time. Keys are stored only on your TV. Keep your TV and accounts secure.</p>

<h2>6. Beta</h2>
<p>Beta versions are early, may have bugs and may change or stop working. Feedback you send us can be used to improve HuddleTape without obligation to you.</p>

<h2>7. Subscriptions</h2>
<p>Guests are free. The TV host may need a subscription after a free trial. Subscriptions are sold and billed through Google Play, renew automatically until you cancel, and are subject to Google Play’s terms and refund policies. We’ll show the price before you subscribe.</p>

<h2>8. Acceptable use</h2>
<p>Don’t misuse the Service: no reverse engineering except where the law allows it, no interfering with other users or our systems, no automated scraping, and no use by anyone under 21.</p>

<h2>9. Responsible play</h2>
<p>HuddleTape is meant to make watching more fun, not to encourage gambling. Set a budget before kickoff. If gambling stops being fun, call or text <strong>1-800-MY-RESET</strong> (1-800-697-3738) for free, confidential help.</p>

<h2>10. Limitation of liability</h2>
<p>To the fullest extent the law allows, HuddleTape won’t be liable for indirect, incidental, special, consequential or punitive damages, or for any losses related to wagers or decisions you make, and our total liability for any claim is limited to the amount you paid us in the 12 months before the claim, or $50, whichever is greater.</p>

<h2>11. Ending use</h2>
<p>You can stop using HuddleTape at any time. We may suspend or end access if you break these terms or to protect the Service or other users.</p>

<h2>12. Changes and governing law</h2>
<p>We may update these terms and will note the date at the top. These terms are governed by the laws of the State of Texas, without regard to conflict-of-law rules.</p>

<h2>13. Contact</h2>
<p>HuddleTape LLC · Texas, USA · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
''')

for name, content in {'index.html': INDEX, 'beta.html': BETA, 'thanks.html': THANKS, '404.html': NOTFOUND,
                      'privacy.html': PRIVACY, 'terms.html': TERMS}.items():
    open(os.path.join(SITE, name), 'w').write(content)
print('pages ok')
