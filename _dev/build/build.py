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
SERVICES = [
    dict(id="consult", icon="chat", title="Free 15&#8209;Min Consultation", book="Free 15-Min Consultation",
         short="A free call to talk through your symptoms and goals and find the right next step.",
         body="A free, no-pressure phone or video call. Tell us what's going on, ask questions about virtual or in-home care, and we'll recommend the best place to start.",
         points=["No cost or commitment", "Phone or video", "Get a recommended plan", "Ask about insurance"], featured=True),
    dict(id="virtual", icon="video", title="Virtual Physiotherapy", book="Physiotherapy",
         short="Live one-on-one video sessions: assessment, exercise and education from home.",
         body="A full one-on-one physiotherapy assessment and treatment over secure video. Ideal for back and neck pain, tendon problems, arthritis, post-surgery progressions and follow-ups.",
         points=["Initial assessment", "Follow-up treatment", "Extended sessions for complex cases", "Written home program"], post="virtual-vs-in-person-physiotherapy"),
    dict(id="in-home", icon="home", title="In-Home Physiotherapy", book="In-Home Treatment",
         short="Hands-on physiotherapy at your home anywhere in the Ottawa area.",
         body="Your physiotherapist comes to you anywhere in Ottawa. Hands-on treatment and exercise built around your real home environment: stairs, transfers and the space you have.",
         points=["No travel or waiting room", "Great after surgery", "Falls prevention and balance", "Home safety tips"], post="in-home-physiotherapy-ottawa"),
    dict(id="post-surgery", icon="bandage", title="Post-Surgery Rehab", book="Post-Surgery Rehab",
         short="Step-by-step rehab after joint replacement, ACL repair, fractures and more.",
         body="A structured, phase-by-phase plan that protects your repair and rebuilds motion, strength and confidence, from the first days home through to full activity.",
         points=["Knee and hip replacement", "ACL and meniscus repair", "Shoulder surgery", "Fractures"], post="post-surgery-rehabilitation-timeline"),
    dict(id="pain", icon="pulse", title="Pain Management", book="Pain Management",
         short="Relief and a long-term plan for back, neck, shoulder and joint pain.",
         body="Clear explanation, hands-on relief and a graded exercise plan for back, neck, shoulder, hip and knee pain, including pain that has lasted months.",
         points=["Lower back pain and sciatica", "Neck pain and headaches", "Arthritis", "Persistent pain"], post="lower-back-pain-at-home"),
    dict(id="sports-injury", icon="run", title="Sports Injury Care", book="Sports Injury Care",
         short="Get back to running, hockey, soccer and the gym safely.",
         body="Assessment and return-to-sport rehab for sprains, strains, tendon pain and overuse injuries, with testing to help you return safely and stay injury-free.",
         points=["Sprains and strains", "Tendon pain", "Running injuries", "Return-to-sport testing"], post="sports-injury-prevention"),
    dict(id="pelvic-floor", icon="heart", title="Pelvic Floor Physiotherapy", book="Pelvic Floor Treatment",
         short="Private, respectful care for leaking, pelvic pain, pregnancy and postpartum.",
         body="Assessment and treatment for bladder leaking, pelvic pain, prolapse symptoms, pregnancy-related pain, postpartum recovery and diastasis recti.",
         points=["Bladder leaking and urgency", "Prenatal and postpartum", "Diastasis recti", "Pelvic pain"], post="pelvic-floor-physiotherapy"),
    dict(id="mva", icon="car", title="Car Accident (MVA) Rehab", book="Motor Vehicle Accident Rehab",
         short="Recovery from whiplash and other car accident injuries.",
         body="Physiotherapy for whiplash, back pain, headaches, concussion symptoms and other injuries after a motor vehicle accident, with guidance on Ontario accident benefits.",
         points=["Whiplash", "Back and shoulder injuries", "Concussion symptoms", "Accident benefits guidance"], post="car-accident-physiotherapy-ontario"),
]


def book_url(svc):
    return "/booking?service=" + svc.replace(" ", "%20")


