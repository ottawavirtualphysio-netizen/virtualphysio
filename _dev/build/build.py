"""Regenerate the Virtual Physio site.

Usage (from the repo root):  python3 _dev/build/build.py
Edits to page text belong in this folder; the generated .html files are overwritten.
booking.html and contact.html keep their own content: only their header/footer/head are refreshed.
"""
import math
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from common import *  # noqa
from posts_a import POSTS_A
from posts_b import POSTS_B
from posts_c import POSTS_C

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TODAY = "2026-11-25"

POSTS = POSTS_A + POSTS_B + POSTS_C
SEO_TITLES = {
    "in-home-physiotherapy-ottawa": "In-Home Physiotherapy in Ottawa: What to Expect",
    "post-surgery-rehabilitation-timeline": "Post-Surgery Rehab Timeline, Week by Week",
    "sports-injury-prevention": "Sports Injury Prevention: 8 Physio Tips",
    "tech-neck-posture-pain": "Tech Neck: Physio for Neck & Posture Pain",
    "pelvic-floor-physiotherapy": "Pelvic Floor Physiotherapy: What to Expect",
    "when-to-see-physiotherapist": "When to See a Physiotherapist After an Injury",
    "virtual-vs-in-person-physiotherapy": "Virtual vs In-Person Physiotherapy",
    "lower-back-pain-at-home": "Lower Back Pain: Home Care & When to See a Physio",
    "postpartum-core-recovery-diastasis-recti": "Postpartum Core Recovery & Diastasis Recti",
    "car-accident-physiotherapy-ontario": "Car Accident Physiotherapy in Ontario",
    "physiotherapy-cost-coverage-ontario": "Physio Referral, OHIP & Insurance in Ontario",
    "dizziness-vestibular-rehabilitation": "Dizziness & Vestibular Rehab (BPPV, Vertigo)",
}
POSTS.sort(key=lambda p: (p["published"], p["slug"]), reverse=True)
BY_SLUG = {p["slug"]: p for p in POSTS}
IMG_SIZES = {}


def img_size(name):
    if name not in IMG_SIZES:
        from PIL import Image
        IMG_SIZES[name] = Image.open(os.path.join(ROOT, "img", name + ".jpg")).size
    return IMG_SIZES[name]


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def words(html_text):
    return len(re.sub(r"<[^>]+>", " ", html_text).split())


def fmt_date(d):
    y, m, dd = map(int, d.split("-"))
    return date(y, m, dd).strftime("%B %-d, %Y")


# ── Services data ──────────────────────────────────────────
from services_data import SERVICE_PAGES
SP_BY_SLUG = {s["slug"]: s for s in SERVICE_PAGES}

CONSULT = dict(slug=None, icon="chat", name="Free 15&#8209;Min Consultation", book="Free 15-Min Consultation",
               card="Not sure where to start? A free call to talk through your symptoms and find the right next step.")

# Values patients can pick on the booking form (stored in Netlify as-is).
BOOK_SERVICES = [
    ("Free 15-Min Consultation", "Free · 15 min call"),
    ("Initial Assessment", "First visit"),
    ("Follow-up Treatment", "Returning patient"),
    ("Pelvic Floor Physiotherapy", "Pelvic health"),
    ("Post-Surgery Rehab", "After surgery"),
    ("Sports Injury Care", "Injury & return to sport"),
    ("Pain Management", "Back, neck & joint pain"),
    ("Car Accident (MVA) Rehab", "Whiplash & MVA"),
]
VISIT_TYPES = [("Virtual", "Video call from anywhere"), ("In my home", "Ottawa area"),
               ("Home clinic room", "In person, by request"), ("Not sure yet", "We'll help you choose")]


def book_url(svc, visit=""):
    u = "/booking?service=" + svc.replace(" ", "%20").replace("(", "%28").replace(")", "%29")
    if visit:
        u += "&visit=" + visit.replace(" ", "%20")
    return u


def service_card(s):
    if s.get("slug"):
        cls, href, cta = "card card--link", f"/services/{s['slug']}", "Learn more &rarr;"
    else:
        cls, href, cta = "card card--link card--featured", book_url(s["book"]), "Book free call &rarr;"
    return f'''          <a class="{cls}" href="{href}">
            <span class="icon">{icon(s["icon"])}</span>
            <span class="card__text"><h3>{s["name"]}</h3>
            <p>{s["card"]}</p></span>
            <span class="card__cta">{cta}</span>
          </a>'''


def post_card(p, heading="h3"):
    w, h = img_size(p["image"])
    return f'''          <article class="card post-card" data-category="{esc(p["category"])}">
            <a class="post-card__img" href="/blog/{p["slug"]}" tabindex="-1" aria-hidden="true">{pic(p["image"], p["image_alt"], w, h)}</a>
            <div class="post-card__body">
              <span class="tag">{esc(p["category"])}</span>
              <{heading}><a href="/blog/{p["slug"]}">{esc(p["title"])}</a></{heading}>
              <p>{esc(p["description"])}</p>
              <span class="post-meta">{fmt_date(p["published"])} · {p["minutes"]} min read</span>
            </div>
          </article>'''


for p in POSTS:
    p["minutes"] = max(3, math.ceil(words(p["body"]) / 220))

