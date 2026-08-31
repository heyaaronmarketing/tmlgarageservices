#!/usr/bin/env python3
"""Google Ads Editor import files for TML Garage Door Services.

$10,000/month, Search only — Local Services Ads is not part of this playbook.

Emits one CSV per entity type into ./import/, plus 00_FULL_IMPORT.csv which
carries the whole account in a single file. Everything is length-checked and
cross-checked before it is written, so nothing fails at import time.

Claims policy: only statements the TML site already makes appear in ad copy.
Prices, licence numbers, years in business and award badges are unverified and
are listed in OPTIONAL_COPY rather than written into the ads.

Usage:  python3 build_campaign.py
"""
import csv
import sys
from pathlib import Path

OUT = Path(__file__).parent / "import"
OUT.mkdir(exist_ok=True)

SITE = "https://www.tmlgarageservices.com"
PHONE = "(832) 887-8747"
SUFFIX = ("utm_source=google&utm_medium=cpc&utm_campaign={campaignid}"
          "&utm_content={adgroupid}&utm_term={keyword}&mt={matchtype}&dev={device}")

# ---------------------------------------------------------------- campaigns
# Allocation is efficiency-first, not proportional to auction size. Sized
# proportionally, Head Terms would take 85% of the budget — $8,500 buying about
# 17 leads at Houston's $38 average CPC. Cheap tiers are bought out first and
# Head Terms absorbs what is left, bid-capped below market.
CAMPAIGNS = [
    ("TML | Search | Head Terms",            5200, "Manual CPC"),
    ("TML | Search | Install & Replace",     2500, "Manual CPC"),
    ("TML | Search | Commercial & Gates",     900, "Manual CPC"),
    ("TML | Search | Components & Symptoms",  800, "Manual CPC"),
    ("TML | Search | Competitor",             400, "Manual CPC"),
    ("TML | Search | Brand",                  200, "Manual CPC"),
]

# ------------------------------------------------------------- $2,000 test
# Run with --test. Not the $10,000 plan scaled by 80% — a different shape.
#
# Two decisions drive it:
#
#   * EXACT MATCH ONLY. At 25 miles, exact tops out around $3,136/mo of
#     capacity, so $2,000 takes ~64% of it — high impression share on the
#     keywords that matter, instead of a thin smear across phrase traffic. It
#     also removes the daily search-term babysitting that phrase demands. The
#     question this test answers is "do these leads exist and convert", not
#     "can we win a loose auction".
#   * FOUR CAMPAIGNS, NOT SIX. Commercial and Competitor are excluded.
#     Commercial leads cost $300-600 and carry a 45-90 day sales cycle — it
#     cannot produce a readable result in 60 days at any budget, let alone this
#     one. Competitor is a nice-to-have, not a lead test.
TEST_BUDGETS = {
    "TML | Search | Head Terms":            1000,
    "TML | Search | Components & Symptoms":  600,
    "TML | Search | Install & Replace":      300,
    "TML | Search | Brand":                  100,
}
TEST_EXCLUDE = ("TML | Search | Commercial & Gates", "TML | Search | Competitor")

TEST = "--test" in sys.argv
if TEST:
    OUT = Path(__file__).parent / "import-test"
    OUT.mkdir(exist_ok=True)
    CAMPAIGNS = [(n, TEST_BUDGETS[n], b) for n, _, b in CAMPAIGNS if n in TEST_BUDGETS]


URLS = {
    "generic":    f"{SITE}/services",
    "emergency":  f"{SITE}/contact",
    "spring":     f"{SITE}/our-services/garage-door-spring-replacement",
    "opener":     f"{SITE}/our-services/garage-door-opener-installation",
    "install":    f"{SITE}/our-services/residential-garage-door-services",
    "commercial": f"{SITE}/our-services/commercial-overhead-door-services",
    "gates":      f"{SITE}/our-services/residential-driveway-gate-services",
    "brand":      f"{SITE}/",
    "book":       f"{SITE}/schedule-consult",
}

