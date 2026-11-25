"""Shared building blocks for the Virtual Physio static site.

Run `python3 _dev/build/build.py` from the repo root to regenerate pages.
"""
import html
import json

SITE = "https://virtualphysio.ca"
PHONE_DISPLAY = "+1 (343) 202-4226"
PHONE_TEL = "+13432024226"
EMAIL = "info@virtualphysio.ca"
WHATSAPP = "https://wa.me/13432024226"
HOURS = "Mon–Sat, 9:00 AM–7:00 PM"
OG_IMAGE = f"{SITE}/img/og-virtual-physio.jpg"
import hashlib as _h, os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", ".."))
# Version = hash of the CSS/JS files, so browsers always fetch the newest copy after a change.
CSS_VERSION = _h.md5(b"".join(open(_os.path.join(_ROOT, f), "rb").read() for f in ("style.css", "refresh.css", "script.js"))).hexdigest()[:10]

AREAS = [
    "Ottawa", "Kanata", "Stittsville", "Barrhaven", "Nepean", "Orléans", "Gloucester",
    "Westboro", "Centretown", "Alta Vista", "Vanier", "Riverside South", "Findlay Creek",
    "Manotick", "Greely", "Rockcliffe Park", "Beacon Hill", "Blackburn Hamlet", "Hunt Club",
    "Carlington", "Hintonburg", "The Glebe", "Sandy Hill", "Overbrook", "Elmvale Acres",
    "South Keys", "Bells Corners",
]

ICONS = {
    "check": '<path d="M5 12l5 5L20 7"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
    "video": '<rect x="2.5" y="6" width="13" height="12" rx="2"/><path d="M15.5 10.5l6-3.5v10l-6-3.5"/>',
    "home": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "bandage": '<rect x="2" y="8" width="20" height="8" rx="4" transform="rotate(-45 12 12)"/><path d="M10 10h.01M14 14h.01M12 12h.01"/>',
    "pulse": '<path d="M3 12h4l3-8 4 16 3-8h4"/>',
    "run": '<circle cx="14" cy="4.5" r="2"/><path d="M8 21l3-6 3 2v5"/><path d="M6 12l3-4 4 1 3 3 3 1"/><path d="M11 15l-2-3"/>',
    "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "car": '<path d="M5 16V11l2-5h10l2 5v5"/><path d="M3 16h18v3H3z"/><circle cx="7.5" cy="16" r="1.5"/><circle cx="16.5" cy="16" r="1.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "spine": '<path d="M12 3v18"/><path d="M9 5h6M8.5 9h7M8.5 13h7M9 17h6"/>',
    "neck": '<circle cx="12" cy="6" r="3"/><path d="M10.5 9v3M13.5 9v3"/><path d="M6 20c0-4 2.7-7 6-7s6 3 6 7"/>',
    "joint": '<circle cx="12" cy="12" r="3"/><path d="M12 3v6M12 15v6"/><path d="M9 4h6M9 20h6"/>',
    "baby": '<circle cx="12" cy="8" r="4"/><path d="M5 21c1-4 3.8-6 7-6s6 2 7 6"/>',
    "dizzy": '<circle cx="12" cy="12" r="9"/><path d="M12 7a5 5 0 1 0 5 5"/><path d="M12 10a2 2 0 1 0 2 2"/>',
    "jaw": '<path d="M5 9c0-3.3 3.1-6 7-6s7 2.7 7 6v2c0 5-3.5 10-7 10s-7-5-7-10z"/><path d="M9 15h6"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5L15.5 10"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "clipboard": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4h6v3H9z"/><path d="M9 12h6M9 16h4"/>',
    "map": '<path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
    "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/>',
}


def icon(name, cls=""):
    return (f'<svg{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{ICONS[name]}</svg>')


def esc(s):
    return html.escape(s, quote=True)


