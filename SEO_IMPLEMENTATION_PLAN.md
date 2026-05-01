# Virtual Physio.ca SEO Implementation Plan

## Highest Priority Actions

1. Verify the real service area and NAP
   - Current site uses: Virtual Physio.ca, +1 613 979 8633, info@virtualphysio.ca.
   - Add the exact public clinic address only if it is allowed to be shown online.
   - If there is no public clinic address, use a service-area Google Business Profile and keep the address hidden.

2. Connect Google tools
   - Add GA4 and Google Search Console.
   - Track these conversion events: `generate_lead`, `book_appointment_nav`, `book_appointment_hero`, `call_hero`, `call_contact`, `call_booking`, `whatsapp_fab`, `whatsapp_booking`.
   - In GA4, mark `generate_lead`, phone clicks and WhatsApp clicks as key events.

3. Publish local landing pages after confirming cities
   - `/physiotherapy-ottawa`
   - `/virtual-physiotherapy-ontario`
   - `/pelvic-floor-physiotherapy-ontario`
   - `/in-home-physiotherapy-ottawa`
   - Each page needs unique copy, FAQs, service-area wording, testimonials and a booking CTA.

4. Improve image performance
   - Rename `Logo.png` to `virtual-physio-logo.png`.
   - Rename `drashti-profile.png` to `drashti-chauhan-virtual-physiotherapist.png`.
   - Export WebP versions under 150 KB when an image tool is available.
   - Use `<picture>` with WebP first and PNG fallback.

5. Build trust signals
   - Add patient reviews once approved for publishing.
   - Add credential details, licensing/registration details and continuing education.
   - Add privacy reassurance beside every lead form.

## On-Page SEO Targets

Primary homepage keyword:
Virtual physiotherapy Ontario

Secondary keywords:
- online physiotherapy Canada
- physiotherapy Ottawa
- in-home physiotherapy
- pelvic floor physiotherapy online
- post-surgery rehabilitation
- sports injury physiotherapy
- lower back pain physiotherapy

Internal linking rules:
- Homepage links to Services, Booking and Contact.
- Every service card links to Booking.
- Blog cards link to the relevant service and booking page.
- Future city pages should link back to Services and Booking.

## Blog Content Roadmap

Publish these as full articles, not just cards:

1. Virtual Physiotherapy vs In-Person Physiotherapy: Which Is Right for You?
2. Pelvic Floor Physiotherapy Online: Symptoms, Benefits and What to Expect
3. How to Manage Lower Back Pain at Home Before Your Physio Appointment
4. Postpartum Core Recovery and Diastasis Recti: A Physiotherapy Guide
5. Vestibular Rehabilitation for Dizziness and Balance Problems
6. TMJ Physiotherapy: Jaw Pain, Headaches and Neck Tension
7. Sports Injury Prevention Tips for Weekend Athletes
8. Post-Surgery Rehabilitation Timeline: What Patients Should Expect

## Backlink Strategy

Free or low-cost:
- Create/optimize Google Business Profile.
- Add listings on Bing Places, Apple Business Connect, Yelp, YellowPages Canada and local chamber directories.
- Ask referral partners to link to the service pages.
- Publish guest education posts for local wellness, fitness, yoga and postpartum organizations.

Paid or premium:
- BrightLocal or Whitespark for citation building.
- Ahrefs or Semrush for competitor keyword gap tracking.
- HARO-style expert quotes through Featured.com or Qwoted.

## Monitoring Stack

Free:
- Google Search Console
- GA4
- PageSpeed Insights
- Rich Results Test
- Bing Webmaster Tools

Paid:
- Semrush or Ahrefs for keyword gap and backlink monitoring
- Screaming Frog SEO Spider for technical crawls
- Hotjar or Microsoft Clarity for UX behavior recordings

## Technical Checklist

- Submit `https://virtualphysio.ca/sitemap.xml` in Search Console.
- Inspect `/`, `/services`, `/booking`, `/contact`, `/about`, `/blog`.
- Validate schema in Google Rich Results Test.
- Confirm Netlify redirects from `.html` URLs to clean URLs.
- Compress images and retest Core Web Vitals.
- Add privacy policy and terms pages before scaling paid campaigns.