# ------------------------------------------------------- ad groups + keywords
# Exact carries the bid; a phrase twin is generated for every exact keyword
# outside Brand and Competitor (see build_keywords). Exact alone tops out around
# $8,100/mo even across the whole Houston metro — phrase is what makes $10,000
# reachable inside 25 miles. No broad match until conversion data can steer it.
AD_GROUPS = [
    # -- the efficiency engine: component vocabulary, $0.28-$9 clicks ---------
    ("TML | Search | Components & Symptoms", "Sensors & Safety", "opener", 6.00, [
        ("garage door sensor repair", "Exact"), ("fix garage door sensor", "Exact"),
        ("garage door sensor replacement", "Exact"),
        ("garage door safety sensor replacement", "Exact"),
    ]),
    ("TML | Search | Components & Symptoms", "Springs & Cables", "spring", 8.00, [
        ("garage door torsion spring replacement", "Exact"),
        ("garage torsion spring replacement", "Exact"),
        ("overhead door torsion spring replacement", "Exact"),
        ("garage door cable replacement", "Exact"),
        ("overhead door cable replacement", "Exact"),
        ("garage door wire replacement", "Exact"),
        ("garage door cable repair", "Exact"), ("garage door cable off drum", "Exact"),
    ]),
    ("TML | Search | Components & Symptoms", "Rollers Tracks Panels", "generic", 9.00, [
        ("garage door roller replacement", "Exact"), ("garage door panel replacement", "Exact"),
        ("garage door track replacement", "Exact"), ("garage door track repair", "Exact"),
        ("garage door hinge replacement", "Exact"), ("garage door hinge repair", "Exact"),
        ("garage door bottom seal replacement", "Exact"),
    ]),
    ("TML | Search | Components & Symptoms", "Opener Mechanics", "opener", 9.00, [
        ("garage door opener replacement", "Exact"), ("garage door motor replacement", "Exact"),
        ("garage door belt replacement", "Exact"),
        ("garage door drive belt replacement", "Exact"),
        ("replace garage door lock", "Exact"),
    ]),
    ("TML | Search | Components & Symptoms", "Symptoms", "generic", 12.00, [
        ("garage door wont open", "Exact"), ("garage door won't open", "Exact"),
        ("garage door wont close", "Exact"), ("garage door won't close", "Exact"),
        ("garage door stuck", "Exact"), ("garage door off track", "Exact"),
        ("garage door off track repair", "Phrase"), ("garage door not working", "Exact"),
        ("garage door stuck open", "Exact"), ("garage door crooked", "Exact"),
        ("garage door making noise", "Exact"), ("garage door came off track", "Exact"),
        ("garage door opener not working", "Exact"), ("garage door opener wont work", "Exact"),
    ]),
    ("TML | Search | Components & Symptoms", "Install Near Me", "install", 8.00, [
        ("garage door installation near me", "Exact"),
    ]),
    # -- head terms: real intent, brutal prices. Capped well under market -----
    ("TML | Search | Head Terms", "Repair Core", "generic", 30.00, [
        ("garage door repair", "Exact"), ("garage door repair near me", "Exact"),
        ("garage door repair service", "Exact"), ("garage door service", "Exact"),
        ("garage door opener repair", "Exact"), ("garage door opener repair near me", "Exact"),
    ]),
    ("TML | Search | Head Terms", "Springs Head", "spring", 30.00, [
        ("garage door spring repair", "Exact"), ("broken garage door spring", "Exact"),
        ("garage door spring replacement", "Exact"),
        ("garage door spring repair near me", "Exact"), ("garage door spring broke", "Exact"),
    ]),
    ("TML | Search | Head Terms", "Local Towns", "generic", 26.00, [
        ("garage door repair conroe", "Exact"), ("garage door repair conroe tx", "Exact"),
        ("garage door conroe", "Exact"), ("garage door repair the woodlands", "Exact"),
        ("garage door repair the woodlands tx", "Exact"),
        ("garage door repair spring tx", "Exact"),
        ("garage door repair montgomery tx", "Exact"),
        ("garage door repair willis tx", "Exact"),
        ("garage door repair magnolia tx", "Exact"),
        ("garage door repair tomball tx", "Exact"),
    ]),
    ("TML | Search | Head Terms", "Emergency Capped", "emergency", 22.00, [
        ("same day garage door repair", "Exact"), ("24 hour garage door repair", "Exact"),
        ("garage door repair open now", "Exact"), ("garage door repair today", "Exact"),
        ("weekend garage door repair", "Exact"), ("after hours garage door repair", "Exact"),
    ]),
    ("TML | Search | Head Terms", "Tune Up", "book", 14.00, [
        ("garage door tune up", "Exact"), ("garage door maintenance", "Exact"),
        ("garage door inspection", "Exact"), ("garage door safety inspection", "Exact"),
        ("garage door tune up near me", "Exact"), ("garage door lubrication service", "Exact"),
    ]),
    # -- install --------------------------------------------------------------
    ("TML | Search | Install & Replace", "New Door Install", "install", 26.00, [
        ("new garage door installation", "Exact"), ("garage door installation", "Exact"),
        ("garage door replacement", "Exact"), ("replace garage door", "Exact"),
        ("new garage door", "Exact"), ("garage door installers near me", "Exact"),
        ("new garage door cost", "Exact"), ("garage door replacement cost", "Exact"),
    ]),
    ("TML | Search | Install & Replace", "Door Types", "install", 8.00, [
        ("insulated garage door", "Exact"), ("insulated garage door installation", "Phrase"),
        ("carriage garage doors", "Exact"), ("custom garage doors", "Exact"),
        ("modern garage doors", "Exact"), ("steel garage door installation", "Exact"),
        ("wood garage door installation", "Exact"), ("glass garage door installation", "Exact"),
        ("double garage door replacement", "Exact"),
    ]),
    ("TML | Search | Install & Replace", "Opener Install & Brands", "opener", 16.00, [
        ("garage door opener installation", "Exact"), ("new garage door opener", "Exact"),
        ("liftmaster garage door opener installation", "Exact"),
        ("liftmaster dealer near me", "Exact"),
        ("chamberlain garage door opener repair", "Exact"),
        ("genie garage door opener repair", "Exact"),
        ("craftsman garage door opener repair", "Exact"),
        ("smart garage door opener installation", "Exact"),
        ("wall mount garage door opener installation", "Exact"),
    ]),
    # -- commercial -----------------------------------------------------------
    ("TML | Search | Commercial & Gates", "Commercial Overhead", "commercial", 40.00, [
        ("commercial garage door repair", "Exact"),
        ("commercial garage door repair near me", "Exact"),
        ("commercial overhead door repair", "Exact"), ("overhead door repair", "Exact"),
        ("commercial garage door installation", "Exact"),
        ("rolling steel door repair", "Exact"), ("loading dock door repair", "Exact"),
        ("commercial door repair near me", "Exact"), ("warehouse door repair", "Exact"),
        ("roll up door repair", "Exact"),
    ]),
    ("TML | Search | Commercial & Gates", "Gates", "gates", 20.00, [
        ("driveway gate repair", "Exact"), ("gate opener repair", "Exact"),
        ("automatic gate repair", "Exact"), ("electric gate repair", "Exact"),
        ("driveway gate installation", "Exact"), ("gate operator repair", "Exact"),
        ("automatic gate installation", "Exact"), ("gate motor repair", "Exact"),
        ("commercial gate repair", "Exact"),
    ]),
    # -- competitor: legal to bid on, never named in the ad text --------------
    ("TML | Search | Competitor", "Competitor Brands", "generic", 8.00, [
        ("pro garage door repair", "Exact"), ("garage door service master", "Exact"),
        ("speedy garage door repair", "Exact"), ("elite garage door repair", "Exact"),
    ]),
    ("TML | Search | Brand", "TML Brand", "brand", 3.00, [
        ("tml garage door services", "Exact"), ("tml garage services", "Exact"),
        ("tml garage door", "Phrase"), ("tml garage door conroe", "Exact"),
    ]),
]

