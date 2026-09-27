#!/usr/bin/env python3
"""
Team R2 static site builder.

Every page shares one header/footer, so edit SETTINGS or page content here and run:
    python build.py
It rewrites the .html files next to this script (in the site folder).
No packages needed — plain Python 3.8+.

You can also just edit the generated .html files directly; this script is a convenience.
"""
import os, html
from datetime import date

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# SETTINGS — change these, then run build.py
# ---------------------------------------------------------------------------
S = {
    "site_url": "https://www.teamr2.com",
    "company": "R2 Fabrication, LLC",
    "brand": "Team R2",
    "email": "info@TeamR2.com",
    "phone": "817.720.6060",
    "street": "804 S Blue Mound Rd",
    "city": "Saginaw", "state": "TX", "zip": "76131",
    "sqft": "80,000",
    "hours": "Mon–Fri 7:00 am – 3:30 pm",
    # Careers buttons go to the Indeed company page
    "indeed_url": "https://www.indeed.com/cmp/R2-Fabrication-1/jobs",
    # Free key from https://web3forms.com (enter info@TeamR2.com, key is emailed to you)
    "web3forms_key": "c0acb7c6-a6e5-420e-9251-f9c2636cbb62",
    "maps_link": "https://maps.google.com/?q=804+South+Blue+Mound+Road+Saginaw+TX+76131",
    "maps_embed": "https://maps.google.com/maps?q=804%20S%20Blue%20Mound%20Rd%2C%20Saginaw%2C%20TX%2076131&z=14&output=embed",
}

NAV = [
    ("fabrication-hvac.html", "Sheet Metal"),
    ("fabrication-misc.html", "Industrial"),
    ("installation-services.html", "Installation"),
    ("equipment.html", "Shop & Equipment"),
    ("about.html", "About"),
    ("careers.html", "Careers"),
]

def e(s): return html.escape(s, quote=True)

TEL = "".join(c for c in S["phone"] if c.isdigit())
if len(TEL) == 10: TEL = "+1" + TEL
CUR = ' aria-current="page"'

ICONS = {
    "bolt": '<svg viewBox="0 0 24 24"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>',
    "layers": '<svg viewBox="0 0 24 24"><path d="m12 2 10 5-10 5L2 7l10-5z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/></svg>',
    "box": '<svg viewBox="0 0 24 24"><path d="M21 8 12 3 3 8v8l9 5 9-5V8z"/><path d="m3 8 9 5 9-5"/><path d="M12 13v8"/></svg>',
    "ruler": '<svg viewBox="0 0 24 24"><path d="M3 17 17 3l4 4L7 21l-4-4z"/><path d="m7 13 2 2M10 10l2 2M13 7l2 2"/></svg>',
    "users": '<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="4"/><path d="M1 21v-1a7 7 0 0 1 14 0v1"/><path d="M17 4a4 4 0 0 1 0 8M23 21v-1a7 7 0 0 0-4-6.3"/></svg>',
    "truck": '<svg viewBox="0 0 24 24"><path d="M1 4h14v12H1zM15 9h4l4 4v3h-8"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/></svg>',
    "shield": '<svg viewBox="0 0 24 24"><path d="M12 2 4 5v6c0 5 3.5 9.5 8 11 4.5-1.5 8-6 8-11V5l-8-3z"/><path d="m9 12 2 2 4-4"/></svg>',
    "clock": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "tool": '<svg viewBox="0 0 24 24"><path d="M14.7 6.3a4 4 0 0 0 5 5L22 14l-8 8-2.3-2.3a4 4 0 0 0-5-5L2 10l8-8 2.3 2.3a4 4 0 0 0 2.4 2z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24"><path d="M12 22s8-7.2 8-13a8 8 0 1 0-16 0c0 5.8 8 13 8 13z"/><circle cx="12" cy="9" r="3"/></svg>',
}

def feature(icon, title, text):
    return f'<div class="feature"><div class="ico">{ICONS[icon]}</div><div><h3>{title}</h3><p>{text}</p></div></div>'

def gallery(items):
    """items: list of (image number, alt text)"""
    out = ['<div class="gallery">']
    for n, alt in items:
        out.append(f'<a href="images/full/{n}.jpg"><img src="images/thumb/{n}.jpg" alt="{e(alt)}" loading="lazy" width="640" height="480"></a>')
    out.append('</div>')
    return "\n".join(out)

def cta_band(title="Have drawings ready to bid?", text="Send plans, a sketch, or a sample part. We’ll come back with pricing and lead time.", btn="Request a Bid", href="contact.html"):
    return f'''
<section class="cta-band">
  <div class="container">
    <div><h2>{title}</h2><p>{text}</p></div>
    <div class="btn-row"><a class="btn btn-dark" href="{href}">{btn}</a></div>
  </div>
</section>'''

def page_hero(eyebrow, title, lead, crumb, img=None, buttons=""):
    img_html = f'<img src="images/full/{img}.jpg" alt="" fetchpriority="high">' if img else ""
    cls = "page-hero has-img" if img else "page-hero"
    return f'''
<section class="{cls}">
  {img_html}
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / {crumb}</div>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
    {buttons}
  </div>
</section>'''

def layout(filename, title, description, body, schema=True):
    addr_line = f'{S["street"]}, {S["city"]}, {S["state"]} {S["zip"]}'
    nav_html = "\n".join(
        f'<a href="{href}"{CUR if href == filename else ""}>{label}</a>' for href, label in NAV)
    phone_top = f'<a href="tel:{TEL}">{S["phone"]}</a>' if S["phone"] else ""
    phone_foot = f'<li><a href="tel:{TEL}">{S["phone"]}</a></li>' if S["phone"] else ""
    hours_foot = f'<li>{S["hours"]}</li>' if S["hours"] else ""
    canonical = S["site_url"] + "/" + ("" if filename == "index.html" else filename)
    ld = ""
    if schema:
        ld = f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"LocalBusiness","name":"{S["company"]}","alternateName":"{S["brand"]}",