def service_card(s):
    cls = "card card--link card--featured" if s.get("featured") else "card card--link"
    return f'''          <a class="{cls}" href="/services#{s["id"]}">
            <span class="icon">{icon(s["icon"])}</span>
            <span class="card__text"><h3>{s["title"]}</h3>
            <p>{s["short"]}</p></span>
            <span class="card__cta">Learn more &rarr;</span>
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
    ("Is physiotherapy covered by my insurance?", "Many extended health plans cover physiotherapy by a registered physiotherapist, including virtual and in-home visits on many plans. Car accident injuries may be covered by auto insurance. Tell us your insurer when you book."),
    ("How do I book an appointment?", f"Book online, call {PHONE_DISPLAY} or send a WhatsApp message. Appointments are available Monday to Saturday, 9 AM to 7 PM."),
]

CONDITIONS = [("spine", "Lower back pain and sciatica"), ("neck", "Neck pain and headaches"), ("joint", "Knee, hip and shoulder pain"),
              ("run", "Sports injuries and sprains"), ("bandage", "Post-surgery recovery"), ("heart", "Pelvic floor and postpartum"),
              ("car", "Whiplash and car accidents"), ("dizzy", "Dizziness and balance"), ("pulse", "Arthritis and persistent pain")]


def build_home():
    w, h = img_size("hero-home-visit")
    svc_cards = "\n".join(service_card(s) for s in SERVICES)
    posts = "\n".join(post_card(p) for p in POSTS[:3])
    conds = "\n".join(f'          <div class="condition">{icon(i)}<span>{t}</span></div>' for i, t in CONDITIONS)
    areas = "\n".join(f"            <li>{a}</li>" for a in AREAS)
    body = f'''    <section class="hero">
      <div class="container hero__grid">
        <div>
          <span class="eyebrow">Virtual &amp; in-home physiotherapy · Ottawa</span>
          <h1>Physiotherapy that comes to you</h1>
          <p class="lead">One-on-one care with Drashti Chauhan, Registered Physiotherapist, online or in your home anywhere in Ottawa. For back and neck pain, sports injuries, pelvic health, post-surgery rehab and car accident recovery.</p>
          <div class="button-row">
            <a class="btn btn-primary" href="/booking?service=Free%2015-Min%20Consultation" data-track="book_appointment_hero">Book a free 15-min consultation</a>
            <a class="btn btn-secondary" href="tel:{PHONE_TEL}" data-track="call_hero">Call {PHONE_DISPLAY}</a>
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

    <section class="section">
      <div class="container">
        <div class="section-heading">
          <span class="eyebrow">Services</span>
          <h2>Care for pain, injury and recovery</h2>
          <p>Every plan starts with a thorough assessment and is built around your goals, whether that's walking without pain, lifting your kids or getting back on the ice.</p>
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
          <div class="step"><h3>Book a free consultation</h3><p>Book online, call or WhatsApp us. We'll talk through your symptoms and goals in a free 15-minute call.</p></div>
          <div class="step"><h3>Get assessed</h3><p>A full one-on-one assessment online or at your home, with a clear explanation of what's going on.</p></div>
          <div class="step"><h3>Follow your plan</h3><p>Treatment plus a personalised home program, with progress tracked at every session until you reach your goals.</p></div>
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
            <a class="btn btn-secondary" href="/about">More about Drashti</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--tint">
      <div class="container">
        <div class="section-heading">
          <span class="eyebrow">Conditions</span>
          <h2>What we help with</h2>
        </div>
        <div class="conditions">
{conds}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container split">
        <div>
          <span class="eyebrow">Why Virtual Physio</span>
          <h2>Unhurried, one-on-one care that fits your life</h2>
          <ul class="ticks">
            <li>Every session one-on-one with a registered physiotherapist</li>
            <li>No travel: virtual sessions or in-home visits across Ottawa</li>
            <li>Evenings and Saturdays available</li>
            <li>Clear explanations and a home program you can actually follow</li>
            <li>Book by form, phone or WhatsApp</li>
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

    <section class="section section--tint">
      <div class="container">
        <div class="section-heading">
          <span class="eyebrow">From the blog</span>
          <h2>Physiotherapy advice you can use</h2>
        </div>
        <div class="grid grid-3">
{posts}
        </div>
        <p style="margin-top:1.5rem"><a class="btn btn-secondary" href="/blog">See all articles</a></p>
      </div>
    </section>

    <section class="section">
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
    ("What conditions can virtual physiotherapy treat?", "Back and neck pain, joint stiffness and arthritis, tendon problems, sports injuries, post-surgery rehab, pelvic floor concerns, balance problems and general movement limitations."),
    ("How many sessions will I need?", "It depends on your condition and goals. After your assessment your physiotherapist will recommend a plan. Many people start weekly and space sessions out as they improve."),
    ("Can virtual physiotherapy help after surgery?", "Yes. Once the early phase is over, virtual sessions work well for exercise progression, education and monitoring. In-home visits are available when hands-on care is needed."),
    ("Do you offer in-home physiotherapy?", "Yes. We visit homes across Ottawa and nearby communities. Share your location and preferred times when booking."),
    ("Do I need a referral?", "No. In Ontario you can book directly with a physiotherapist. Some insurance plans require a doctor's note for reimbursement."),
    ("What should I wear?", "Comfortable clothing that lets the area being treated be seen and moved, for example shorts for knee problems or a tank top for shoulder problems."),
]