def pic(name, alt, w, h, cls="", eager=False, sizes="100vw"):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source srcset="/img/{name}.webp" type="image/webp">'
            f'<img src="/img/{name}.jpg" alt="{esc(alt)}" width="{w}" height="{h}" {load} decoding="async"'
            f'{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}></picture>')


NAV = [("/services", "Services"), ("/about", "About"), ("/blog", "Resources"), ("/booking#contact", "Contact")]


def header(active):
    items = "\n".join(
        f'        <li><a href="{href}"{" aria-current=" + chr(34) + "page" + chr(34) if href == active else ""}>{label}</a></li>'
        for href, label in NAV) + '\n        <li class="nav-menu__book"><a href="/booking">Book an appointment</a></li>'
    return f'''  <a class="skip-link" href="#main">Skip to content</a>
  <div class="topbar">
    <div class="container topbar__inner">
      <span>Virtual &amp; in-home physiotherapy across Ottawa · {HOURS}</span>
      <span class="topbar__links"><a href="tel:{PHONE_TEL}" data-track="call_topbar">{icon("phone")}{PHONE_DISPLAY}</a><a href="{WHATSAPP}" rel="noopener" data-track="whatsapp_topbar">{icon("chat")}WhatsApp</a></span>
    </div>
  </div>
  <header class="site-header">
    <nav class="navbar container" aria-label="Main navigation">
      <a class="brand" href="/" aria-label="Virtual Physio home">
        <picture><source srcset="/img/logo.webp" type="image/webp"><img src="/img/logo.png" alt="Virtual Physio" width="480" height="213"></picture>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-menu" aria-label="Open navigation">
        <span></span><span></span><span></span>
      </button>
      <ul id="primary-menu" class="nav-menu">
{items}
      </ul>
      <a class="nav-cta" href="/booking" data-track="book_appointment_nav">Book now</a>
    </nav>
  </header>'''


from services_data import SERVICE_PAGES
FOOTER_SERVICES = [(s["nav"], f"/services/{s['slug']}") for s in SERVICE_PAGES]


def footer(posts):
    svc = "\n".join(f'          <li><a href="{u}">{t}</a></li>' for t, u in FOOTER_SERVICES)
    recent = "\n".join(f'          <li><a href="/blog/{p["slug"]}">{esc(p["short"])}</a></li>' for p in posts[:5])
    return f'''  <footer class="site-footer">
    <div class="container footer-grid">
      <div>
        <a class="footer-logo-pill" href="/" aria-label="Virtual Physio home"><picture><source srcset="/img/logo.webp" type="image/webp"><img src="/img/logo.png" alt="Virtual Physio" width="150" height="67" loading="lazy" style="width:150px;height:auto"></picture></a>
        <p>Virtual and in-home physiotherapy across Ottawa with Drashti Chauhan, PT. One-on-one care for pain, injury and recovery.</p>
        <p><a href="{WHATSAPP}" rel="noopener">Message us on WhatsApp</a></p>
      </div>
      <div>
        <h2>Services</h2>
        <ul>
{svc}
        </ul>
      </div>
      <div>
        <h2>From the blog</h2>
        <ul>
{recent}
          <li><a href="/blog">All articles &rarr;</a></li>
        </ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{HOURS}</li>
          <li>In-home visits: <a href="/areas/kanata">Kanata</a>, <a href="/areas/barrhaven">Barrhaven</a>, <a href="/areas/orleans">Orléans</a>, <a href="/areas/nepean">Nepean</a> and <a href="/areas">more</a></li>
          <li><a href="/booking">Book an appointment</a></li>
        </ul>
      </div>
    </div>
    <div class="container footer-bottom">
      <span>&copy; 2026 Virtual Physio, Ottawa, Ontario · <a href="/privacy">Privacy policy</a></span>
      <span>Not an emergency service. In an emergency, call 911. Photos are for illustration.</span>
    </div>
  </footer>
  <nav class="mobile-bar" aria-label="Quick contact">
    <a class="call" href="tel:{PHONE_TEL}" data-track="call_mobile_bar">{icon("phone")}<span>Call</span></a>
    <a class="wa" href="{WHATSAPP}" rel="noopener" data-track="whatsapp_mobile_bar">{icon("chat")}<span>WhatsApp</span></a>
    <a class="book" href="/booking" data-track="book_mobile_bar">Book now</a>
  </nav>'''