"url":"{S["site_url"]}","email":"{S["email"]}",{('"telephone":"' + S["phone"] + '",') if S["phone"] else ""}
"image":"{S["site_url"]}/images/hero.jpg","logo":"{S["site_url"]}/images/r2-logo.png",
"address":{{"@type":"PostalAddress","streetAddress":"{S["street"]}","addressLocality":"{S["city"]}","addressRegion":"{S["state"]}","postalCode":"{S["zip"]}","addressCountry":"US"}},
"areaServed":"Dallas–Fort Worth, Texas","description":"HVAC ductwork fabrication, industrial metal fabrication, and commercial HVAC installation."}}
</script>'''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{S["site_url"]}/images/hero.jpg">
<meta name="theme-color" content="#FF6700">
<link rel="icon" type="image/png" sizes="32x32" href="images/icon-32.png">
<link rel="apple-touch-icon" href="images/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Barlow+Condensed:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar">
  <div class="container">
    <div class="tb-left"><span>{addr_line}</span>{phone_top}</div>
    <div class="tb-right"><a href="mailto:{S["email"]}">{S["email"]}</a><a href="contact.html?type=pickup">Stock pickup order</a></div>
  </div>
</div>
<header class="site-header">
  <div class="container">
    <a class="brand" href="index.html" aria-label="{S["brand"]} home">
      <img src="images/r2-logo.png" alt="" width="46" height="46">
      <span><span class="wordmark">TEAM <span>R2</span></span><span class="sub">Fabrication &amp; Installation</span></span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Menu"><span></span><span></span><span></span></button>
    <nav class="nav" id="site-nav" aria-label="Main">
      {nav_html}
      <a class="btn btn-primary" href="contact.html"{CUR if filename == "contact.html" else ""}>Request a Bid</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="container">
    <div class="foot-grid">
      <div>
        <div class="foot-brand"><img src="images/r2-logo.png" alt="" width="44" height="44"><span class="wordmark">TEAM <span>R2</span></span></div>
        <p>{S["company"]} fabricates HVAC ductwork and industrial metal work, and installs commercial HVAC systems, from our {S["sqft"]} sq. ft. shop in North Fort Worth.</p>
      </div>
      <div>
        <h4>What we do</h4>
        <ul>
          <li><a href="fabrication-hvac.html">Sheet metal &amp; HVAC duct</a></li>
          <li><a href="fabrication-misc.html">Industrial fabrication</a></li>
          <li><a href="installation-services.html">Installation</a></li>
          <li><a href="equipment.html">Shop &amp; equipment</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About R2</a></li>
          <li><a href="careers.html">Careers</a></li>
          <li><a href="contact.html">Request a bid</a></li>
          <li><a href="contact.html#location">Location</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:{S["email"]}">{S["email"]}</a></li>
          {phone_foot}
          <li>{S["street"]}<br>{S["city"]}, {S["state"]} {S["zip"]}</li>
          {hours_foot}
          <li><a href="{S["maps_link"]}" target="_blank" rel="noopener">Get directions →</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© <span id="year">{date.today().year}</span> {S["company"]}. All rights reserved.</span>
      <span><a href="privacy-policy.html">Privacy Policy</a><a href="sms.html">SMS Terms</a></span>
    </div>
  </div>
</footer>
<script src="js/site.js" defer></script>
</body>
</html>
'''

PAGES = {}

# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------
PAGES["index.html"] = ("Team R2 | HVAC Ductwork Fabrication & Installation | Fort Worth, TX",
"R2 Fabrication fabricates HVAC ductwork and industrial metal work and installs commercial HVAC systems for general and mechanical contractors across Dallas–Fort Worth.",
f'''
<section class="hero">
  <div class="hero-grid">
    <div class="hero-copy">
      <span class="eyebrow">Saginaw · North Fort Worth, TX</span>
      <h1>HVAC ductwork, fabricated and installed <em>by people who’ve done the job.</em></h1>
      <p class="lead">R2 Fabrication builds rectangular, spiral, and oval duct, industrial metal work, and specialty items for general and mechanical contractors across Dallas–Fort Worth, and our own crews can install it.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="contact.html">Request a Bid</a>
        <a class="btn btn-outline" href="fabrication-hvac.html">See what we build</a>
      </div>
    </div>
    <div class="hero-media">
      <img src="images/hero.jpg" alt="Automated duct coil line on the R2 shop floor" width="1920" height="745" fetchpriority="high">
      <div class="hero-tag"><strong>{S["sqft"]} sq. ft.</strong> fabrication shop</div>
    </div>
  </div>
</section>

<section class="proof" aria-label="At a glance">
  <div class="container">
    <div class="stat"><div class="num">{S["sqft"]}</div><div class="label">sq. ft. shop in North Fort Worth</div></div>
    <div class="stat"><div class="num">3</div><div class="label">divisions: ductwork, industrial, installation</div></div>
    <div class="stat"><div class="num">5</div><div class="label">metals: galvanized, carbon, stainless, aluminum, copper</div></div>
    <div class="stat"><div class="num">1/4″</div><div class="label">plate capacity for industrial work</div></div>
    <!-- IDEA: swap in real numbers once confirmed — years in business, lbs of duct per week, safety EMR -->
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Who we work with</span>
      <h2>One shop for the contractors who build DFW.</h2>
      <p class="lead">Buy fabrication only, or hand us fabrication and installation together.</p>
    </div>
    <div class="grid g3">
      <div class="card audience">
        <span class="tag">Mechanical contractors</span>
        <h3>Fabrication for your crews</h3>
        <ul>
          <li>Custom duct built to your drawings</li>
          <li>Rectangular, spiral, flat oval, snap lock</li>
          <li>Stock items ready for pickup</li>
          <li>No minimum order</li>
        </ul>
        <a class="more" href="fabrication-hvac.html">Sheet metal capabilities</a>
      </div>
      <div class="card audience dark">
        <span class="tag">General contractors</span>
        <h3>Fabrication + installation</h3>
        <ul>
          <li>We build and install our own duct</li>
          <li>From two-day jobs to multi-month projects</li>
          <li>Shop fabricates on demand for active jobs</li>
          <li>Crews led by experienced foremen</li>
        </ul>
        <a class="more" href="installation-services.html">Installation services</a>
      </div>
      <div class="card audience">
        <span class="tag">Industrial &amp; owners</span>
        <h3>Specialty and industrial builds</h3>
        <ul>
          <li>Dust collector duct, fume and grease exhaust</li>
          <li>Platforms, stairs, ladders, handrails</li>
          <li>Housings, hoppers, cyclones, ovens</li>
          <li>Built from drawings, a sample, or site measurements</li>
        </ul>
        <a class="more" href="fabrication-misc.html">Industrial fabrication</a>
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">What we build</span>
      <h2>From a single fitting to a full building’s duct.</h2>
    </div>
    <div class="grid g4">
      <a class="card" href="fabrication-hvac.html"><div class="card-img"><img src="images/thumb/15.jpg" alt="Rectangular duct sections being assembled" loading="lazy"></div><div class="card-body"><h3>Rectangular duct</h3><p>Custom duct and fittings in any gauge, built to order.</p><span class="more">Details</span></div></a>
      <a class="card" href="fabrication-hvac.html"><div class="card-img"><img src="images/thumb/41.jpg" alt="Spiral pipe machine" loading="lazy"></div><div class="card-body"><h3>Spiral &amp; flat oval</h3><p>Spiral pipe from two in-house spiral machines, flat oval, fittings, and long seam welded pipe.</p><span class="more">Details</span></div></a>
      <a class="card" href="fabrication-misc.html"><div class="card-img"><img src="images/thumb/01.jpg" alt="Custom stainless steel housing" loading="lazy"></div><div class="card-body"><h3>Industrial &amp; exhaust</h3><p>Grease duct, fume exhaust, housings, and ironwork up to 1/4″ plate.</p><span class="more">Details</span></div></a>
      <a class="card" href="installation-services.html"><div class="card-img"><img src="images/thumb/56.jpg" alt="Installed spiral duct in a commercial building" loading="lazy"></div><div class="card-body"><h3>Installation</h3><p>Commercial installs backed by our own shop.</p><span class="more">Details</span></div></a>
    </div>
  </div>
</section>

<section>
  <div class="container split">
    <div class="split-img"><img src="images/full/32.jpg" alt="R2 fabricator running the duct coil line" loading="lazy"></div>
    <div>
      <span class="eyebrow">Why R2</span>
      <h2>A shop run by metal workers.</h2>
      <p class="lead">Our people have worked this trade as installers, shop hands, foremen, and managers. We know what your job needs before you have to ask.</p>
      <div class="grid" style="gap:22px;margin-top:26px">
        {feature("clock", "Fast turnaround", "Fabrication and installation are under one roof, so we can build for active jobs without waiting on outside suppliers.")}
        {feature("box", "Stock and custom", "Common items are stocked for pickup. Custom orders come in any quantity, with no minimum.")}
        {feature("ruler", "Specialty builds", "We can build from drawings, copy an existing part, or measure on site. We take on work other shops turn down.")}
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">How it works</span>
      <h2>From drawings to installed duct</h2>
    </div>
    <ol class="steps">
      <li><h3>Send the scope</h3><p>Drawings, specs, a sketch, or a sample part.</p></li>
      <li><h3>Bid &amp; review</h3><p>We price the job and confirm lead time with you.</p></li>
      <li><h3>Fabricate</h3><p>Built in our shop from galvanized, stainless, aluminum, carbon steel, or copper.</p></li>
      <li><h3>Deliver or pick up</h3><p>We deliver to the job, or you pick up at our Saginaw shop.</p></li>
      <li><h3>Install</h3><p>Our crews can install it, or yours can.</p></li>
    </ol>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head" style="display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;max-width:none">
      <div><span class="eyebrow">Our work</span><h2 style="margin:0">From the shop floor</h2></div>
      <a class="btn btn-outline" href="equipment.html">Tour the shop</a>
    </div>
    {gallery([("09","Shop floor with duct fabrication lines"),("13","Fabricator working a sheet metal machine"),("21","CNC plasma cutting table"),("17","Galvanized round fitting"),("36","Duct sections on the roller line"),("38","Large-diameter ring fabrication"),("60","Custom enclosure with fan array"),("59","Painted steel platform frame")])}
  </div>
</section>
{cta_band()}
''')