def build_services():
    trail = [("Home", "/"), ("Services", "/services")]
    rows = []
    for s in SERVICES:
        pts = "".join(f"<li>{p}</li>" for p in s["points"])
        more = f' <a href="/blog/{s["post"]}">Read our guide</a>.' if s.get("post") else ""
        rows.append(f'''        <article class="service-row" id="{s["id"]}">
          <span class="icon">{icon(s["icon"])}</span>
          <div>
            <h3>{s["title"]}</h3>
            <p>{s["body"]}{more}</p>
            <ul>{pts}</ul>
          </div>
          <a class="btn {"btn-primary" if s.get("featured") else "btn-secondary"}" href="{book_url(s["book"])}">Book</a>
        </article>''')
    conds = "\n".join(f'          <div class="condition">{icon(i)}<span>{t}</span></div>' for i, t in CONDITIONS + [("jaw", "Jaw (TMJ) pain"), ("baby", "Pregnancy-related pain"), ("user", "Falls prevention")])
    body = f'''    <section class="page-hero">
      <div class="container">
        {breadcrumb_html(trail)}
        <span class="eyebrow">Services</span>
        <h1>Physiotherapy services in Ottawa</h1>
        <p>Choose a service below, or start with a free 15-minute consultation and we'll recommend the right option. Every session is one-on-one with a registered physiotherapist, online or in your home.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
{chr(10).join(rows)}
      </div>
    </section>

    <section class="section section--tint">
      <div class="container">
        <div class="section-heading">
          <span class="eyebrow">Ways to see us</span>
          <h2>Virtual, in-home or in person</h2>
        </div>
        <div class="grid grid-3">
          <div class="card"><span class="icon">{icon("video")}</span><h3>Virtual</h3><p>Secure video sessions from anywhere in Ontario. Great for exercise-based care, education and follow-ups.</p><a class="card__cta" href="/blog/virtual-vs-in-person-physiotherapy">Is virtual right for me? &rarr;</a></div>
          <div class="card"><span class="icon">{icon("home")}</span><h3>In-home</h3><p>We come to you across Ottawa. Best when hands-on treatment is needed or travel is difficult.</p><a class="card__cta" href="/blog/in-home-physiotherapy-ottawa">About in-home care &rarr;</a></div>
          <div class="card"><span class="icon">{icon("user")}</span><h3>Home clinic room</h3><p>Person-to-person appointments in a private home clinic room, available by request.</p><a class="card__cta" href="/contact">Ask about availability &rarr;</a></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-heading">
          <span class="eyebrow">Conditions</span>
          <h2>Common conditions we treat</h2>
          <p>Not sure if physiotherapy can help? These are some of the most common reasons patients book with us.</p>
        </div>
        <div class="conditions">
{conds}
        </div>
      </div>
    </section>

    <section class="section section--tint">
      <div class="container split">
        <div>
          <span class="eyebrow">Insurance</span>
          <h2>Using your insurance</h2>
          <p>Many extended health plans cover physiotherapy by a registered physiotherapist, and many include virtual and in-home visits. Car accident injuries may be covered by your auto insurance accident benefits.</p>
          <p>Tell us your insurer when you book. Our guide explains <a href="/blog/physiotherapy-cost-coverage-ontario">referrals, OHIP and insurance in Ontario</a>.</p>
        </div>
        <div>
          <ul class="ticks">
            <li>No doctor's referral needed to book</li>
            <li>Check your plan's annual physiotherapy maximum</li>
            <li>Ask whether virtual and home visits are covered</li>
            <li>Keep receipts for medical expense tax credits</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container narrow">
        <div class="section-heading section-heading--center">
          <span class="eyebrow">FAQ</span>
          <h2>Common questions</h2>
        </div>
        {faq_html(SERVICE_FAQS)}
      </div>
    </section>

{cta_band()}'''
    offers = [{"@type": "Offer", "itemOffered": {"@type": "MedicalTherapy", "name": s["title"], "description": s["short"]}} for s in SERVICES]
    schema = ld({**BUSINESS, "makesOffer": offers}, breadcrumb_ld(trail), faq_ld(SERVICE_FAQS))
    write("services.html", page(path="/services", title="Physiotherapy Services in Ottawa | Virtual Physio",
                                description="Virtual physiotherapy, in-home physiotherapy, post-surgery rehab, pain management, sports injury, pelvic floor and car accident rehab across Ottawa.",
                                active="/services", body=body, posts=POSTS, schema=schema))