# ------------------------------------------------------------------ negatives
# Phrases, not words. Written as a blob split on whitespace this list turned
# "entry door" and "home depot" into the negatives "door" and "home", which
# would have blocked every keyword in the account.
#
# Deliberately absent: "free" (blocks "free estimate", a buying search),
# "reviews" (blocks comparison shopping), "license" (blocks "licensed garage
# door repair"), and "spring" / "houston" / "cypress" — real places we serve.
NEGATIVES = {
    "DIY and how-to": [
        "diy", "do it yourself", "how to", "how do i", "how can i", "fix it myself",
        "fix myself", "repair myself", "tutorial", "youtube", "video", "instructions",
        "manual", "step by step", "homemade", "troubleshoot", "troubleshooting",
        "reset code", "program remote", "programming", "reprogram", "myq setup"],
    "Jobs and training": [
        "job", "jobs", "career", "careers", "hiring", "salary", "salaries", "wage",
        "wages", "employment", "apprentice", "apprenticeship", "training", "school",
        "certification", "course", "classes", "resume", "vacancy", "recruiter",
        "union", "how much do they make"],
    "Parts and retail": [
        "parts", "home depot", "lowes", "lowe's", "amazon", "menards", "costco",
        "walmart", "ebay", "harbor freight", "wholesale", "supplier", "supply",
        "distributor", "buy online", "for sale", "kit", "kits", "replacement parts",
        "remote battery", "battery", "batteries", "struts", "brackets", "used",
        "second hand", "salvage"],
    "Design and decor": [
        "ideas", "design ideas", "paint", "painting", "color", "colors", "decor",
        "decorating", "curtain", "curtains", "screen", "screens", "magnets",
        "decals", "mural", "wrap", "sticker", "window inserts", "decorative",
        "faux windows"],
    "Not our service": [
        "storage unit", "storage units", "self storage", "garage sale", "garage band",
        "parking garage", "garage floor", "epoxy", "flooring", "garage organization",
        "shelving", "cabinets", "gym", "garage conversion", "adu", "shed", "carport",
        "rental", "rent", "for rent", "entry door", "front door", "screen door",
        "storm door", "shower door", "barn door", "pet door", "interior door",
        "fence", "fencing", "window replacement", "car garage"],
    "Research and complaints": [
        "meaning", "definition", "wikipedia", "reddit", "forum", "what is",
        "why does", "complaints", "scam", "lawsuit", "attorney", "lawyer",
        "class action", "recall", "warranty claim", "insurance claim"],
    "Business and franchise": [
        "franchise", "franchises", "business for sale", "start a business",
        "dealer application", "become a dealer", "manufacturer", "factory"],
    "Outside service area": [
        "dallas", "fort worth", "austin", "san antonio", "el paso", "lubbock",
        "amarillo", "corpus christi", "galveston", "beaumont", "college station",
        "waco", "tyler", "killeen", "midland", "odessa", "oklahoma", "louisiana",
        "florida", "california", "arizona"],
}