# ---------------------------------------------------------------------------
# HVAC DUCTWORK
# ---------------------------------------------------------------------------
PAGES["fabrication-hvac.html"] = ("Sheet Metal & HVAC Duct Fabrication | Rectangular, Spiral & Oval | Team R2",
"Custom rectangular duct, spiral and flat oval pipe and fittings, snap lock, and angle rings, fabricated in Fort Worth, with stock items ready for pickup.",
page_hero("HVAC ductwork", "Sheet metal fabrication",
  f"Our {S['sqft']} sq. ft. shop in North Fort Worth builds HVAC duct in any quantity, and we keep common items in stock for quick pickup.",
  "Sheet Metal", img="13",
  buttons='<div class="btn-row"><a class="btn btn-primary" href="contact.html">Request a Bid</a><a class="btn btn-outline" style="color:#fff;border-color:#fff" href="contact.html?type=pickup">Order stock for pickup</a></div>')
+ f'''
<section>
  <div class="container">
    <div class="grid g2">
      <div class="panel">
        <h3>Custom fabricated to order</h3>
        <ul class="checklist">
          <li>Rectangular duct and fittings</li>
          <li>Spiral pipe and fittings</li>
          <li>Flat oval spiral pipe and fittings</li>
          <li>Long seam welded pipe</li>
          <li>Snap lock pipe and fittings</li>
          <li>Angle rings</li>
        </ul>
      </div>
      <div class="panel">
        <h3>Stocked for quick pickup</h3>
        <ul class="checklist">
          <li>Snap lock pipe and fittings</li>
          <li>Flexible duct</li>
          <li>Dampers</li>
          <li>Access doors</li>
          <li>Angle rings</li>
          <li>Sealer and fasteners</li>
        </ul>
        <a class="btn btn-dark" href="contact.html?type=pickup" style="margin-top:6px">Place a pickup order</a>
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container split">
    <div>
      <span class="eyebrow">Materials</span>
      <h2>The metal your spec calls for.</h2>
      <p>We build HVAC and exhaust duct from any of these metals, in the gauge your project requires.</p>
      <ul class="pill-list" style="margin-top:20px">
        <li>Galvanized steel</li><li>Carbon steel</li><li>Stainless steel</li><li>Aluminum</li><li>Copper</li>
      </ul>
      <!-- IDEA: add gauge/size ranges per product once confirmed (e.g. rectangular 26–10 ga, spiral diameter range) -->
    </div>
    <div class="split-img"><img src="images/full/34.jpg" alt="Coils of sheet metal staged on the shop floor" loading="lazy"></div>
  </div>
</section>

<section>
  <div class="container split flip">
    <div>
      <span class="eyebrow">Bid faster</span>
      <h2>What to send us</h2>
      <p>The more we have up front, the faster and tighter the number.</p>
      <ul class="checklist">
        <li>Mechanical drawings and specs, or a shop drawing set</li>
        <li>Duct types and materials (galvanized, stainless, etc.)</li>
        <li>Pressure class or construction requirements, if specified</li>
        <li>Bid due date and when you need material on site</li>
        <li>Fabrication only, or fabrication and installation</li>
      </ul>
      <a class="btn btn-primary" href="contact.html">Start a bid request</a>
    </div>
    <div class="split-img"><img src="images/full/20.jpg" alt="Rectangular-to-round duct transition" loading="lazy"></div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Gallery</span><h2>Inside the shop</h2></div>
    {gallery([("01","Stainless housing with access doors"),("09","Duct fabrication area"),("12","Ironworker"),("14","Transition plenum"),("15","Duct assembly"),("16","Fabricated plenum"),("17","Round fitting"),("20","Rectangular-to-round transition"),("25","Duct with test port"),("27","Fabricator at machine"),("28","Roll forming line"),("31","Shop interior"),("33","Coil racks"),("36","Duct roller line"),("45","Curved duct panel"),("53","Custom transition fitting")])}
  </div>
</section>
{cta_band("Need duct for your next job?", "Custom orders, bulk quantities, or stock for pickup. Tell us what you need.")}
''')

# ---------------------------------------------------------------------------
# INDUSTRIAL
# ---------------------------------------------------------------------------
PAGES["fabrication-misc.html"] = ("Industrial Metal Fabrication | Exhaust, Ironwork & Specialty Builds | Team R2",
"Industrial fabrication up to 1/4 inch plate: dust collector duct, fume and grease exhaust, platforms, handrails, housings, hoppers, cyclones, and ovens.",
page_hero("Industrial division", "Industrial fabrication",
  "Structural ironwork, exhaust and ventilation systems, and custom specialty builds up to 1/4″ plate. We take the jobs other shops turn away.",
  "Industrial", img="30",
  buttons='<div class="btn-row"><a class="btn btn-primary" href="contact.html?type=industrial">Talk to us about a build</a></div>')
+ f'''
<section>
  <div class="container">
    <div class="grid g2">
      <div class="panel">
        <h3>Industrial capabilities</h3>
        <ul class="checklist">
          <li>Working capacity to 1/4″ plate</li>
          <li>Ironwork: structural angles, channels, and beams</li>
          <li>Ladders, stairs, platforms, and handrails</li>
          <li>Duct and connections for dust collectors</li>
          <li>Fume exhaust systems</li>
          <li>HEPA air cleaners</li>
          <li>Grease duct systems</li>
        </ul>
      </div>
      <div class="panel">
        <h3>Specialty items</h3>
        <ul class="checklist cols-2">
          <li>Sound attenuators</li>
          <li>Braces and supports</li>
          <li>Housings</li>
          <li>Ovens (up to 6′ H × 8′ W × 30′ L)</li>
          <li>Battery racks</li>
          <li>Stainless steel filter racks</li>
          <li>Cage ladders</li>
          <li>Platforms and handrails</li>
          <li>Hoppers and cyclones</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container split">
    <div class="split-img"><img src="images/full/54.jpg" alt="Large custom steel enclosure" loading="lazy"></div>
    <div>
      <span class="eyebrow">Specialty work</span>
      <h2>Have a project no one else will take?</h2>
      <p class="lead">Along with HVAC and industrial work, we do the specialty jobs you and your customers need.</p>
      <div class="grid" style="gap:20px;margin-top:22px">
        {feature("ruler", "Built from drawings", "Send your drawings or specs and we’ll build to them.")}
        {feature("layers", "Copied from a sample", "Bring an existing part and we’ll reproduce it.")}
        {feature("pin", "Measured on site", "We can come measure the space and build to fit.")}
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head"><span class="eyebrow">Gallery</span><h2>Industrial work</h2></div>
    {gallery([("30","Industrial fabrication bay"),("22","Housing with fan array"),("24","Stainless filter housing"),("35","Air cleaner enclosure"),("37","Rooftop equipment housing"),("38","Large-diameter ring"),("46","Stainless housing interior"),("47","Fan housing"),("48","Fan array enclosure"),("51","Fabricated panel"),("52","Steel framing"),("54","Custom steel enclosure"),("55","Bolted access panel"),("58","Steel frame assembly"),("59","Painted platform frame"),("43","Duct and structural steel")])}
  </div>
</section>
{cta_band("Let’s solve your fabrication problem.", "No minimum order. Built to your spec. Fast turnaround.", "Talk to Us", "contact.html?type=industrial")}
''')