# ── Blog index ─────────────────────────────────────────────
def build_blog():
    trail = [("Home", "/"), ("Blog", "/blog")]
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
    trail = [("Home", "/"), ("Blog", "/blog"), (p["short"], f"/blog/{p['slug']}")]
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


# ── Booking & contact: refresh chrome only ─────────────────
def refresh_chrome(rel, active, title, description):
    path = os.path.join(ROOT, rel)
    src = open(path, encoding="utf-8").read()
    main = re.search(r'<main id="main">(.*)</main>', src, re.S).group(1)
    main = main.replace("<h1>", "<h1>", 1)
    schema = re.findall(r'  <script type="application/ld\+json">.*?</script>', src, re.S)
    out = page(path="/" + rel.replace(".html", ""), title=title, description=description, active=active,
               body=main.strip("\n"), posts=POSTS, schema="\n".join(schema))
    write(rel, out)


def build_sitemap():
    urls = [("/", "1.0"), ("/services", "0.9"), ("/booking", "0.9"), ("/about", "0.8"), ("/contact", "0.8"), ("/blog", "0.8")]
    items = [f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>" for u, pr in urls]
    for p in POSTS:
        items.append(f"  <url><loc>{SITE}/blog/{p['slug']}</loc><lastmod>{p.get('updated', TODAY)}</lastmod><priority>0.7</priority></url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(items) + "\n</urlset>\n")


if __name__ == "__main__":
    build_home()
    build_about()
    build_services()
    build_blog()
    for p in POSTS:
        build_post(p)
    refresh_chrome("booking.html", None, "Book a Physiotherapy Appointment | Virtual Physio Ottawa",
                   "Book virtual or in-home physiotherapy in Ottawa online in under a minute. Free 15-minute consultations available. Mon–Sat, 9 AM–7 PM.")
    refresh_chrome("contact.html", "/contact", "Contact Virtual Physio | Physiotherapy in Ottawa",
                   "Contact Virtual Physio by phone, email or WhatsApp, or send an appointment request. Virtual and in-home physiotherapy across Ottawa.")
    build_sitemap()
    write("404.html", page(path="/404", title="Page not found | Virtual Physio", description="The page you were looking for could not be found.",
                           active=None, posts=POSTS, body='''    <section class="page-hero"><div class="container">
        <span class="eyebrow">404</span>
        <h1>Sorry, we couldn't find that page</h1>
        <p>It may have moved. Try one of these instead:</p>
        <div class="button-row"><a class="btn btn-primary" href="/">Home</a><a class="btn btn-secondary" href="/services">Services</a><a class="btn btn-secondary" href="/blog">Blog</a></div>
      </div></section>''').replace('index, follow', 'noindex'))
    for p in POSTS:
        print(f'{p["slug"]:45s} {words(p["body"]):5d} words')