# Steers each search to the campaign that can serve it cheapest. Note what is
# NOT here: a blanket "repair" negative on Install & Replace. That campaign holds
# "chamberlain garage door opener repair" and its siblings, and a campaign-level
# "repair" negative would have silently switched all four brand keywords off.
CROSS_NEGATIVES = {
    "TML | Search | Install & Replace": [
        ("won't open", "Phrase"), ("wont open", "Phrase"), ("off track", "Phrase"),
        ("broken spring", "Phrase"), ("emergency", "Phrase"), ("same day", "Phrase")],
    "TML | Search | Head Terms": [
        ("installation", "Phrase"), ("sensor", "Phrase"), ("panel replacement", "Phrase"),
        ("roller replacement", "Phrase"), ("cable replacement", "Phrase"),
        ("torsion spring replacement", "Phrase"), ("hinge", "Phrase"),
        ("bottom seal", "Phrase")],
}

# Commercial and gate work must never be paid for out of a residential
# campaign. In the $2,000 test that traffic is pure waste — Commercial & Gates
# is not running at all. In the full plan it belongs in the campaign built for
# it, where the bid ($40) and the landing page match the job value.
#
# "overhead door" is deliberately NOT here: Components legitimately holds
# "overhead door torsion spring replacement" and "overhead door cable
# replacement". Plenty of Texas homeowners call a residential door an overhead
# door, and blocking the phrase would cost real repair work.
COMMERCIAL_NEGATIVES = [
    "commercial", "industrial", "warehouse", "loading dock", "dock door",
    "dock leveler", "rolling steel", "roll up door", "rollup door",
    "roll-up door", "storefront", "shop door", "bay door", "high speed door",
    "fire door", "sectional steel", "apartment complex", "strip mall",
    "hangar", "business park", "property manager", "facility",
    "gate", "gates", "gate opener", "gate operator", "driveway gate",
    "automatic gate", "electric gate", "sliding gate", "swing gate",
]
RESIDENTIAL_CAMPAIGNS = (
    "TML | Search | Head Terms",
    "TML | Search | Components & Symptoms",
    "TML | Search | Install & Replace",
)

for _c in RESIDENTIAL_CAMPAIGNS:
    CROSS_NEGATIVES.setdefault(_c, [])
    CROSS_NEGATIVES[_c] += [(t, "Phrase") for t in COMMERCIAL_NEGATIVES]


# --------------------------------------------------------------- ad creative
COMMON_H = [
    "Same-Day Garage Door Repair", "Conroe & The Woodlands", "Call (832) 887-8747",
    "Weekends At No Extra Charge", "Upfront Price Before We Start", "Trained, Insured Techs",
    "Book Online In One Minute", "Serving Greater Houston",
]
COMMON_D = [
    "Same-day appointments across Conroe, The Woodlands and Spring. Call (832) 887-8747.",
    "We quote the full price before any work starts. No surprises when the job is done.",
    "Trained, insured technicians. Weekend appointments at no extra charge.",
    "Book online in about a minute, or call and speak to someone in Conroe today.",
]