# ---------------------------------------------------------------------------
# INSTALLATION
# ---------------------------------------------------------------------------
PAGES["installation-services.html"] = ("Commercial HVAC Duct Installation | Dallas–Fort Worth | Team R2",
"Commercial HVAC ductwork installation across DFW, backed by R2's own fabrication shop. From two-day jobs to multi-month projects.",
page_hero("Installation division", "Commercial installation",
  "From a two-day job to a multi-month commercial build-out, our own shop builds the duct and our own crews install it.",
  "Installation", img="10",
  buttons='<div class="btn-row"><a class="btn btn-primary" href="contact.html?type=install">Request an install bid</a></div>')
+ f'''
<section>
  <div class="container">
    <div class="section-head"><span class="eyebrow">The R2 advantage</span><h2>Installation backed by our own shop</h2>
      <p class="lead">We run the shop and the install crew, so we control the schedule from start to finish and never wait on an outside supplier.</p></div>
    <div class="grid g3">
      {feature("bolt", "Faster lead times", "Our shop builds on demand for our active install jobs, so you get material sooner.")}
      {feature("layers", "Projects big and small", "Two days of work or a months-long commercial project get the same experience and urgency.")}
      {feature("users", "Experienced crews", "Our installers, foremen, and managers have worked every part of this trade.")}
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container split">
    <div class="split-img"><img src="images/full/57.jpg" alt="Installed ductwork and equipment" loading="lazy"></div>
    <div>
      <span class="eyebrow">Scope</span>
      <h2>What our crews install</h2>
      <ul class="checklist">
        <li>Rectangular, spiral, and flat oval supply, return, and exhaust duct</li>
        <li>Grease duct and fume exhaust systems</li>
        <li>Dust collector duct and connections</li>
        <li>Supports, hangers, and bracing</li>
        <li>Specialty housings and equipment built in our shop</li>
      </ul>
      <!-- CONFIRM this scope list with the install team before publishing -->
      <a class="btn btn-primary" href="contact.html?type=install">Tell us about your project</a>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head"><span class="eyebrow">Gallery</span><h2>Installation projects</h2></div>
    {gallery([("10","Installed duct and walkway"),("02","Service walkway with ductwork"),("08","Installed equipment housing"),("18","Duct run at ceiling"),("19","Installed grille"),("23","Spiral duct at ceiling"),("39","Exposed spiral duct"),("40","Spiral duct under roof trusses"),("43","Rectangular duct installation"),("49","Commercial project"),("50","Exposed round duct"),("56","Installed spiral duct"),("57","Mechanical room"),("60","Custom enclosure installed"),("61","Fabricator at press brake"),("26","Installed equipment")])}
  </div>
</section>
{cta_band("Have an install project?", "Tell us the scope. We’ll help you plan it and build it faster than you expect.", "Get a Quote", "contact.html?type=install")}
''')

# ---------------------------------------------------------------------------
# EQUIPMENT
# ---------------------------------------------------------------------------
PAGES["equipment.html"] = ("Shop & Equipment | Team R2 Fabrication | Saginaw, TX",
f"Inside R2's {S['sqft']} sq. ft. fabrication shop in North Fort Worth: coil line, CNC plasma and laser cutting, two spiral machines, shears, press brakes, and more.",
page_hero("Shop & equipment", "Our shop",
  f"{S['sqft']} sq. ft. in Saginaw, set up to build the full range of HVAC and industrial sheet metal.",
  "Shop &amp; Equipment", img="31")
+ f'''
<section>
  <div class="container">
    <div class="section-head"><span class="eyebrow">Equipment</span><h2>What’s on the floor</h2>
      <p class="lead">Contractors ask what we run before they send work. Here’s the short list.</p></div>
    <!-- CONFIRM each row (machine type, count, and capacity) before publishing. Add a "Capacity" column when numbers are known. -->
    <div class="table-wrap">
    <table class="equip">
      <thead><tr><th>Equipment</th><th>What it does for your job</th></tr></thead>
      <tbody>
        <tr><td>Automated coil line</td><td>Uncoils, flattens, notches, and cuts sheet for rectangular duct straight from the coil.</td></tr>
        <tr><td>CNC plasma cutting table</td><td>Cuts fittings, transitions, and heavier-gauge parts from nested layouts.</td></tr>
        <tr><td>CNC laser cutting table</td><td>Clean, precise cuts for detailed parts, stainless, and specialty work.</td></tr>
        <tr><td>Spiral pipe machines (2)</td><td>Two machines forming spiral round pipe in-house, so round duct doesn’t wait in line.</td></tr>
        <tr><td>Roll formers / lockformers</td><td>Form Pittsburgh locks, seams, and connectors.</td></tr>
        <tr><td>Power shears</td><td>Cut sheet and plate to size.</td></tr>
        <tr><td>Press brakes</td><td>Bend panels, angles, and heavy-gauge parts.</td></tr>
        <tr><td>Ironworker</td><td>Punches, notches, and cuts angle, flat bar, and channel for supports and structural work.</td></tr>
        <tr><td>Spot and MIG/TIG welding</td><td>Welds galvanized, carbon, stainless, and aluminum, including long seam welded pipe and grease duct.</td></tr>
        <tr><td>Forklifts and shipping dock</td><td>Stage and load orders for delivery or will-call pickup.</td></tr>
      </tbody>
    </table>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="grid g3">
      <div class="card"><div class="card-img"><img src="images/thumb/21.jpg" alt="CNC plasma cutting table" loading="lazy"></div><div class="card-body"><h3>Cutting</h3><p>CNC plasma and laser tables, shears, and the coil line handle everything from light-gauge duct to 1/4″ plate.</p></div></div>
      <div class="card"><div class="card-img"><img src="images/thumb/41.jpg" alt="Spiral pipe machine" loading="lazy"></div><div class="card-body"><h3>Forming</h3><p>Two spiral machines, roll formers, and press brakes for round, oval, and rectangular work.</p></div></div>
      <div class="card"><div class="card-img"><img src="images/thumb/13.jpg" alt="Fabricator at spot welder" loading="lazy"></div><div class="card-body"><h3>Assembly &amp; welding</h3><p>Spot, MIG, and TIG welding for duct, housings, and industrial builds.</p></div></div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head"><span class="eyebrow">Gallery</span><h2>Around the shop</h2></div>
    {gallery([("31","Main shop bay"),("09","Duct lines"),("32","Coil line"),("33","Coil racks"),("34","Coil storage"),("21","CNC plasma"),("41","Spiral pipe machine"),("28","Roll former"),("12","Ironworker"),("13","Spot welder"),("27","Fabricator at work"),("49","Power shear"),("62","Power shear"),("61","Press brake"),("06","Loading dock and staging"),("03","Shop exterior")])}
  </div>
</section>
{cta_band("Want to see it in person?", "Contractors are welcome to visit the shop. Let us know when you’d like to come by.", "Schedule a visit", "contact.html?type=general")}
''')

