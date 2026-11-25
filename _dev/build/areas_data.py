"""Area pages: /areas/<slug>. Keep content factual: service availability, nearby neighbourhoods, how visits work."""
AREA_PAGES = [
    dict(slug="kanata", name="Kanata", nearby=["Kanata North", "Kanata South", "Bridlewood", "Beaverbrook", "Glen Cairn", "Morgan's Grant", "Stittsville"],
         note="Whether it's desk-related neck or back pain, a sports injury or recovery after surgery, you can be seen at home in Kanata or online."),
    dict(slug="barrhaven", name="Barrhaven", nearby=["Half Moon Bay", "Stonebridge", "Longfields", "Davidson Heights", "Riverside South", "Manotick"],
         note="In-home and virtual visits can make it easier to fit physiotherapy around work, school runs and childcare in Barrhaven."),
    dict(slug="orleans", name="Orléans", nearby=["Avalon", "Chapel Hill", "Convent Glen", "Queenswood Heights", "Fallingbrook", "Navan"],
         note="Home visits and online sessions mean no commute from Orléans, whether you need care for back pain or rehab after surgery."),
    dict(slug="nepean", name="Nepean", nearby=["Centrepointe", "Craig Henry", "Bells Corners", "Bayshore", "Merivale", "Carlington", "Hunt Club"],
         note="In Nepean we can see you at home, where practising balance, strength and safe movement in your own space can be especially practical, or online."),
]