# ── Home ───────────────────────────────────────────────────
HOME_FAQS = [
    ("Do I need a doctor's referral to book?", "No. In Ontario you can book directly with a registered physiotherapist. Some insurance plans ask for a doctor's note before reimbursing, so check your plan."),
    ("Is virtual physiotherapy effective?", "Yes, for many conditions. Virtual physiotherapy supports assessment, education, exercise prescription and progress tracking, and research shows similar results to in-person care for many exercise-based treatments. If you need hands-on care, we'll arrange an in-home visit."),
    ("Which areas of Ottawa do you cover?", "Virtual care is available anywhere in Ontario. In-home visits cover Ottawa and nearby communities, including Kanata, Stittsville, Barrhaven, Nepean, Orléans, Gloucester, Westboro, Centretown, Alta Vista, Riverside South, Findlay Creek and Manotick."),
    ("Is physiotherapy covered by my insurance?", "Many extended health plans cover physiotherapy by a registered physiotherapist, including virtual and in-home visits on many plans. Tell us your insurer when you book. Car accident injuries may be covered by auto insurance."),
    ("How do I book an appointment?", f"Book online, call {PHONE_DISPLAY} or send a WhatsApp message. Appointments are available Monday to Saturday, 9 AM to 7 PM."),
]

CONDITIONS = [("spine", "Lower back pain and sciatica"), ("neck", "Neck pain and headaches"), ("joint", "Knee, hip and shoulder pain"),
              ("run", "Sports injuries and sprains"), ("bandage", "Post-surgery recovery"), ("heart", "Pelvic floor and postpartum"),
              ("car", "Whiplash and car accidents"), ("dizzy", "Dizziness and balance"), ("pulse", "Arthritis and persistent pain")]