# ---------------------------------------------------------------------------
# ABOUT
# ---------------------------------------------------------------------------
PAGES["about.html"] = ("About R2 Fabrication | Team R2 | Fort Worth, TX",
"R2 Fabrication, LLC supplies HVAC ductwork and industrial fabrication, with an install division behind it. Our team has worked every job in the trade.",
page_hero("About R2", "Built on decades in the trade.",
  "R2 Fabrication, LLC supplies HVAC ductwork and industrial fabrication, with an install division that backs it all up.",
  "About", img="36")
+ f'''
<section>
  <div class="container split">
    <div>
      <span class="eyebrow">Our story</span>
      <h2>A shop run by people who know the trade.</h2>
      <p>R2 Fabrication gives our partners one source for fabricated ductwork, industrial items, and specialty needs. Metal workers who have been in the trade for decades run and manage our shop.</p>
      <p>From the shop floor to upper management, we’ve worked as installers, shop hands, shop foremen, and managers. We understand the business and what it takes to give you and your customers first-class products and service.</p>
      <p>Every day we build items for the HVAC industry, for industrial applications, and for specific products inside and outside HVAC. If you have a product that needs to be fabricated, we want to work with you.</p>
      <!-- IDEA: add founding year and a short founder/leadership note here -->
    </div>
    <div class="split-img"><img src="images/full/03.jpg" alt="R2 Fabrication facility in Saginaw, Texas" loading="lazy"></div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head"><span class="eyebrow">What you can expect</span><h2>How we work</h2></div>
    <div class="grid g2">
      {feature("users", "Trade experience at every level", "The people quoting and managing your job have done the work themselves.")}
      {feature("clock", "Speed", "Our fabrication and installation work together, so lead times stay short.")}
      {feature("box", "No minimums", "One fitting or a full building. We treat both the same.")}
      {feature("tool", "Specialty capability", "Drawings, samples, or site measurements, we can build it.")}
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head"><span class="eyebrow">Safety &amp; standards</span><h2>Built right, built safe</h2>
      <p class="lead">Our duct is built to the construction standards your project specifies, and our crews work safely in the shop and on site.</p></div>
    <!--
      IDEA: GC prequalification teams look for these. Add the real values and remove this comment:
      <div class="grid g4">
        <div class="panel"><h3>EMR</h3><p>0.xx</p></div>
        <div class="panel"><h3>SMACNA</h3><p>HVAC Duct Construction Standards, 4th ed. (2020)</p></div>
        <div class="panel"><h3>OSHA</h3><p>OSHA 10/30 trained crews</p></div>
        <div class="panel"><h3>Licensing</h3><p>TACLA #_____</p></div>
      </div>
    -->
    <div class="grid g3">
      {feature("shield", "Safety first", "Safety training for our shop and field crews. Ask us for our safety documentation for your prequalification file.")}
      {feature("ruler", "Built to spec", "Gauge, reinforcement, and seams built to your project’s specified construction standard.")}
      {feature("truck", "Serving DFW", "Based in Saginaw and serving Fort Worth, Dallas, Arlington, Denton, and all of North Texas.")}
    </div>
  </div>
</section>
{cta_band("Got a project for us?", "A standard ductwork order or a specialty build nobody else will attempt, let’s talk.", "Get in Touch")}
''')

# ---------------------------------------------------------------------------
# CAREERS
# ---------------------------------------------------------------------------
PAGES["careers.html"] = ("Careers | Sheet Metal & HVAC Jobs in Fort Worth | Team R2",
"Join R2 Fabrication. We hire sheet metal fabricators, installers, welders, and shop staff in Saginaw / North Fort Worth. See open jobs on Indeed.",
page_hero("Careers", "Build with R2.",
  "We’re a shop run by tradespeople, and we’re always looking for good people who want to build.",
  "Careers", img="61",
  buttons=f'<div class="btn-row"><a class="btn btn-primary" href="{S["indeed_url"]}" target="_blank" rel="noopener">See open jobs on Indeed</a></div>')
+ f'''
<section>
  <div class="container split">
    <div>
      <span class="eyebrow">Why work here</span>
      <h2>Learn from people who’ve done the job.</h2>
      <p>Our leaders came up through the trade as installers, shop hands, foremen, and managers. If you want to learn sheet metal the right way, or you already know it and want a shop that respects that, we want to hear from you.</p>
      <div class="grid" style="gap:20px;margin-top:22px">
        {feature("tool", "Real fabrication work", "HVAC duct, industrial builds, and specialty jobs keep the work varied.")}
        {feature("users", "Room to grow", "Move from helper to fabricator, installer to foreman.")}
        {feature("pin", "Location", f"{S['street']}, {S['city']}, {S['state']}, in North Fort Worth.")}
      </div>
    </div>
    <div class="split-img"><img src="images/full/27.jpg" alt="R2 team member at work in the shop" loading="lazy"></div>
  </div>
</section>

<section class="section-alt">
  <div class="container center" style="max-width:760px;text-align:center">
    <span class="eyebrow">Open positions</span>
    <h2>Current openings are posted on Indeed.</h2>
    <p class="lead center">We post every open job on Indeed, where you can read the details and apply.</p>
    <!-- IDEA: typical roles to mention once confirmed: sheet metal fabricator, HVAC duct installer, welder, apprentice/helper, CAD detailer, driver -->
    <div class="btn-row" style="justify-content:center;margin-top:10px">
      <a class="btn btn-primary" href="{S["indeed_url"]}" target="_blank" rel="noopener">View jobs on Indeed</a>
      <a class="btn btn-outline" href="contact.html?type=careers">Ask about a job</a>
    </div>
  </div>
</section>
''')