ADS = {
    "Sensors & Safety": (
        ["Garage Door Sensor Repair", "Sensors Realigned Same Day", "Door Reversing On You?",
         "Safety Eye Repair"] + COMMON_H,
        ["Door reverses before it closes? Usually the safety sensors. Same-day fix.",
         "We realign, rewire or replace photo-eye sensors across Conroe and The Woodlands."]
        + COMMON_D[1:3], "opener", "sensors", "repair"),
    "Springs & Cables": (
        ["Torsion Spring Replacement", "Cable Off The Drum?", "Springs Replaced In Pairs",
         "Broken Spring? Same Day"] + COMMON_H,
        ["Broken spring or a cable off its drum? Same-day replacement by trained techs.",
         "Springs replaced in matched pairs so you are not paying for a second visit."]
        + COMMON_D[1:3], "spring", "springs", "replacement"),
    "Rollers Tracks Panels": (
        ["Roller & Track Replacement", "Garage Door Panel Repair", "Bottom Seal Replacement",
         "Door Off Its Track?"] + COMMON_H,
        ["Worn rollers, bent track, split panel or a perished bottom seal - all same day.",
         "Trained, insured technicians across Conroe, The Woodlands and Spring."]
        + COMMON_D[1:3], "generic", "parts", "replacement"),
    "Opener Mechanics": (
        ["Garage Door Opener Repair", "Motor Or Belt Replacement", "Opener Replaced Same Day",
         "LiftMaster & Genie Service"] + COMMON_H,
        ["Motor burnt out, belt snapped or the opener finally given up? Same-day service.",
         "We service and replace LiftMaster, Chamberlain, Genie and Craftsman openers."]
        + COMMON_D[1:3], "opener", "openers", "repair"),
    "Symptoms": (
        ["Garage Door Won't Open?", "Garage Door Won't Close?", "Door Stuck Or Off Track?",
         "We Fix It Same Day"] + COMMON_H,
        ["Stuck, crooked, noisy or off its track? Same-day appointments across Conroe.",
         "We quote the full price before any work starts. No surprises at the end."]
        + COMMON_D[2:], "generic", "garage-door", "repair"),
    "Install Near Me": (
        ["Garage Door Install Near You", "Local Conroe Installers", "Free On-Site Measure",
         "New Door, Fitted Right"] + COMMON_H,
        ["New garage door measured and fitted by a local Conroe team. Free on-site quote.",
         "Full price confirmed before anything is ordered."] + COMMON_D[2:],
        "install", "new-door", "installation"),
    "Repair Core": (
        ["Garage Door Repair Near You", "Local Conroe Garage Door Co", "Same-Day Appointments",
         "Repaired Today, Not Next Week"] + COMMON_H, COMMON_D, "generic", "garage-door", "repair"),
    "Springs Head": (
        ["Garage Door Spring Repair", "Broken Spring? Same Day", "Springs Replaced In Pairs"]
        + COMMON_H,
        ["Broken spring? Same-day replacement by trained technicians across Conroe.",
         "We replace springs in matched pairs so you are not paying for a second call."]
        + COMMON_D[1:3], "spring", "springs", "repair"),
    "Local Towns": (
        ["Garage Door Repair Conroe", "Serving The Woodlands, TX", "Based Here, Not Out Of Town",
         "Same-Day In Montgomery Co."] + COMMON_H,
        ["A Conroe team, not a call centre. Same-day across The Woodlands, Spring and Willis.",
         "We quote the full price before any work starts."] + COMMON_D[2:],
        "generic", "conroe", "repair"),
    "Emergency Capped": (
        ["Same-Day Garage Door Repair", "Open Today - Call Now", "Weekend Repairs, No Surcharge",
         "Garage Door Repaired Today"] + COMMON_H,
        ["Door stuck or won't open? Same-day appointments across Conroe and The Woodlands.",
         "Call and speak to a person. Full price quoted before any work begins."]
        + COMMON_D[2:], "emergency", "same-day", "repair"),
    "Tune Up": (
        ["Garage Door Tune-Up", "Keep It Running Quietly", "Book A Service Visit",
         "Annual Door Maintenance"] + COMMON_H,
        ["Texas heat is hard on door hardware. Book a tune-up and keep it running quietly.",
         "Balance check, lubrication, safety reverse test and every fixing tightened."]
        + COMMON_D[2:], "book", "tune-up", "service"),
    "New Door Install": (
        ["New Garage Door Install", "Garage Door Replacement", "Free On-Site Measure",
         "New Door, Fitted Right"] + COMMON_H,
        ["New garage door fitted by trained, insured technicians across greater Houston.",
         "We measure on site and quote the full price before anything is ordered."]
        + COMMON_D[2:], "install", "new-door", "installation"),
    "Door Types": (
        ["Insulated Garage Doors", "Carriage & Modern Doors", "Custom Garage Doors",
         "Steel, Wood & Glass Doors"] + COMMON_H,
        ["Insulated, carriage, modern and custom doors fitted across Conroe and Spring.",
         "An insulated door makes a real difference to an attached garage in a Texas summer."]
        + COMMON_D[2:], "install", "new-door", "styles"),
    "Opener Install & Brands": (
        ["New Garage Door Opener", "LiftMaster Installation", "Quiet Belt Drive Openers",
         "Opener Fitted Same Day"] + COMMON_H,
        ["LiftMaster, Chamberlain, Genie and Craftsman openers supplied and fitted.",
         "Quiet belt drive for attached garages. Battery backup for storm season."]
        + COMMON_D[2:], "opener", "openers", "installation"),
    "Commercial Overhead": (
        ["Commercial Overhead Doors", "Roll-Up & Dock Door Repair", "Business Door Service",
         "Commercial Door Repair"] + COMMON_H[1:],
        ["Overhead, roll-up and dock door repair for businesses across greater Houston.",
         "Downtime costs money. Same-day and emergency commercial appointments."]
        + COMMON_D[1:3], "commercial", "commercial", "overhead-doors"),
    "Gates": (
        ["Driveway Gate Repair", "Gate Opener Service", "Automatic Gate Repair",
         "Gate Not Opening?"] + COMMON_H[1:],
        ["Driveway gate and gate operator repair, service and installation.",
         "Gate stuck open or motor dead? Same-day appointments across greater Houston."]
        + COMMON_D[1:3], "gates", "gates", "repair"),
    # Bidding on a competitor's name is allowed; using it in the ad text is
    # trademark infringement. Nothing below names anyone.
    "Competitor Brands": (
        ["Garage Door Repair Conroe", "Compare Local Garage Door Co", "Same-Day Appointments",
         "Upfront Price, No Surprises", "Based In Conroe, TX"] + COMMON_H[1:],
        ["Comparing garage door companies? Same-day appointments and upfront pricing.",
         "A local Conroe team. Full price quoted before any work starts."]
        + COMMON_D[2:], "generic", "compare", "conroe"),
    "TML Brand": (
        ["TML Garage Door Services", "Official TML Site", "Conroe, TX - Call Us",
         "Book With TML Directly"] + COMMON_H[1:], COMMON_D, "brand", "tml", "official"),
}