def build_home():
    w, h = img_size("hero-home-visit")
    svc_cards = "\n".join(service_card(s) for s in [CONSULT] + SERVICE_PAGES)
    posts = "\n".join(post_card(p) for p in POSTS[:3])
    areas = "\n".join(f"            <li>{a}</li>" for a in AREAS)
    body = f'''    <section class="hero">
      <div class="container hero__grid">
        <div>
          <span class="eyebrow">Virtual &amp; in-home physiotherapy · Ottawa</span>
          <h1>Physiotherapy that comes to you</h1>
          <p class="lead">One-on-one care with Drashti Chauhan, Registered Physiotherapist, online or in your home anywhere in Ottawa. No referral needed.</p>
          <div class="button-row">
            <a class="btn btn-primary" href="/booking" data-track="book_appointment_hero">Book an appointment</a>
            <a class="btn btn-secondary" href="/booking?service=Free%2015-Min%20Consultation" data-track="book_consult_hero">Free 15-min consultation</a>
          </div>
          <ul class="trust-row">
            <li>{icon("shield")}Registered physiotherapist</li>
            <li>{icon("clock")}Mon–Sat, 9 AM–7 PM</li>
            <li>{icon("check")}No referral needed</li>
          </ul>
        </div>
        <div class="hero__media">
          {pic("hero-home-visit", "Physiotherapist helping an older woman with a resistance band exercise in her living room", w, h, eager=True)}
          <div class="hero__card">
            {pic("drashti-chauhan", "Drashti Chauhan", 800, 1067)}
            <div><strong>Drashti Chauhan, PT</strong><span>Registered Physiotherapist</span></div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="help-title">
      <div class="container">
        <div class="section-heading">
          <span class="eyebrow">Services</span>
          <h2 id="help-title">What do you need help with?</h2>
          <p>Choose what fits best, or start with a free consultation if you're not sure.</p>
        </div>
        <div class="grid grid-4">
{svc_cards}
        </div>
      </div>
    </section>

    <section class="section section--tint">
      <div class="container">
        <div class="section-heading section-heading--center">
          <span class="eyebrow">How it works</span>
          <h2>Getting started is simple</h2>
        </div>
        <div class="steps">
          <div class="step"><h3>Send a request</h3><p>Book online in about a minute, or call or WhatsApp us. Choose virtual, in-home or a home clinic room visit.</p></div>
          <div class="step"><h3>We confirm your time</h3><p>We'll contact you to confirm your appointment, usually the same day.</p></div>
          <div class="step"><h3>Get assessed and treated</h3><p>A one-on-one assessment, a clear explanation, and a plan with exercises you can do at home.</p></div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="meet-title">
      <div class="container profile">
        <div class="profile__photo">{pic("drashti-chauhan", "Portrait of Drashti Chauhan, Registered Physiotherapist", 800, 1067)}</div>
        <div>
          <span class="eyebrow">Meet your physiotherapist</span>
          <h2 id="meet-title">Drashti Chauhan, PT</h2>
          <p class="role">Registered Physiotherapist</p>
          <p>I'm a registered physiotherapist (PT) in Canada with a Bachelor of Physiotherapy from India. Before my registration, I worked as a Physiotherapy Assistant in long-term care and private practice, which showed me how different everyone's rehabilitation needs are at each stage of life.</p>
          <p>I started Virtual Physio to make good physiotherapy easier to access: unhurried, one-on-one, and in a setting that works for you.</p>
          <div class="button-row">
            <a class="btn btn-primary" href="/booking" data-track="book_appointment_profile">Book with Drashti</a>
            <a class="btn btn-secondary" href="/about">About Virtual Physio</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--tint">
      <div class="container split">
        <div>
          <span class="eyebrow">Why Virtual Physio</span>
          <h2>Unhurried, one-on-one care that fits your life</h2>
          <ul class="ticks">
            <li>Every session one-on-one with a registered physiotherapist</li>
            <li>No travel: virtual sessions or in-home visits across Ottawa</li>
            <li>Evenings and Saturdays available</li>
            <li>Clear explanations and a home program you can actually follow</li>
            <li>Book online, by phone or on WhatsApp</li>
          </ul>
        </div>
        <div>
          <h3>In-home visits across Ottawa</h3>
          <p class="muted">Virtual care is available anywhere in Ontario. We visit homes in:</p>
          <ul class="chips">
{areas}
          </ul>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-heading">
          <span class="eyebrow">Resources</span>
          <h2>Physiotherapy advice you can use</h2>
        </div>
        <div class="grid grid-3">
{posts}
        </div>
        <p style="margin-top:1.5rem"><a class="btn btn-secondary" href="/blog">See all articles</a></p>
      </div>
    </section>

    <section class="section section--tint">
      <div class="container narrow">
        <div class="section-heading section-heading--center">
          <span class="eyebrow">FAQ</span>
          <h2>Questions before booking</h2>
        </div>
        {faq_html(HOME_FAQS)}
      </div>
    </section>

{cta_band()}'''
    schema = ld({**BUSINESS, "description": "Virtual and in-home physiotherapy in Ottawa with a registered physiotherapist.",
                 "sameAs": [WHATSAPP]}, PERSON,
                {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Virtual Physio"},
                faq_ld(HOME_FAQS))
    preload = '  <link rel="preload" as="image" href="/img/hero-home-visit.webp" type="image/webp" fetchpriority="high">\n'
    write("index.html", page(path="/", title="Virtual & In-Home Physiotherapy in Ottawa | Virtual Physio",
                             description="One-on-one virtual and in-home physiotherapy in Ottawa with a registered physiotherapist. Back pain, sports injuries, pelvic floor, post-surgery and MVA rehab.",
                             active="/", body=body, posts=POSTS, schema=schema, preload=preload))


# ── About ──────────────────────────────────────────────────
def build_about():
    trail = [("Home", "/"), ("About", "/about")]
    w, h = img_size("home-visit-knee")
    body = f'''    <section class="page-hero">
      <div class="container">
        {breadcrumb_html(trail)}
        <span class="eyebrow">About Virtual Physio</span>
        <h1>Physiotherapy built around you, not the clinic schedule</h1>
        <p>Virtual Physio offers one-on-one physiotherapy online and in homes across Ottawa, so getting good care doesn't depend on getting to a clinic.</p>
      </div>
    </section>

    <section class="section" aria-labelledby="drashti">
      <div class="container profile">
        <div class="profile__photo">{pic("drashti-chauhan", "Portrait of Drashti Chauhan, Registered Physiotherapist", 800, 1067, eager=True)}</div>
        <div>
          <span class="eyebrow">Your physiotherapist</span>
          <h2 id="drashti">Drashti Chauhan, PT</h2>
          <p class="role">Registered Physiotherapist</p>
          <p>I'm a registered physiotherapist (PT) in Canada. I earned my Bachelor of Physiotherapy in India and then worked as a Physiotherapy Assistant in long-term care and private practice settings in Canada.</p>
          <p>Working with people from young athletes to older adults in long-term care taught me that good rehab isn't one-size-fits-all. It has to fit the person's body, goals, home and daily routine. That's why I offer care virtually and in your home.</p>
          <ul class="facts">
            <li>{icon("shield")}Registered Physiotherapist (PT)</li>
            <li>{icon("book")}Bachelor of Physiotherapy</li>
            <li>{icon("home")}Experience in long-term care</li>
            <li>{icon("user")}Experience in private practice</li>
          </ul>
          <a class="btn btn-primary" href="/booking" data-track="book_appointment_about">Book with Drashti</a>
        </div>
      </div>
    </section>

    <section class="section section--tint">
      <div class="container split">
        <div class="media-frame">{pic("home-visit-knee", "Physiotherapist working with an older man at home", w, h)}</div>
        <div>
          <span class="eyebrow">Our approach</span>
          <h2>Listen first, then build a plan that works in real life</h2>
          <p>Every appointment begins with a focused assessment and a conversation about what matters to you. From there we set clear goals and build a plan that respects your lifestyle, comfort and pace.</p>
          <p>Treatment may include exercise, hands-on techniques, posture and movement training, education and self-management strategies. Each step is explained in plain language, and you're encouraged to ask questions at any point.</p>
          <p>The goal isn't just to relieve pain today. It's to help you move with confidence and independence, and to know what to do if symptoms come back.</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-heading">
          <span class="eyebrow">What we value</span>
          <h2>How we care for patients</h2>
        </div>
        <div class="grid grid-3">
          <div class="card"><span class="icon">{icon("clipboard")}</span><h3>Evidence-based</h3><p>Treatment choices guided by current research and your response, not habit.</p></div>
          <div class="card"><span class="icon">{icon("chat")}</span><h3>Clear communication</h3><p>Plain-language explanations and time for your questions at every visit.</p></div>
          <div class="card"><span class="icon">{icon("map")}</span><h3>Accessible</h3><p>Virtual, in-home and person-to-person options, with evenings and Saturdays.</p></div>
          <div class="card"><span class="icon">{icon("pulse")}</span><h3>Measurable progress</h3><p>Goals and milestones you can see, reviewed and adjusted as you improve.</p></div>
          <div class="card"><span class="icon">{icon("shield")}</span><h3>Prevention-focused</h3><p>Skills and exercises to help you stay well after discharge.</p></div>
          <div class="card"><span class="icon">{icon("heart")}</span><h3>Respect and privacy</h3><p>Your comfort and consent come first, especially for sensitive care like pelvic health.</p></div>
        </div>
      </div>
    </section>

{cta_band("Ready to get started?")}'''
    schema = ld(PERSON, {**BUSINESS}, breadcrumb_ld(trail),
                {"@type": "AboutPage", "url": f"{SITE}/about", "name": "About Virtual Physio", "mainEntity": {"@id": f"{SITE}/about#drashti"}})
    write("about.html", page(path="/about", title="About Drashti Chauhan, PT | Virtual Physio Ottawa",
                             description="Meet Drashti Chauhan, Registered Physiotherapist, and learn how Virtual Physio delivers one-on-one virtual and in-home physiotherapy across Ottawa.",
                             active="/about", body=body, posts=POSTS, schema=schema))


# ── Services ───────────────────────────────────────────────
SERVICE_FAQS = [
    ("How many sessions will I need?", "It depends on your condition and goals. After your assessment your physiotherapist will recommend a plan. Many people start weekly and space sessions out as they improve."),
    ("Virtual, in-home or home clinic room: which should I choose?", "Virtual works well for exercise-based care, education and follow-ups. In-home is best when hands-on treatment is needed or travel is hard. The home clinic room offers in-person care by request. Not sure? Book a free consultation."),
    ("Do I need a referral?", "No. In Ontario you can book directly with a physiotherapist. Some insurance plans require a doctor's note for reimbursement."),
    ("Is physiotherapy covered by insurance?", "Many extended health plans cover physiotherapy by a registered physiotherapist. Car accident injuries may be covered through auto insurance. Tell us your insurer when you book."),
    ("What should I wear?", "Comfortable clothing that lets the area being treated be seen and moved, for example shorts for a knee problem."),
]


def build_services():
    trail = [("Home", "/"), ("Services", "/services")]
    cards = "\n".join(service_card(s) for s in [CONSULT] + SERVICE_PAGES)
    body = f'''    <section class="page-hero">
      <div class="container">
        {breadcrumb_html(trail)}
        <span class="eyebrow">Services</span>
        <h1>Physiotherapy services in Ottawa</h1>
        <p>Every session is one-on-one with a registered physiotherapist, online or in your home. Choose a service to learn more, or start with a free consultation.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="grid grid-4">
{cards}
        </div>
      </div>
    </section>

    <section class="section section--tint">
      <div class="container">
        <div class="section-heading">
          <span class="eyebrow">Ways to see us</span>
          <h2>Virtual, in-home or in person</h2>
        </div>
        <div class="grid grid-3">
          <div class="card"><span class="icon">{icon("video")}</span><h3>Virtual</h3><p>Secure video sessions from anywhere in Ontario. Great for exercise-based care, education and follow-ups.</p><a class="card__cta" href="/services/virtual-physiotherapy">About virtual care &rarr;</a></div>
          <div class="card"><span class="icon">{icon("home")}</span><h3>In-home</h3><p>We come to you across Ottawa. Best when hands-on treatment is needed or travel is difficult.</p><a class="card__cta" href="/services/in-home-physiotherapy">About in-home care &rarr;</a></div>
          <div class="card"><span class="icon">{icon("user")}</span><h3>Home clinic room</h3><p>In-person appointments in a private home clinic room, available by request.</p><a class="card__cta" href="{book_url("Initial Assessment", "Home clinic room")}">Request a visit &rarr;</a></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container split">
        <div>
          <span class="eyebrow">Insurance</span>
          <h2>Using your insurance</h2>
          <p>Many extended health plans cover physiotherapy by a registered physiotherapist, and many include virtual and in-home visits. Car accident injuries may be covered through your auto insurance accident benefits.</p>
          <p>Our guide explains <a href="/blog/physiotherapy-cost-coverage-ontario">referrals, OHIP and insurance in Ontario</a>.</p>
        </div>
        <ul class="ticks">
          <li>No doctor's referral needed to book</li>
          <li>Check your plan's yearly physiotherapy maximum</li>
          <li>Ask whether virtual and home visits are covered</li>
          <li>Keep receipts for the medical expense tax credit</li>
        </ul>
      </div>
    </section>

    <section class="section section--tint">
      <div class="container narrow">
        <div class="section-heading section-heading--center">
          <span class="eyebrow">FAQ</span>
          <h2>Common questions</h2>
        </div>
        {faq_html(SERVICE_FAQS)}
      </div>
    </section>

{cta_band()}'''
    offers = [{"@type": "Offer", "itemOffered": {"@type": "MedicalTherapy", "name": s["name"], "url": f"{SITE}/services/{s['slug']}"}} for s in SERVICE_PAGES]
    schema = ld({**BUSINESS, "makesOffer": offers}, breadcrumb_ld(trail), faq_ld(SERVICE_FAQS))
    write("services/index.html", page(path="/services", title="Physiotherapy Services in Ottawa | Virtual Physio",
                                description="Virtual and in-home physiotherapy in Ottawa: back and neck pain, sports injuries, pelvic floor, post-surgery rehab and car accident recovery.",
                                active="/services", body=body, posts=POSTS, schema=schema))


def build_service_page(s):
    path = f"/services/{s['slug']}"
    trail = [("Home", "/"), ("Services", "/services"), (s["name"].replace("&#8209;", "-"), path)]
    w, h = img_size(s["image"])
    who = "".join(f"<li>{x}</li>" for x in s["for"])
    steps = "\n".join(f'          <div class="step"><h3>{t}</h3><p>{d}</p></div>' for t, d in s["expect"])
    posts = "\n".join(post_card(BY_SLUG[x]) for x in s["posts"] if x in BY_SLUG)
    others = "\n".join(f'            <li><a href="/services/{o["slug"]}">{o["nav"]}</a></li>' for o in SERVICE_PAGES if o is not s)
    book = book_url(s["book"], s.get("visit", ""))
    body = f'''    <section class="page-hero">
      <div class="container hero__grid">
        <div>
          {breadcrumb_html(trail)}
          <span class="eyebrow">Services</span>
          <h1>{s["title"]}</h1>
          <p>{s["lead"]}</p>
          <div class="button-row">
            <a class="btn btn-primary" href="{book}" data-track="book_service_page">Book {s["name"].split(" (")[0].lower() if s["slug"] != "car-accident-rehab" else "MVA rehab"}</a>
            <a class="btn btn-secondary" href="tel:{PHONE_TEL}" data-track="call_service_page">Call {PHONE_DISPLAY}</a>
          </div>
        </div>
        <div class="media-frame">{pic(s["image"], s["image_alt"], w, h, eager=True)}</div>
      </div>
    </section>

    <section class="section">
      <div class="container split">
        <div>
          <span class="eyebrow">Who it's for</span>
          <h2>Can this help you?</h2>
          <ul class="ticks">{who}</ul>
        </div>
        <div class="card">
          <h3>Not sure if this is right for you?</h3>
          <p>Book a free 15-minute call. We'll listen, answer your questions and suggest the best next step.</p>
          <a class="btn btn-primary" href="/booking?service=Free%2015-Min%20Consultation" style="align-self:flex-start">Book a free consultation</a>
        </div>
      </div>
    </section>

    <section class="section section--tint">
      <div class="container">
        <div class="section-heading">
          <span class="eyebrow">What to expect</span>
          <h2>How it works</h2>
        </div>
        <div class="steps">
{steps}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container narrow">
        <div class="section-heading section-heading--center">
          <span class="eyebrow">FAQ</span>
          <h2>Common questions</h2>
        </div>
        {faq_html(s["faqs"])}
      </div>
    </section>

    <section class="section section--tint">
      <div class="container">
        <div class="section-heading"><h2>Helpful articles</h2></div>
        <div class="grid grid-3">
{posts}
        </div>
        <div style="margin-top:2.5rem">
          <h3>Other services</h3>
          <ul class="chips">
{others}
          </ul>
        </div>
      </div>
    </section>

{cta_band("Ready to book?", "Send a request online in about a minute, or call or WhatsApp us. We'll confirm your appointment, usually the same day.")}'''
    svc_ld = {"@type": "MedicalTherapy", "name": s["name"].replace("&#8209;", "-"), "description": s["description"], "url": SITE + path,
              "provider": {"@id": f"{SITE}/#business"}}
    write(f"services/{s['slug']}/index.html",
          page(path=path, title=s["seo_title"] + " | Virtual Physio" if len(s["seo_title"]) < 50 else s["seo_title"],
               description=s["description"], active="/services", body=body, posts=POSTS,
               schema=ld(svc_ld, {**BUSINESS}, breadcrumb_ld(trail), faq_ld(s["faqs"])),
               og_image=f"{SITE}/img/{s['image']}.jpg"))


# ── Blog index ─────────────────────────────────────────────
def build_blog():
    trail = [("Home", "/"), ("Resources", "/blog")]
    cats = []
    for p in POSTS:
        if p["category"] not in cats:
            cats.append(p["category"])
    filters = '<button type="button" aria-pressed="true" data-filter="all">All</button>' + "".join(
        f'<button type="button" aria-pressed="false" data-filter="{esc(c)}">{esc(c)}</button>' for c in cats)
    cards = "\n".join(post_card(p, "h2") for p in POSTS)
    body = f'''    <section class="page-hero">
      <div class="container">
        {breadcrumb_html(trail)}
        <span class="eyebrow">Blog</span>
        <h1>Physiotherapy advice and guides</h1>
        <p>Practical, evidence-based articles on pain, injuries, recovery and getting the most from physiotherapy in Ottawa.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="filter-row" role="group" aria-label="Filter articles by topic">{filters}</div>
        <div class="grid grid-3" id="post-grid">
{cards}
        </div>
      </div>
    </section>

{cta_band("Have a question about your symptoms?")}

    <script>
      document.querySelectorAll('.filter-row button').forEach(function (b) {{
        b.addEventListener('click', function () {{
          var f = b.dataset.filter;
          document.querySelectorAll('.filter-row button').forEach(function (x) {{ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }});
          document.querySelectorAll('#post-grid .post-card').forEach(function (c) {{ c.hidden = !(f === 'all' || c.dataset.category === f); }});
        }});
      }});
    </script>'''
    blog_ld = {"@type": "Blog", "@id": f"{SITE}/blog", "name": "Virtual Physio Blog", "url": f"{SITE}/blog",
               "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}/blog/{p['slug']}", "datePublished": p["published"]} for p in POSTS]}
    write("blog.html", page(path="/blog", title="Physiotherapy Blog: Pain, Injury & Recovery | Virtual Physio",
                            description="Evidence-based physiotherapy articles: back and neck pain, sports injuries, post-surgery rehab, pelvic health, car accidents, dizziness and insurance in Ontario.",
                            active="/blog", body=body, posts=POSTS, schema=ld(blog_ld, breadcrumb_ld(trail))))