# ---------------------------------------------------------------------------
# CONTACT / QUOTE
# ---------------------------------------------------------------------------
PAGES["contact.html"] = ("Request a Bid | Contact Team R2 | Saginaw, TX",
"Request a bid for HVAC ductwork, industrial fabrication, or installation. Send your project details and drawings link to R2 Fabrication.",
page_hero("Contact", "Request a bid",
  "Tell us about your project. The more detail you send, the faster we can price it. For quick questions, email us directly.",
  "Contact")
+ f'''
<section>
  <div class="container contact-grid">
    <div class="panel">
      <form id="quote-form" action="https://api.web3forms.com/submit" method="POST">
        <input type="hidden" name="access_key" value="{S["web3forms_key"]}">
        <input type="hidden" name="from_name" value="TeamR2.com website">
        <input type="hidden" name="subject" value="Website inquiry">
        <input type="hidden" name="redirect" value="{S["site_url"]}/thanks.html">
        <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">

        <div class="form-grid">
          <div class="full">
            <label for="request_type">What can we help with? <span class="req">*</span></label>
            <select id="request_type" name="request_type" required>
              <option data-key="fab" value="Bid request: ductwork fabrication">Bid request: ductwork fabrication</option>
              <option data-key="fabinstall" value="Bid request: fabrication + installation">Bid request: fabrication + installation</option>
              <option data-key="install" value="Installation only">Installation only</option>
              <option data-key="industrial" value="Industrial / specialty fabrication">Industrial / specialty fabrication</option>
              <option data-key="pickup" value="Stock order for pickup">Stock order for pickup</option>
              <option data-key="general" value="General question">General question</option>
              <option data-key="careers" value="Careers question">Careers question</option>
            </select>
          </div>

          <h3 class="form-section">Your info</h3>
          <div><label for="name">Name <span class="req">*</span></label><input id="name" name="name" type="text" autocomplete="name" required></div>
          <div><label for="company">Company <span class="req">*</span></label><input id="company" name="company" type="text" autocomplete="organization" required></div>
          <div><label for="email">Email <span class="req">*</span></label><input id="email" name="email" type="email" autocomplete="email" required></div>
          <div><label for="phone">Phone <span class="req">*</span></label><input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
          <div class="full">
            <label for="role">You are a…</label>
            <select id="role" name="role">
              <option value="">Select one</option>
              <option>Mechanical contractor</option>
              <option>General contractor</option>
              <option>Building owner / facility</option>
              <option>Industrial / manufacturer</option>
              <option>Other</option>
            </select>
          </div>

          <h3 class="form-section">Project <span class="hint">(skip for general questions)</span></h3>
          <div><label for="project_name">Project name</label><input id="project_name" name="project_name" type="text"></div>
          <div><label for="project_city">Project city</label><input id="project_city" name="project_city" type="text" placeholder="e.g. Fort Worth"></div>
          <div><label for="bid_date">Bid due date</label><input id="bid_date" name="bid_date" type="date"></div>
          <div><label for="need_by">Material needed on site by</label><input id="need_by" name="need_by" type="date"></div>
          <fieldset class="full">
            <legend>Duct / item types</legend>
            <div class="checks">
              <label><input type="checkbox" name="duct_types[]" value="Rectangular"> Rectangular</label>
              <label><input type="checkbox" name="duct_types[]" value="Spiral round"> Spiral round</label>
              <label><input type="checkbox" name="duct_types[]" value="Flat oval"> Flat oval</label>
              <label><input type="checkbox" name="duct_types[]" value="Snap lock"> Snap lock</label>
              <label><input type="checkbox" name="duct_types[]" value="Welded / grease"> Welded / grease</label>
              <label><input type="checkbox" name="duct_types[]" value="Industrial / exhaust"> Industrial / exhaust</label>
              <label><input type="checkbox" name="duct_types[]" value="Specialty item"> Specialty item</label>
            </div>
          </fieldset>
          <fieldset class="full">
            <legend>Materials</legend>
            <div class="checks">
              <label><input type="checkbox" name="materials[]" value="Galvanized"> Galvanized</label>
              <label><input type="checkbox" name="materials[]" value="Stainless"> Stainless</label>
              <label><input type="checkbox" name="materials[]" value="Aluminum"> Aluminum</label>
              <label><input type="checkbox" name="materials[]" value="Carbon / black iron"> Carbon / black iron</label>
              <label><input type="checkbox" name="materials[]" value="Copper"> Copper</label>
              <label><input type="checkbox" name="materials[]" value="Not sure"> Not sure</label>
            </div>
          </fieldset>
          <div class="full">
            <label for="plans_link">Link to drawings / specs <span class="hint">(Dropbox, Google Drive, OneDrive, Box, plan room…)</span></label>
            <input id="plans_link" name="plans_link" type="url" placeholder="https://">
          </div>
          <div class="full">
            <label for="message">Tell us about the job <span class="req">*</span></label>
            <textarea id="message" name="message" required placeholder="Scope, quantities, sizes, anything special. For pickup orders, list items and when you’ll pick up."></textarea>
          </div>
          <div class="full">
            <label for="heard">How did you hear about us?</label>
            <input id="heard" name="heard" type="text">
          </div>
          <div class="full">
            <label class="consent"><input type="checkbox" name="sms_consent" value="Yes - opted in to SMS order/delivery updates">
              <span>Optional: text me order and delivery updates from R2 Fabrication, LLC. Message frequency varies (about 3–5 per order). Message and data rates may apply. Reply STOP to cancel, HELP for help. Consent isn’t required to do business with us. See our <a href="sms.html">SMS Terms</a> and <a href="privacy-policy.html">Privacy Policy</a>.</span></label>
          </div>
          <div class="full">
            <button class="btn btn-primary" type="submit">Send request</button>
            <div id="form-status" class="form-status" role="status" aria-live="polite"></div>
          </div>
        </div>
      </form>
    </div>

    <aside>
      <div class="panel" style="margin-bottom:24px">
        <div class="info-block"><h3>Email</h3><p><a href="mailto:{S["email"]}">{S["email"]}</a></p></div>
        {f'<div class="info-block"><h3>Phone</h3><p><a href="tel:{TEL}">{S["phone"]}</a></p></div>' if S["phone"] else ""}
        <div class="info-block"><h3>Shop &amp; pickup</h3><p>{S["street"]}<br>{S["city"]}, {S["state"]} {S["zip"]}</p></div>
        {f'<div class="info-block"><h3>Hours</h3><p>{S["hours"]}</p></div>' if S["hours"] else ""}
        <div class="info-block"><h3>Careers</h3><p><a href="careers.html">See open positions →</a></p></div>
      </div>
      <div id="location">
        <iframe class="map" src="{S["maps_embed"]}" title="Map to R2 Fabrication" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        <p style="margin-top:10px"><a href="{S["maps_link"]}" target="_blank" rel="noopener">Open in Google Maps →</a></p>
      </div>
    </aside>
  </div>
</section>
''')