# Held back deliberately — each depends on a fact nobody has confirmed.
OPTIONAL_COPY = [
    ("$69 Garage Door Tune-Up", "on the site, but the price is not in the verified facts; "
     "Google requires offer terms and limitations to be stated"),
    ("5.0 From 213 Google Reviews", "must match the live Google Business Profile on the day "
     "the ad runs, and be re-checked as the count moves"),
    ("Licensed, Bonded & Insured", "no licence or bond number on file"),
    ("Family Owned Since 20XX", "years in business unknown"),
    ("Angi Super Service Award", "the award on the site is dated 2019"),
]

SITELINKS = [
    ("Book Online", "Pick a day and time.", "Confirmation straight away.", URLS["book"]),
    ("Spring Replacement", "Broken spring? Same day.", "Replaced in matched pairs.", URLS["spring"]),
    ("Opener Repair", "LiftMaster, Genie, Craftsman.", "Same-day appointments.", URLS["opener"]),
    ("New Garage Doors", "Measured and fitted on site.", "Full price before ordering.", URLS["install"]),
    ("Commercial Doors", "Overhead, roll-up and dock.", "Emergency service available.", URLS["commercial"]),
    ("Driveway Gates", "Gate and operator repair.", "Across greater Houston.", URLS["gates"]),
]
CALLOUTS = ["Same-Day Appointments", "No Weekend Surcharge", "Upfront Pricing",
            "Trained & Insured Techs", "Locally Based In Conroe", "Emergency Service",
            "LiftMaster Openers", "Free On-Site Quote"]
SNIPPETS = [("Services", ["Spring Replacement", "Opener Repair", "New Installation",
                          "Cable & Roller Repair", "Commercial Doors", "Driveway Gates"]),
            ("Brands", ["LiftMaster", "Chamberlain", "Genie", "Craftsman"])]

RADIUS = "25 mi radius around Conroe, Texas"
GEO = ["Conroe, Texas", "The Woodlands, Texas", "Spring, Texas", "Montgomery, Texas",
       "Willis, Texas", "Magnolia, Texas", "Tomball, Texas", "Porter, Texas",
       "New Caney, Texas", "Shenandoah, Texas", "Oak Ridge North, Texas", "Splendora, Texas"]

# Loosening these two buys nothing but noise.
TIGHT = ("TML | Search | Brand", "TML | Search | Competitor")