# ── Blog posts ─────────────────────────────────────────────
def build_post(p):
    trail = [("Home", "/"), ("Resources", "/blog"), (p["short"], f"/blog/{p['slug']}")]
    toc = "".join(f'<li><a href="#{a}">{re.sub("<[^>]+>", "", t)}</a></li>'
                  for a, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', p["body"]))
    w, h = img_size(p["image"])
    related = "\n".join(post_card(BY_SLUG[s]) for s in p["related"] if s in BY_SLUG)
    updated = p.get("updated", TODAY)
    dates = f'Published {fmt_date(p["published"])}'
    if updated != p["published"]:
        dates += f' · Updated {fmt_date(updated)}'
    faq_block = f'''
          <h2 id="faq">Frequently asked questions</h2>
          {faq_html(p["faqs"])}''' if p.get("faqs") else ""
    if p.get("faqs"):
        toc += '<li><a href="#faq">FAQ</a></li>'
    body = f'''    <article>
      <header class="article-hero">
        <div class="container">
          {breadcrumb_html(trail)}
          <span class="tag">{esc(p["category"])}</span>
          <h1>{esc(p["title"])}</h1>
          <p class="lead">{esc(p["lead"])}</p>
          <div class="byline"><span>By the Virtual Physio team</span><span>{dates}</span><span>{p["minutes"]} min read</span></div>
        </div>
      </header>
      <div class="container">
        <figure class="article-cover">{pic(p["image"], p["image_alt"], w, h, eager=True)}</figure>
        <div class="article-layout">
          <div class="prose">
{p["body"]}{faq_block}
            <p class="notice" style="margin-top:2rem">This article is general information and isn't a substitute for an individual assessment. If you're unsure about your symptoms, speak to a physiotherapist or your doctor.</p>
            <div class="author-box">
              {pic("drashti-chauhan", "Drashti Chauhan", 800, 1067)}
              <p><strong>Virtual Physio</strong> provides one-on-one virtual and in-home physiotherapy across Ottawa with Drashti Chauhan, Registered Physiotherapist. <a href="/about">About us</a></p>
            </div>
          </div>
          <aside class="toc" aria-label="On this page">
            <h2>On this page</h2>
            <ol>{toc}</ol>
            <a class="btn btn-primary" href="/booking?service=Free%2015-Min%20Consultation" data-track="book_from_article">Free 15-min consult</a>
          </aside>
        </div>
      </div>
    </article>

    <section class="section section--tint">
      <div class="container">
        <div class="section-heading"><h2>Related articles</h2></div>
        <div class="grid grid-3">
{related}
        </div>
      </div>
    </section>

{cta_band()}'''
    article = {
        "@type": "BlogPosting",
        "@id": f"{SITE}/blog/{p['slug']}#article",
        "headline": p["title"],
        "description": p["description"],
        "image": f"{SITE}/img/{p['image']}.jpg",
        "datePublished": p["published"],
        "dateModified": updated,
        "author": {"@type": "Organization", "name": "Virtual Physio", "url": f"{SITE}/"},
        "publisher": {"@id": f"{SITE}/#business"},
        "mainEntityOfPage": f"{SITE}/blog/{p['slug']}",
        "wordCount": words(p["body"]),
        "articleSection": p["category"],
    }
    objs = [article, breadcrumb_ld(trail), {**BUSINESS}]
    if p.get("faqs"):
        objs.append(faq_ld(p["faqs"]))
    write(f"blog/{p['slug']}/index.html",
          page(path=f"/blog/{p['slug']}", title=SEO_TITLES.get(p["slug"], p["title"]) + " | Virtual Physio", description=p["description"],
               active="/blog", body=body, posts=POSTS, schema=ld(*objs), og_type="article",
               og_image=f"{SITE}/img/{p['image']}.jpg",
               preload=f'  <link rel="preload" as="image" href="/img/{p["image"]}.webp" type="image/webp" fetchpriority="high">\n'))


# ── Booking (also the contact page) ────────────────────────
def build_booking():
    trail = [("Home", "/"), ("Book an appointment", "/booking")]
    svc = "\n".join(
        f'''              <label class="choice"><input type="radio" name="service" value="{v}"{" required" if i == 0 else ""}><span><strong>{v}</strong><small>{d}</small></span></label>'''
        for i, (v, d) in enumerate(BOOK_SERVICES))
    visit = "\n".join(
        f'''              <label class="choice choice--sm"><input type="radio" name="visitType" value="{v}"><span><strong>{v}</strong><small>{d}</small></span></label>'''
        for v, d in VISIT_TYPES)
    ages = "".join(f"<option>{a}</option>" for a in ["Under 18", "18–34", "35–49", "50–64", "65 or older"])
    body = f'''    <section class="page-hero page-hero--compact">
      <div class="container">
        {breadcrumb_html(trail)}
        <h1>Book an appointment</h1>
        <p>Send a request in about a minute. We'll confirm your appointment by phone, email or WhatsApp, usually the same day.</p>
      </div>
    </section>

    <section class="section section--flush-top">
      <div class="container contact-grid">
        <form class="booking-form vp-form" id="appointment-form" name="appointment-request" method="POST" action="/booking" data-netlify="true" netlify-honeypot="bot-field" novalidate>
          <input type="hidden" name="form-name" value="appointment-request">
          <p class="sr-only"><label>Leave this empty: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>

          <fieldset class="form-step">
            <legend><span class="step-num">1</span>What do you need help with? <span class="req">*</span></legend>
            <div class="choices" data-field="service">
{svc}
            </div>
            <small class="field-error" aria-live="polite"></small>
          </fieldset>

          <fieldset class="form-step">
            <legend><span class="step-num">2</span>How would you like to be seen? <span class="req">*</span></legend>
            <div class="choices choices--4" data-field="visitType">
{visit}
            </div>
            <small class="field-error" aria-live="polite"></small>
            <div class="form-row" data-show-when="In my home" hidden>
              <label for="area">Your area or neighbourhood <span class="req">*</span></label>
              <input id="area" name="area" type="text" autocomplete="address-level2" placeholder="e.g. Kanata, Barrhaven, Orléans">
              <small class="hint">We'll confirm your full address when we call.</small>
              <small class="field-error" aria-live="polite"></small>
            </div>
          </fieldset>

          <fieldset class="form-step">
            <legend><span class="step-num">3</span>Your details</legend>
            <div class="form-grid">
              <div class="form-row">
                <label for="name">Full name <span class="req">*</span></label>
                <input id="name" name="name" type="text" autocomplete="name" required>
                <small class="field-error" aria-live="polite"></small>
              </div>
              <div class="form-row">
                <label for="phone">Phone <span class="req">*</span></label>
                <input id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="343 202 4226" required>
                <small class="field-error" aria-live="polite"></small>
              </div>
              <div class="form-row">
                <label for="email">Email <span class="opt">(optional)</span></label>
                <input id="email" name="email" type="email" autocomplete="email">
                <small class="field-error" aria-live="polite"></small>
              </div>
              <div class="form-row">
                <label for="ageGroup">Patient's age group <span class="req">*</span></label>
                <select id="ageGroup" name="ageGroup" required><option value="">Select…</option>{ages}</select>
                <small class="hint age-note" hidden>Patients under 18 need a parent or guardian to book and to be present at appointments.</small>
                <small class="field-error" aria-live="polite"></small>
              </div>
            </div>
          </fieldset>

          <fieldset class="form-step">
            <legend><span class="step-num">4</span>When suits you? <span class="opt">(optional)</span></legend>
            <div class="form-grid">
              <div class="form-row">
                <label for="date">Preferred date</label>
                <input id="date" name="date" type="date">
              </div>
              <div class="form-row">
                <label for="timeOfDay">Preferred time</label>
                <select id="timeOfDay" name="timeOfDay"><option value="">Any time</option><option>Morning (9–12)</option><option>Afternoon (12–4)</option><option>Evening (4–7)</option></select>
              </div>
            </div>
          </fieldset>

          <fieldset class="form-step">
            <legend><span class="step-num">5</span>Anything else? <span class="opt">(optional)</span></legend>
            <div class="form-row">
              <label for="insurance">Insurance provider</label>
              <input id="insurance" name="insurance" type="text" placeholder="e.g. Sun Life, Manulife, Canada Life, auto insurance">
            </div>
            <div class="form-row">
              <label for="message">Briefly, what's going on?</label>
              <textarea id="message" name="message" rows="4" placeholder="e.g. Left knee pain for 6 weeks, worse on stairs."></textarea>
            </div>
          </fieldset>

          <div class="form-row consent">
            <label class="check"><input type="checkbox" name="consent" value="Yes" required> <span>I agree that Virtual Physio may contact me about this request by phone, email or WhatsApp, and I've read the <a href="/privacy" target="_blank">privacy policy</a>. <span class="req">*</span></span></label>
            <small class="field-error" aria-live="polite"></small>
          </div>

          <button class="btn btn-primary btn-block" type="submit">Send request</button>
          <div class="form-status" role="status" aria-live="polite"></div>
          <p class="hint" style="margin-top:.8rem">Not an emergency service. If you have a medical emergency, call 911.</p>
        </form>

        <aside class="contact-panel" id="contact" aria-label="Contact Virtual Physio">
          <h2>Prefer to talk?</h2>
          <div class="contact-actions">
            <a class="btn btn-secondary btn-block" href="tel:{PHONE_TEL}" data-track="call_booking">{icon("phone")} Call {PHONE_DISPLAY}</a>
            <a class="btn btn-whatsapp btn-block" href="{WHATSAPP}" rel="noopener" data-track="whatsapp_booking">{icon("chat")} WhatsApp us</a>
            <a class="btn btn-secondary btn-block" href="mailto:{EMAIL}">Email {EMAIL}</a>
          </div>
          <h3>Hours</h3>
          <p>Monday to Saturday, 9:00 AM – 7:00 PM</p>
          <h3>What happens next</h3>
          <ol class="next-steps">
            <li>We contact you to confirm a time.</li>
            <li>Virtual: you get a secure video link.</li>
            <li>In-home: we confirm your address and access details.</li>
          </ol>
          <h3>Where we see patients</h3>
          <p class="muted">Virtual care anywhere in Ontario. In-home visits across Ottawa, including Kanata, Barrhaven, Orléans, Nepean, Stittsville and Manotick.</p>
        </aside>
      </div>
    </section>'''
    schema = ld({**BUSINESS}, breadcrumb_ld(trail),
                {"@type": "ContactPage", "url": f"{SITE}/booking", "name": "Book an appointment", "about": {"@id": f"{SITE}/#business"}})
    write("booking.html", page(path="/booking", title="Book a Physiotherapy Appointment | Virtual Physio Ottawa",
                               description="Book virtual or in-home physiotherapy in Ottawa in about a minute, or call or WhatsApp us. Free 15-minute consultations. Mon–Sat, 9 AM–7 PM.",
                               active="/booking#contact", body=body, posts=POSTS, schema=schema))


def build_privacy():
    trail = [("Home", "/"), ("Privacy policy", "/privacy")]
    body = f'''    <section class="page-hero page-hero--compact">
      <div class="container">
        {breadcrumb_html(trail)}
        <h1>Privacy policy</h1>
        <p>Last updated {fmt_date(TODAY)}</p>
      </div>
    </section>
    <section class="section section--flush-top">
      <div class="container narrow prose">
        <p>Virtual Physio respects your privacy and protects your personal health information in line with Ontario's <em>Personal Health Information Protection Act</em> (PHIPA) and the standards of the College of Physiotherapists of Ontario.</p>
        <h2>What we collect</h2>
        <ul>
          <li><strong>Booking requests:</strong> your name, phone number, email (optional), age group, the service and visit type you choose, your area, preferred times, insurance provider and anything you choose to tell us about your symptoms.</li>
          <li><strong>Clinical records:</strong> if you become a patient, the assessment and treatment notes physiotherapists are required to keep.</li>
          <li><strong>Website data:</strong> basic technical information such as your browser and IP address, used to keep the website secure and prevent spam.</li>
        </ul>
        <h2>Why we collect it</h2>
        <p>To respond to your request, schedule and provide care, communicate with you, bill you or your insurer when you ask us to, and meet our legal and professional obligations. We don't sell your information or use it for advertising.</p>
        <h2>How it's stored and shared</h2>
        <ul>
          <li>Booking requests sent through this website are stored by our website host, Netlify.</li>
          <li>If you choose to message us on WhatsApp, that conversation is handled by WhatsApp (Meta) under its own privacy policy.</li>
          <li>We share health information only with your consent, or where the law requires or permits it.</li>
          <li>Clinical records are kept securely for as long as professional regulations require.</li>
        </ul>
        <h2>Your choices and rights</h2>
        <p>You can ask to see or correct your personal health information, withdraw your consent to being contacted, or ask us to delete a booking request that didn't lead to care. Please don't include more health detail in the booking form than you're comfortable sharing. We'll ask what we need when we speak with you.</p>
        <h2>Contact us</h2>
        <p>Questions or requests about your privacy: <a href="mailto:{EMAIL}">{EMAIL}</a> or <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>. If you have concerns we can't resolve, you can contact the <a href="https://www.ipc.on.ca/" rel="noopener">Information and Privacy Commissioner of Ontario</a>.</p>
      </div>
    </section>'''
    write("privacy.html", page(path="/privacy", title="Privacy Policy | Virtual Physio", description="How Virtual Physio collects, uses and protects your personal and health information.",
                               active=None, body=body, posts=POSTS, schema=ld(breadcrumb_ld(trail))))


def build_sitemap():
    urls = [("/", "1.0"), ("/services", "0.9"), ("/booking", "0.9"), ("/about", "0.8"), ("/blog", "0.8"), ("/privacy", "0.3")]
    urls += [(f"/services/{s['slug']}", "0.9") for s in SERVICE_PAGES]
    items = [f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>" for u, pr in urls]
    for p in POSTS:
        items.append(f"  <url><loc>{SITE}/blog/{p['slug']}</loc><lastmod>{p.get('updated', TODAY)}</lastmod><priority>0.7</priority></url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(items) + "\n</urlset>\n")


if __name__ == "__main__":
    build_home()
    build_about()
    build_services()
    for s in SERVICE_PAGES:
        build_service_page(s)
    build_blog()
    for p in POSTS:
        build_post(p)
    build_booking()
    build_privacy()
    build_sitemap()
    write("404.html", page(path="/404", title="Page not found | Virtual Physio", description="The page you were looking for could not be found.",
                           active=None, posts=POSTS, body='''    <section class="page-hero"><div class="container">
        <span class="eyebrow">404</span>
        <h1>Sorry, we couldn't find that page</h1>
        <p>It may have moved. Try one of these instead:</p>
        <div class="button-row"><a class="btn btn-primary" href="/booking">Book an appointment</a><a class="btn btn-secondary" href="/services">Services</a><a class="btn btn-secondary" href="/blog">Resources</a></div>
      </div></section>''').replace('index, follow', 'noindex'))
    print("built", len(SERVICE_PAGES), "service pages,", len(POSTS), "posts")