# ---------------------------------------------------------------------------
# THANKS / 404 / LOCATION redirect
# ---------------------------------------------------------------------------
PAGES["thanks.html"] = ("Thank You | Team R2", "Thanks for contacting R2 Fabrication.",
page_hero("Message sent", "Thank you.", "We got your request and will get back to you shortly.", "Thanks",
  buttons='<div class="btn-row"><a class="btn btn-primary" href="index.html">Back to home</a></div>'))

PAGES["404.html"] = ("Page Not Found | Team R2", "Page not found.",
page_hero("404", "We can’t find that page.", "It may have moved when we rebuilt the site.", "Not found",
  buttons='<div class="btn-row"><a class="btn btn-primary" href="index.html">Home</a><a class="btn btn-outline" href="contact.html">Contact us</a></div>'))

# ---------------------------------------------------------------------------
# PRIVACY + SMS (based on the policies on the current live site — have them reviewed)
# ---------------------------------------------------------------------------
PAGES["privacy-policy.html"] = ("Privacy Policy | R2 Fabrication, LLC", "Privacy policy for www.TeamR2.com and the R2 Fabrication SMS program.",
page_hero("Legal", "Privacy Policy", "Effective date: April 20, 2026", "Privacy Policy") + f'''
<section><div class="container prose">
<p>{S["company"]} (“R2,” “we,” “us”) respects the privacy of every individual who interacts with our services, including visitors to www.TeamR2.com and participants in our SMS program. By providing personal information or opting in to messages, you agree to this policy.</p>
<h2>Information we collect</h2>
<ul><li>Contact details such as name, phone number, email, and address</li><li>Project and business information</li><li>Service and transaction records</li><li>Records of communications with us</li><li>Device and usage data collected through cookies</li><li>Records of SMS consent</li></ul>
<h2>How we collect it</h2>
<p>Directly from you, through SMS interactions, automatically through website cookies, from third-party sources, and from orders placed in person.</p>
<h2>SMS / text messaging</h2>
<p>If you consent to receive texts, we may send messages about appointments, project updates, quotes, and orders or deliveries. Message frequency varies based on your interactions. Message and data rates may apply. Reply STOP at any time to opt out; you will receive one final confirmation message. See our <a href="sms.html">SMS Terms</a>.</p>
<h2>How we use information</h2>
<p>To provide our services, communicate about orders, process transactions, send messages you opted in to, respond to inquiries, and comply with legal obligations.</p>
<h2>Sharing</h2>
<p>We do not sell, rent, or trade your personal information. We share it only with service providers who help us operate, when required by law, or as part of a business transfer. Mobile opt-in data and consent are not shared with third parties for marketing purposes.</p>
<h2>Security and retention</h2>
<p>We use reasonable safeguards to protect your information, but no method of electronic transmission or storage is completely secure. We keep information only as long as needed for the purposes above.</p>
<h2>Your rights</h2>
<p>Depending on where you live, you may request access to, correction of, or deletion of your personal information by contacting us.</p>
<h2>Contact</h2>
<p>Email: <a href="mailto:{S["email"]}">{S["email"]}</a><br>{S["company"]}, {S["street"]}, {S["city"]}, {S["state"]} {S["zip"]}</p>
</div></section>''')

PAGES["sms.html"] = ("SMS Terms | R2 Fabrication, LLC", "Terms for the R2 Fabrication order and delivery text message program.",
page_hero("Legal", "SMS Terms", "R2 Fabrication, LLC order and delivery text notifications", "SMS Terms") + f'''
<section><div class="container prose">
<h2>Program description</h2>
<p>{S["company"]} sends order-specific text notifications, such as order status and delivery updates, to customers who opt in.</p>
<h2>Message frequency</h2>
<p>About 3–5 messages per order or delivery. Message and data rates may apply.</p>
<h2>Opting out</h2>
<p>Text <strong>STOP</strong> at any time to cancel. You will receive one confirmation message, and no further messages will be sent. Text <strong>HELP</strong> for help, or email <a href="mailto:{S["email"]}">{S["email"]}</a>.</p>
<h2>Carriers</h2>
<p>Carriers are not liable for delayed or undelivered messages.</p>
<h2>Privacy</h2>
<p>We will not share your information with third parties, excluding aggregators and providers of the text messaging services. See our <a href="privacy-policy.html">Privacy Policy</a>.</p>
</div></section>''')

# old location page → send people to the contact page's map
LOCATION_REDIRECT = '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=contact.html#location"><link rel="canonical" href="%s/contact.html">
<title>Location | Team R2</title></head><body><p><a href="contact.html#location">Our location has moved to the Contact page.</a></p></body></html>
''' % S["site_url"]

def main():
    for fn, (title, desc, body) in PAGES.items():
        with open(os.path.join(OUT, fn), "w", encoding="utf-8", newline="\n") as f:
            f.write(layout(fn, title, desc, body, schema=(fn == "index.html")))
    with open(os.path.join(OUT, "location.html"), "w", encoding="utf-8") as f:
        f.write(LOCATION_REDIRECT)
    urls = [p for p in PAGES if p not in ("thanks.html", "404.html")]
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for p in urls:
            loc = S["site_url"] + "/" + ("" if p == "index.html" else p)
            f.write(f"  <url><loc>{loc}</loc><lastmod>{date.today().isoformat()}</lastmod></url>\n")
        f.write("</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {S['site_url']}/sitemap.xml\n")
    print("Built", len(PAGES) + 1, "pages into", OUT)

if __name__ == "__main__":
    main()
