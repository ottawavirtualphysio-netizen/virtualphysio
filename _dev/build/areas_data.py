"""Area pages: /areas/<slug>. Keep content factual: service availability, nearby neighbourhoods, how visits work."""
AREA_PAGES = [
    dict(slug="kanata", name="Kanata", nearby=["Kanata North", "Kanata South", "Bridlewood", "Beaverbrook", "Glen Cairn", "Morgan's Grant", "Stittsville"],
         note="Kanata's mix of tech-sector desk jobs and active families means we often help with desk-related neck and back pain, running and hockey injuries, and recovery after surgery."),
    dict(slug="barrhaven", name="Barrhaven", nearby=["Half Moon Bay", "Stonebridge", "Longfields", "Davidson Heights", "Riverside South", "Manotick"],
         note="Many Barrhaven households are young families and commuters, so in-home and virtual visits help fit physiotherapy around school runs, work and childcare, including postpartum and pelvic health care."),
    dict(slug="orleans", name="Orléans", nearby=["Avalon", "Chapel Hill", "Convent Glen", "Queenswood Heights", "Fallingbrook", "Navan"],
         note="Getting downtown from Orléans can take time, so home visits and online sessions save the commute for everything from back pain to rehab after joint replacement."),
    dict(slug="nepean", name="Nepean", nearby=["Centrepointe", "Craig Henry", "Bells Corners", "Bayshore", "Merivale", "Carlington", "Hunt Club"],
         note="Nepean has many older adults living at home and in retirement residences, so we often focus on balance, strength and safe movement at home, as well as recovery after surgery."),
]