def w(name, header, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        c = csv.writer(f)
        c.writerow(header)
        c.writerows(rows)
    print(f"  {name:<40} {len(rows):>5} rows")


def check(text, limit, what):
    if len(text) > limit:
        raise SystemExit(f"TOO LONG ({len(text)}/{limit}) {what}: {text!r}")
    return text


def build_keywords():
    """Every keyword as written, plus a phrase twin for each exact one outside
    Brand and Competitor. An earlier version tested the *output* match type when
    deciding what to skip, which silently dropped the three keywords that were
    already phrase to begin with."""
    out, seen = [], set()
    for camp, grp, url, cpc, terms in AD_GROUPS:
        if TEST and camp in TEST_EXCLUDE:
            continue
        for kw, mt in terms:
            variants = [(mt, 1.0)]
            if not TEST and mt == "Exact" and camp not in TIGHT:
                variants.append(("Phrase", 0.8))
            for m, mult in variants:
                if (camp, kw, m) in seen:
                    continue
                seen.add((camp, kw, m))
                out.append([camp, grp, kw, m, f"{cpc * mult:.2f}", "Enabled", URLS[url]])
    return out


def active_groups():
    return [g for g in AD_GROUPS if not (TEST and g[0] in TEST_EXCLUDE)]


def rsa_fields(grp):
    heads, descs, u, p1, p2 = ADS[grp]
    H, seen = [], set()
    for h in heads:
        if h not in seen:
            seen.add(h)
            H.append(check(h, 30, f"{grp} headline"))
    D = [check(d, 90, f"{grp} description") for d in descs][:4]
    return (H + [""] * 15)[:15], (D + [""] * 4)[:4], u, check(p1, 15, "path1"), check(p2, 15, "path2")


def validate(keywords):
    """Refuse to ship anything that would misfire once live."""
    def blocks(neg, kw):
        n, k = neg.lower().split(), kw.lower().split()
        return any(k[i:i + len(n)] == n for i in range(len(k) - len(n) + 1))

    shared = [t for terms in NEGATIVES.values() for t in terms]
    for n in shared:
        for r in keywords:
            if blocks(n, r[2]):
                raise SystemExit(f"shared negative {n!r} blocks keyword {r[2]!r}")
    for camp, terms in CROSS_NEGATIVES.items():
        for n, _ in terms:
            for r in keywords:
                if r[0] == camp and blocks(n, r[2]):
                    raise SystemExit(f"{camp}: negative {n!r} blocks its own keyword {r[2]!r}")
    seen = set()
    for r in keywords:
        key = (r[0], r[2], r[3])
        if key in seen:
            raise SystemExit(f"duplicate keyword {key}")
        seen.add(key)
    groups = {(c, g) for c, g, _, _, _ in active_groups()}
    for c, g in groups:
        if g not in ADS:
            raise SystemExit(f"ad group with no ad: {c} / {g}")
    print("  validation: negatives clean, no duplicates, every ad group has an ad")


def build_full_import():
    """One CSV Google Ads Editor can swallow in a single pass.

    Editor decides what each row is by which columns are filled, so every row
    carries the full column set and leaves the rest blank. Order matters —
    campaigns before the ad groups inside them.

    Assets are deliberately not here: Editor treats them as separate entity
    types with their own columns, and mixing them in is the most common reason
    an import half-fails. They stay in files 07-09 and 11.
    """
    cols = (["Campaign", "Campaign type", "Campaign status", "Campaign daily budget",
             "Bid strategy type", "Networks", "Languages", "Final URL suffix", "Location",
             "Ad group", "Ad group status", "Max CPC", "Keyword", "Criterion type",
             "Ad type", "Status"]
            + [f"Headline {i}" for i in range(1, 16)]
            + [f"Description {i}" for i in range(1, 5)]
            + ["Path 1", "Path 2", "Final URL"])
    blank = {c: "" for c in cols}
    rows = []

    def row(**kw):
        r = dict(blank)
        r.update(kw)
        rows.append([r[c] for c in cols])

    for name, monthly, bid in CAMPAIGNS:
        # "en", not "English" — Editor's Languages column takes ISO codes.
        row(**{"Campaign": name, "Campaign type": "Search", "Campaign status": "Paused",
               "Campaign daily budget": f"{monthly / 30.4:.2f}", "Bid strategy type": bid,
               "Networks": "Google search;Search Partners", "Languages": "en",
               "Final URL suffix": SUFFIX})
    for name, _, _ in CAMPAIGNS:
        row(**{"Campaign": name, "Location": RADIUS})
        for g in GEO:
            row(**{"Campaign": name, "Location": g})
    for camp, grp, _, cpc, _ in active_groups():
        row(**{"Campaign": camp, "Ad group": grp, "Ad group status": "Enabled",
               "Max CPC": f"{cpc:.2f}"})
    for camp, _, _ in CAMPAIGNS:
        for terms in NEGATIVES.values():
            for t in terms:
                row(**{"Campaign": camp, "Keyword": t,
                       "Criterion type": "Campaign Negative Phrase"})
    for camp, terms in CROSS_NEGATIVES.items():
        for k, mt in terms:
            row(**{"Campaign": camp, "Keyword": k, "Criterion type": f"Campaign Negative {mt}"})
    for camp, grp, kw, mt, cpc, status, url in build_keywords():
        row(**{"Campaign": camp, "Ad group": grp, "Keyword": kw, "Criterion type": mt,
               "Max CPC": cpc, "Status": status, "Final URL": url})
    for camp, grp, _, _, _ in active_groups():
        H, D, u, p1, p2 = rsa_fields(grp)
        d = {"Campaign": camp, "Ad group": grp, "Ad type": "Responsive search ad",
             "Status": "Enabled", "Path 1": p1, "Path 2": p2, "Final URL": URLS[u]}
        d.update({f"Headline {i+1}": H[i] for i in range(15)})
        d.update({f"Description {i+1}": D[i] for i in range(4)})
        row(**d)

    w("00_FULL_IMPORT.csv", cols, rows)
    return len(rows)


def main():
    keywords = build_keywords()
    validate(keywords)
    monthly = sum(c[1] for c in CAMPAIGNS)

    w("01_campaigns.csv",
      ["Campaign", "Campaign type", "Campaign status", "Campaign daily budget", "Budget type",
       "Bid strategy type", "Networks", "Languages", "Final URL suffix"],
      [[n, "Search", "Paused", f"{m/30.4:.2f}", "Daily", b,
        "Google search;Search Partners", "en", SUFFIX] for n, m, b in CAMPAIGNS])
    w("02_ad_groups.csv", ["Campaign", "Ad Group", "Status", "Max CPC", "Ad Group Type"],
      [[c, g, "Enabled", f"{cpc:.2f}", "Standard"] for c, g, _, cpc, _ in active_groups()])
    w("03_keywords.csv",
      ["Campaign", "Ad Group", "Keyword", "Criterion Type", "Max CPC", "Status", "Final URL"],
      keywords)
    w("04_negative_keywords_shared_list.csv",
      ["Shared Set", "Keyword", "Criterion Type", "Reason Group"],
      [["TML Shared Negatives", t, "Negative Phrase", g]
       for g, terms in NEGATIVES.items() for t in terms])
    w("05_negative_keywords_campaign.csv", ["Campaign", "Keyword", "Criterion Type"],
      [[c, k, f"Campaign Negative {mt}"] for c, terms in CROSS_NEGATIVES.items()
       for k, mt in terms])

    hdr = (["Campaign", "Ad Group", "Ad Type", "Status"]
           + [f"Headline {i}" for i in range(1, 16)]
           + [f"Description {i}" for i in range(1, 5)]
           + ["Path 1", "Path 2", "Final URL"])
    ads = []
    for camp, grp, _, _, _ in active_groups():
        H, D, u, p1, p2 = rsa_fields(grp)
        ads.append([camp, grp, "Responsive search ad", "Enabled"] + H + D + [p1, p2, URLS[u]])
    w("06_responsive_search_ads.csv", hdr, ads)

    w("07_assets_sitelinks.csv",
      ["Campaign", "Sitelink Text", "Description Line 1", "Description Line 2", "Final URL"],
      [[c[0], check(t, 25, "sitelink"), check(d1, 35, "sl desc1"), check(d2, 35, "sl desc2"), u]
       for c in CAMPAIGNS for t, d1, d2, u in SITELINKS])
    w("08_assets_callouts.csv", ["Campaign", "Callout Text"],
      [[c[0], check(t, 25, "callout")] for c in CAMPAIGNS for t in CALLOUTS])
    w("09_assets_structured_snippets.csv", ["Campaign", "Header", "Values"],
      [[c[0], h, "; ".join(v)] for c in CAMPAIGNS for h, v in SNIPPETS])
    w("10_geo_targets.csv", ["Campaign", "Location", "Target Type", "Bid Modifier"],
      [[c[0], RADIUS, "Location of presence", "0%"] for c in CAMPAIGNS]
      + [[c[0], g, "Location of presence", "0%"] for c in CAMPAIGNS for g in GEO])
    w("11_call_asset.csv", ["Campaign", "Phone Number", "Country", "Call Reporting"],
      [[c[0], PHONE, "US", "Enabled"] for c in CAMPAIGNS])
    w("12_copy_held_back.csv", ["Suggested Copy", "Why it is not in the ads"],
      [[t, r] for t, r in OPTIONAL_COPY])

    n = build_full_import()
    print(f"\n{len(CAMPAIGNS)} campaigns · {len(active_groups())} ad groups · {len(keywords)} keywords "
          f"· {sum(len(v) for v in NEGATIVES.values())} shared negatives · {len(ads)} RSAs")
    print(f"00_FULL_IMPORT.csv: {n} rows — the whole account in one file")
    if TEST:
        print(f"TEST MODE — exact match only, {len(CAMPAIGNS)} campaigns, "
              f"${monthly:,}/mo (${monthly/30.4:.2f}/day)")
        print("Run for 60 days before judging it. See TEST-PLAN.md")
    else:
        print(f"Search only — Local Services Ads excluded. Total ${monthly:,}/mo")


if __name__ == "__main__":
    main()