BUSINESS = {
    "@type": ["MedicalBusiness", "Physiotherapy"],
    "@id": f"{SITE}/#business",
    "name": "Virtual Physio",
    "url": f"{SITE}/",
    "telephone": PHONE_TEL,
    "email": EMAIL,
    "image": OG_IMAGE,
    "logo": f"{SITE}/img/logo.png",
    "medicalSpecialty": "Physiotherapy",
    "priceRange": "$$",
    "address": {"@type": "PostalAddress", "addressLocality": "Ottawa", "addressRegion": "ON", "addressCountry": "CA"},
    "areaServed": [{"@type": "City", "name": a} for a in ["Ottawa", "Kanata", "Barrhaven", "Nepean", "Orléans", "Stittsville", "Gloucester", "Manotick"]],
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "opens": "09:00", "closes": "19:00"}],
    "employee": {"@id": f"{SITE}/about#drashti"},
}

PERSON = {
    "@type": "Person",
    "@id": f"{SITE}/about#drashti",
    "name": "Drashti Chauhan",
    "jobTitle": "Registered Physiotherapist",
    "honorificSuffix": "PT",
    "image": f"{SITE}/img/drashti-chauhan.jpg",
    "worksFor": {"@id": f"{SITE}/#business"},
    "url": f"{SITE}/about",
}


def ld(*objs):
    graph = {"@context": "https://schema.org", "@graph": list(objs)}
    return '  <script type="application/ld+json">\n' + json.dumps(graph, ensure_ascii=False, indent=1) + '\n  </script>'


def breadcrumb_ld(trail):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + url}
            for i, (name, url) in enumerate(trail)
        ],
    }


def breadcrumb_html(trail):
    parts = []
    for i, (name, url) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f'<li aria-current="page">{esc(name)}</li>')
        else:
            parts.append(f'<li><a href="{url}">{esc(name)}</a></li>')
    return '<ol class="breadcrumb">' + "".join(parts) + '</ol>'


def faq_ld(faqs):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }


def faq_html(faqs):
    return '<div class="faq-list">\n' + "\n".join(
        f'          <details>\n            <summary>{esc(q)}</summary>\n            <p>{esc(a)}</p>\n          </details>'
        for q, a in faqs) + '\n        </div>'


def page(*, path, title, description, active, body, posts, schema="", og_image=OG_IMAGE, og_type="website",
         extra_head="", preload=""):
    url = SITE + path
    return f'''<!DOCTYPE html>
<html lang="en-CA">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#1f6fd1">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Virtual Physio">
  <meta property="og:locale" content="en_CA">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/img/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
{preload}  <link rel="stylesheet" href="/style.css?v={CSS_VERSION}">
  <link rel="stylesheet" href="/refresh.css?v={CSS_VERSION}">
{extra_head}{schema}
</head>
<body>
{header(active)}

  <main id="main">
{body}
  </main>

{footer(posts)}

  <script src="/script.js?v={CSS_VERSION}" defer></script>
</body>
</html>
'''


def cta_band(title="Ready to get started?", text="Book online in about a minute, or call or WhatsApp us. Have questions first? Book a free 15-minute intro call (general information only, not an assessment)."):
    return f'''    <section class="section section--tight">
      <div class="container">
        <div class="cta-band">
          <div>
            <h2>{title}</h2>
            <p>{text}</p>
          </div>
          <div class="button-row">
            <a class="btn btn-light" href="/booking" data-track="book_cta_band">Book an appointment</a>
            <a class="btn btn-ghost-light" href="tel:{PHONE_TEL}" data-track="call_cta_band">Call {PHONE_DISPLAY}</a>
          </div>
        </div>
      </div>
    </section>'''
