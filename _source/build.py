"""Ocmand Construction website generator.

Writes every page of ocmandconstruction.com (plus sitemap.xml, robots.txt and _redirects) into the
repository root, which is what Cloudflare Pages publishes. Edit the text and project list in this
file, then run:   python3 _source/build.py
Never edit the generated .html files by hand - the next build overwrites them.
styles.css and site.js in the repository root are hand-written source, not generated.
See CLAUDE.md in the repository root for the full playbook.
"""
import json, html, os
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
PREVIEW=os.environ.get('PREVIEW')=='1'            # click-through preview build, made by make_preview.py
OUT=os.environ.get('OUT') or ROOT
if PREVIEW and os.path.abspath(OUT)==ROOT: raise SystemExit('A preview build needs its own folder - run _source/make_preview.py instead.')
LASTMOD='2026-11-16'                               # sitemap date - bump when page content changes
HOME='index.html' if PREVIEW else './'
DL='https://developinglafayette.com/wp/bangkok-thai-to-anchor-new-center-on-johnston-street/'
SITE='https://ocmandconstruction.com'
MAIL='jobs@ocmandconstruction.com'
GA='''<script async src="https://www.googletagmanager.com/gtag/js?id=G-M17NYKK31T"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-M17NYKK31T');</script>'''
DIM={1:(1600,1600),5:(1200,1600),6:(1200,1600)}
def img(n,alt,sizes='(max-width:900px) 100vw, 50vw',lazy=True):
    w,h=DIM.get(n,(1600,1200)); f=f'project-{n:02d}'
    return f'<img src="{f}.jpg" srcset="{f}-800.jpg 800w, {f}.jpg 1600w" sizes="{sizes}" width="{w}" height="{h}" alt="{alt}"{" loading=\"lazy\" decoding=\"async\"" if lazy else " fetchpriority=\"high\""}>'
def tb(name,loc,typ):
    return f'<dl class="tb"><div><dt>Project</dt><dd>{name}</dd></div><div><dt>Location</dt><dd>{loc}</dd></div><div><dt>Type</dt><dd>{typ}</dd></div></dl>'
# n, name, location, type, category, alt
P=[(11,'Breaux Bridge Eye Care','Breaux Bridge, LA','Medical office','commercial','Brick medical office building with a metal awning, built by Ocmand Construction'),
   (10,"Buck &amp; Johnny's",'Breaux Bridge, LA','Restaurant','commercial','Two-story masonry restaurant building on a downtown corner'),
   (8,'Retail and office center','Louisiana','Retail and office','commercial','Single-story multi-tenant retail and office center with a parking lot'),
   (1,'Historic downtown restoration','Louisiana','Restoration','commercial','Two-story historic commercial building with wraparound galleries'),
   (12,'Parc Hardy pavilion','Breaux Bridge, LA','Public park','commercial','Open-air park pavilions with red metal roofs'),
   (9,'Historic Acadian cottage','Louisiana','Restoration','commercial','Restored Acadian cottage with a metal roof under live oaks')]
PD={p[0]:p for p in P}
def shot(n,cls='',sizes='(max-width:900px) 100vw, 50vw',lazy=True,href=None,reveal=True,d=0):
    _,name,loc,typ,cat,alt=PD[n]
    tag='a' if href else 'figure'; h=f' href="{href}"' if href else ''
    r=f' data-reveal style="--d:{d}s"' if reveal else ''
    return f'<{tag} class="shot {cls}"{h}{r}><div class="frame">{img(n,alt,sizes,lazy)}</div>{tb(name,loc,typ)}</{tag}>'
ARROW='<span class="go" aria-hidden="true"><svg viewBox="0 0 16 16"><path d="M2 8h11M9 3.5 13.5 8 9 12.5"/></svg></span>'
MARKETS=[('commercial-construction.html','Ground-up commercial','New commercial buildings, from site preparation through final completion.'),
 ('restaurant-retail.html','Restaurant and retail','New restaurants, retail centers and tenant build-outs.'),
 ('healthcare-occupied.html','Healthcare and occupied facilities','Renovations in hospitals, clinics and other facilities that remain open during construction.'),
 ('public-works.html','Public works','Construction for parish, municipal and state agencies.'),
 ('metal-buildings.html','Pre-engineered metal buildings','Metal building systems for commercial use, complete from foundation to finish.'),
 ('concrete-sitework.html','Concrete and site work','Foundations, slabs, paving, drainage and site utilities.')]
def markets():
    return '<ul class="markets">'+''.join(f'<li data-reveal><a href="{u}"><span class="name">{n}</span><span class="desc">{d}</span>{ARROW}</a></li>' for u,n,d in MARKETS)+'</ul>'
NAVMENU=''.join(f'<a href="{u}">{n}</a>' for u,n,_ in MARKETS)
def header(cur):
    def a(u,t): return f'<a href="{u}"{" aria-current=\"page\"" if cur==u else ""}>{t}</a>'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{HOME}" aria-label="Ocmand Construction Co., LLC, home"><svg viewBox="0 0 1954.7 284" role="img" aria-hidden="true"><use href="logo.svg#lockup"/></svg></a>
    <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="Main">
      <div class="has-menu">{a('services.html','Markets')}
        <div class="menu">{NAVMENU}</div>
      </div>
      {a('projects.html','Projects')}{a('approach.html','How we work')}{a('about.html','About')}{a('contact.html','Contact')}
      <a class="btn light" href="contact.html#bid">Request a bid</a>
    </nav>
  </div>
</header>'''
FOOT=f'''<footer class="site-footer">
  <div class="wrap top">
    <div>
      <a class="f-logo" href="{HOME}" aria-label="Ocmand Construction Co., LLC"><svg viewBox="0 0 841.3 410" aria-hidden="true"><use href="logo.svg#stacked"/></svg></a>
      <p class="blurb">A family-owned commercial general contractor. New construction, renovations and public works.</p>
    </div>
    <div><h3>Markets</h3><ul>{''.join(f'<li><a href="{u}">{n}</a></li>' for u,n,_ in MARKETS)}</ul></div>
    <div><h3>Company</h3><ul><li><a href="projects.html">Projects</a></li><li><a href="approach.html">How we work</a></li><li><a href="about.html">About</a></li><li><a href="contact.html">Contact</a></li><li><a href="contact.html#subs">Subcontractors</a></li></ul></div>
    <div><h3>Reach us</h3><ul><li><a href="mailto:{MAIL}">{MAIL}</a></li><li>P.O. Box 4<br>Youngsville, LA 70592</li><li>Monday to Friday, 7 to 5</li></ul></div>
  </div>
  <div class="wrap"><div class="bottom"><span>&copy; <span data-year>2026</span> Ocmand Construction Company, L.L.C.</span><span>Louisiana Contractor License No. 37723</span></div></div>
</footer>
<script src="site.js" defer></script>
</body></html>'''
def page(fname,title,desc,body,cur=None,schema=''):
    slug='' if fname=='index.html' else fname[:-5]
    canon=f'{SITE}/{slug}'
    out=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Ocmand Construction Co., LLC">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}/og.jpg">
<meta name="theme-color" content="#0c2148">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">
<script>document.documentElement.classList.add('js')</script>
{GA}
{schema}
</head>
<body>
{header(cur or fname)}
<main id="main">
{body}
</main>
{FOOT}'''
    if PREVIEW:
        out=out.replace(GA,'')
        if fname=='index.html':
            out=out.replace('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n','').replace('</head>\n<body>\n','').replace('</body></html>','')
            out='\n'.join(l for l in out.split('\n') if not l.startswith(('<link rel="canonical"','<meta property','<meta name="description"','<meta name="theme-color"','<link rel="icon"','<link rel="preload"')))
            out=out.replace(title,'Ocmand Construction Website')
    if not PREVIEW: out=absolutize(out)
    open(OUT+'/'+fname,'w').write(out); return fname
import re
def absolutize(h):
    """Production only: root-relative, extensionless URLs so no page click needs a redirect and the 404 page works at any depth."""
    def fix(u):
        if not u or u.startswith(('http:','https:','mailto:','#','/','data:')): return u
        if u=='./': return '/'
        u=re.sub(r'^index\.html','',u)
        u=re.sub(r'^([a-z0-9-]+)\.html',r'\1',u)
        return '/'+u
    h=re.sub(r'\b(href|src|data-full)="([^"]*)"',lambda m:f'{m.group(1)}="{fix(m.group(2))}"',h)
    h=re.sub(r'\bsrcset="([^"]*)"',lambda m:'srcset="'+', '.join(' '.join([fix(p.split()[0])]+p.split()[1:]) for p in m.group(1).split(',') if p.strip())+'"',h)
    return h
def head(crumbs,h1,lede,n=None):
    c=' / '.join([f'<a href="{u}">{t}</a>' for u,t in crumbs[:-1]]+[crumbs[-1][1]])
    bg=f'<div class="ph-bg">{img(n,"","100vw",lazy=False)}</div>' if n else '<svg class="ghost-mark" viewBox="0 0 248.9 284" aria-hidden="true"><use href="logo.svg#mark"/></svg>'
    return f'''<section class="page-head{" has-photo" if n else ""}">{bg}
<div class="wrap"><p class="crumb">{c}</p><h1 class="h-xl">{h1}</h1><p class="lede">{lede}</p></div></section>'''
def cta(h='Let us build your next project.',p='Send us your drawings or tell us about your plans. We respond to every inquiry within one business day.'):
    return f'''<section class="cta"><div class="cta-bg">{img(1,"","100vw")}</div><div class="wrap"><div><h2 class="h-lg">{h}</h2><p class="lede">{p}</p></div>
<div class="btn-row"><a class="btn light" href="contact.html#bid">Request a bid</a><a class="btn outline-light" href="mailto:{MAIL}">{MAIL}</a></div></div></section>'''
def scope(items): return '<ul class="scope">'+''.join(f'<li>{i}</li>' for i in items)+'</ul>'
def cols3(items): return '<div class="cols3">'+''.join(f'<div data-reveal style="--d:{i*.08:.2f}s"><h3 class="h-sm">{h}</h3><p>{p}</p></div>' for i,(h,p) in enumerate(items))+'</div>'

# ============ HOME ============
schema='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"GeneralContractor","name":"Ocmand Construction Co., LLC","legalName":"Ocmand Construction Company, L.L.C.","url":SITE+"/","logo":SITE+"/apple-touch-icon.png","image":SITE+"/og.jpg","email":MAIL,"address":{"@type":"PostalAddress","postOfficeBoxNumber":"4","addressLocality":"Youngsville","addressRegion":"LA","postalCode":"70592","addressCountry":"US"},"areaServed":"Louisiana","openingHours":"Mo-Fr 07:00-17:00","description":"Family-owned commercial general contractor in Louisiana. New construction, renovations and public works."})+'</script>'
CAPS=[('Preconstruction','Estimating, budgeting, value engineering and scheduling that give owners a clear picture of cost and time before construction begins.'),
      ('General contracting','Complete responsibility for the project under a single contract, from site work through final completion.'),
      ('Project management','Close coordination of subcontractors, schedules and documentation to keep every project organized and on track.')]
PILLARS_HOME=[('Quality','We hold every project to a high standard and review the work at each stage to make sure it is done right.'),
      ('Schedule','We plan ahead, coordinate the trades and manage the schedule closely so projects finish on time.'),
      ('Safety','A safe job site protects everyone. Safety is a priority on every project we build.'),
      ('Communication','Owners and architects are kept informed from the first meeting through final completion.')]
def pillars(items): return cols3(items).replace('class="cols3"','class="cols3 four"')
def feature():
    return f'''<section class="feature">
<figure class="render" data-reveal><picture><source media="(max-width:700px)" srcset="bangkok-thai-rendering-m.jpg"><img src="bangkok-thai-rendering.jpg" srcset="bangkok-thai-rendering-1200.jpg 1200w, bangkok-thai-rendering.jpg 2400w" sizes="100vw" width="2400" height="571" alt="Architectural rendering of the Bangkok Thai restaurant and retail center" loading="lazy" decoding="async"></picture><figcaption>Rendering: Boudreaux Hoffpauir &amp; Associates</figcaption></figure>
<div class="sec navy on-navy"><div class="wrap split top">
  <div class="stack" data-reveal><p class="kicker">Featured project</p><h2 class="h-lg">Bangkok Thai and retail center</h2>
  <p class="lede">A new restaurant and retail center in Lafayette, anchored by Bangkok Thai. Ocmand Construction is the general contractor for the project, from site work through the finished restaurant.</p>
  <p><a class="link" href="{DL}" target="_blank" rel="noopener">Read the coverage on Developing Lafayette</a></p></div>
  <dl class="facts on-dark" data-reveal style="--d:.1s"><div><dt>Location</dt><dd>101 Gerald Drive, Lafayette, Louisiana</dd></div><div><dt>Size</dt><dd>9,660 square feet</dd></div><div><dt>Type</dt><dd>New restaurant and retail center</dd></div><div><dt>Architect</dt><dd>Boudreaux Hoffpauir &amp; Associates</dd></div><div><dt>Contractor</dt><dd>Ocmand Construction Co., LLC</dd></div></dl>
</div></div></section>'''
home=f'''<section class="hero">
  <div class="hero-bg">{img(11,"","100vw",lazy=False)}</div>
  <div class="wrap">
    <div class="hero-copy">
      <span class="kicker">Commercial general contractor</span>
      <h1 class="h-xl">Built right, from the ground up.</h1>
      <p class="lede">Ocmand Construction is a family-owned general contractor building commercial projects for private owners, developers and public agencies.</p>
      <div class="btn-row"><a class="btn light" href="contact.html#bid">Request a bid</a><a class="btn outline-light" href="projects.html">View our projects</a></div>
    </div>
    {tb('Breaux Bridge Eye Care','Breaux Bridge, LA','Medical office').replace('class="tb"','class="tb hero-tb"')}
  </div>
</section>
<div class="creds"><div class="wrap"><dl>
  <div><dt>35+ years</dt><dd>of construction experience</dd></div>
  <div><dt>Family owned</dt><dd>and operated</dd></div>
  <div><dt>Public and private</dt><dd>commercial construction</dd></div>
  <div><dt>Licensed, bonded, insured</dt><dd>State of Louisiana</dd></div>
</dl></div></div>

<section class="sec"><div class="wrap">
  <div class="intro">
    <h2 class="h-lg" data-reveal>Committed to doing the job right.</h2>
    <div class="prose" data-reveal style="--d:.08s"><p>Ocmand Construction is a family-owned general contractor led by Shawn Ocmand, who brings more than 35 years of construction experience to every project. We work with owners, architects and public agencies to deliver commercial buildings that are built correctly, finished on schedule and made to last.</p><p>We take pride in our work and we stand behind it. Every project receives the same care and attention, whether it is a new building, a renovation or a public contract.</p><p><a class="link" href="about.html">About the company</a></p></div>
  </div>
  <div class="cols3 mt-l">{''.join(f'<div data-reveal style="--d:{i*.08:.2f}s"><h3 class="h-sm">{h}</h3><p>{p}</p></div>' for i,(h,p) in enumerate(CAPS))}</div>
</div></section>

<section class="sec concrete"><div class="wrap">
  <div class="sec-head"><h2 class="h-lg" data-reveal>Markets</h2><p class="lede" data-reveal>Commercial construction for a range of owners and building types.</p></div>
  {markets()}
</div></section>

{feature()}

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2 class="h-lg" data-reveal>Completed work</h2><p class="lede" data-reveal>A selection of commercial projects built by Ocmand Construction.</p></div>
  <div class="work">
    {shot(10,'wide','(max-width:900px) 100vw, 58vw',href='projects.html')}
    {shot(1,'narrow','(max-width:900px) 100vw, 42vw',href='projects.html',d=.1)}
    {shot(8,'',href='projects.html')}
    {shot(12,'',href='projects.html',d=.1)}
  </div>
  <p class="mt-l"><a class="btn ghost" href="projects.html">View all projects</a></p>
</div></section>

<section class="sec concrete"><div class="wrap">
  <div class="sec-head"><h2 class="h-lg" data-reveal>Our commitment</h2><p class="lede" data-reveal>We care about the work we put our name on. Every project is planned thoroughly, managed closely and checked at every stage.</p></div>
  {pillars(PILLARS_HOME)}
  <p class="mt-l"><a class="btn ghost" href="approach.html">How we work</a></p>
</div></section>
{cta()}'''
page('index.html','Ocmand Construction Co., LLC | Commercial General Contractor','Ocmand Construction is a family-owned commercial general contractor in Louisiana. New construction, renovations and public works for private owners and public agencies.',home,schema=schema)

# ============ SERVICES OVERVIEW ============
page('services.html','Markets | Ocmand Construction Co., LLC','Ocmand Construction builds commercial projects across a range of markets: new buildings, restaurant and retail, healthcare, public works, metal buildings, and concrete and site work.',
head([(HOME,'Home'),('','Markets')],'Markets','Ocmand Construction serves private owners, developers and public agencies across a range of commercial markets.',n=8)+f'''
<section class="sec"><div class="wrap">{markets()}</div></section>
<section class="sec concrete"><div class="wrap"><div class="sec-head"><h2 class="h-lg" data-reveal>Our services</h2><p class="lede" data-reveal>The same services and the same standard of care on every project.</p></div>{cols3(CAPS)}</div></section>{cta()}''')

# ============ SERVICE PAGES ============
def service(fname,name,title,desc,h1,lede,n,intro_h,intro,scope_h,items,how,related):
    rel=''.join(shot(r,'',sizes='(max-width:640px) 100vw, 33vw',href='projects.html',d=i*.08) for i,r in enumerate(related))
    body=head([(HOME,'Home'),('services.html','Markets'),('',name)],h1,lede,n=n)+f'''
<section class="sec"><div class="wrap intro">
  <h2 class="h-lg" data-reveal>{intro_h}</h2><div class="prose" data-reveal style="--d:.08s">{intro}</div>
</div></section>
<section class="sec concrete"><div class="wrap">
  <div class="sec-head single"><h2 class="h-lg" data-reveal>{scope_h}</h2></div>
  <div data-reveal>{scope(items)}</div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head single"><h2 class="h-lg" data-reveal>Our approach</h2></div>
  {cols3(how)}
</div></section>
<section class="sec concrete"><div class="wrap">
  <div class="sec-head"><h2 class="h-lg" data-reveal>Related projects</h2><p class="lede" data-reveal><a class="link" href="projects.html">View all projects</a></p></div>
  <div class="work thirds">{rel}</div>
</div></section>{cta()}'''
    page(fname,title,desc,body,cur='services.html')

service('commercial-construction.html','Ground-up commercial','Ground-Up Commercial Construction | Ocmand Construction','New commercial construction in Louisiana. Office, medical, retail and multi-tenant buildings, delivered complete by Ocmand Construction.',
 'Ground-up commercial construction','New commercial buildings, delivered complete from site work through final completion.',11,
 'New construction, start to finish.',
 "<p>Ocmand Construction builds new commercial facilities for owners and developers, including office, medical, retail and multi-tenant buildings. We manage every phase of the work under a single contract, from site preparation through the certificate of occupancy.</p><p>Our team works closely with the owner and the design team throughout the project to protect the budget, maintain the schedule and deliver a building that meets the drawings and the owner's expectations.</p>",
 'Project types',
 ['Office buildings','Medical and dental offices','Retail centers','Restaurants','Multi-tenant shell buildings','Pre-engineered metal buildings','Site development and parking','Interior build-outs'],
 [('Planning','Careful planning before construction begins, so the budget and the schedule are established early.'),
  ('Quality','The work is reviewed at every stage to confirm it meets the plans, the specifications and our own standards.'),
  ('Communication','Owners and architects are kept informed throughout the project, with one point of contact from start to finish.')],
 [11,8,10])

service('restaurant-retail.html','Restaurant and retail','Restaurant and Retail Construction | Ocmand Construction','Restaurant and retail construction in Louisiana. New buildings, lease space and tenant build-outs by Ocmand Construction.',
 'Restaurant and retail construction','New restaurants, retail centers and tenant build-outs, completed on schedule for opening day.',10,
 'Ready for opening day.',
 '<p>Ocmand Construction builds restaurants, retail centers and tenant spaces for owners, developers and tenants. Our work includes new buildings, shell space for lease and complete interior build-outs.</p><p>We understand that an opening date matters. Our team coordinates the design team, subcontractors, suppliers and inspectors to keep the project moving and finish on time.</p>',
 'Project types',
 ['Restaurants and commercial kitchens','Retail centers','Multi-tenant lease space','Tenant build-outs and improvements','Storefronts and exterior renovations','Renovations and additions'],
 [('Schedule','The schedule is built around your opening date and managed closely through completion.'),
  ('Coordination','Equipment, utilities and finishes are coordinated with every trade so the work comes together correctly.'),
  ('Quality','Every space is reviewed in detail before it is turned over to the owner.')],
 [10,8,1])

service('healthcare-occupied.html','Healthcare and occupied facilities','Healthcare and Occupied Facility Renovation | Ocmand Construction','Renovations in hospitals, clinics and businesses that remain open during construction, by Ocmand Construction.',
 'Healthcare and occupied facilities','Renovations in hospitals, clinics and businesses that remain open during construction.',8,
 'Construction in active facilities.',
 '<p>Renovating a facility that remains in operation requires careful planning. Ocmand Construction works with administrators and facility staff to plan the work, protect patients, staff and the public, and keep daily operations running.</p><p>We respect the environment we are working in. Our crews and subcontractors follow the requirements of the facility, keep work areas clean and contained, and schedule disruptive work around the people who use the building.</p>',
 'Project types',
 ['Hospital and clinic renovations','Medical office build-outs','Imaging and treatment rooms','Occupied office renovations','Phased renovations','Additions to existing facilities'],
 [('Planning','Phasing, access and utility shutdowns are planned with the facility before work begins.'),
  ('Safety and cleanliness','Work areas are separated from occupied areas and kept clean, safe and secure.'),
  ('Coordination','We work around the schedule of the facility and keep its staff informed at every step.')],
 [8,11,1])

service('public-works.html','Public works','Public Works Contractor in Louisiana | Ocmand Construction','Public works general contractor for parish, municipal and state agencies in Louisiana. Licensed, bonded and insured.',
 'Public works','Construction for parish, municipal and state agencies.',12,
 'Building for public owners.',
 '<p>Ocmand Construction bids and builds public projects for parish, municipal and state agencies in Louisiana. We are licensed, bonded and insured, and we are familiar with the requirements of public contracts.</p><p>Public owners expect accountability. We follow the contract documents closely, maintain complete project records and deliver the work as specified.</p>',
 'Project types',
 ['Public buildings and renovations','Healthcare facilities','Parks and recreation facilities','Memorials and site improvements','Concrete and site work','Additions to existing facilities'],
 [('Compliance','The work is performed in accordance with the contract documents and Louisiana public bid law.'),
  ('Documentation','Submittals, pay applications and closeout documents are prepared thoroughly and on time.'),
  ('Accountability','One team is responsible for the project from the bid through final completion.')],
 [12,1,9])

service('metal-buildings.html','Pre-engineered metal buildings','Pre-Engineered Metal Buildings | Ocmand Construction','Pre-engineered metal buildings for commercial use in Louisiana, delivered complete from foundation to finish by Ocmand Construction.',
 'Pre-engineered metal buildings','Metal building systems for commercial use, delivered complete from foundation to finish.',11,
 'Complete metal building projects.',
 '<p>Pre-engineered metal buildings are an efficient and economical way to build commercial space. Ocmand Construction provides the complete project, including the foundation, the building, and the interior and exterior finishes.</p><p>We work with established building manufacturers and experienced erectors, and we coordinate the building with every other part of the project so the work fits together as designed.</p>',
 'Project types',
 ['Retail and restaurant buildings','Office and warehouse buildings','Shop and service buildings','Storage and equipment buildings','Building additions','Interior build-outs'],
 [('Coordination','The building system is coordinated with the foundation, the structure and the finishes before fabrication.'),
  ('Quality','Materials and installation are checked throughout construction to make sure the building is erected properly.'),
  ('Value','Competitive pricing from building manufacturers gives owners strong value for their budget.')],
 [11,8,12])

service('concrete-sitework.html','Concrete and site work','Commercial Concrete and Site Work | Ocmand Construction','Commercial concrete and site work in Louisiana. Foundations, slabs, paving, drainage and site utilities by Ocmand Construction.',
 'Concrete and site work','Foundations, slabs, paving, drainage and site utilities for commercial projects.',12,
 'The groundwork for every project.',
 '<p>Every building depends on the work beneath it. Ocmand Construction provides concrete and site work for our own building projects and as stand-alone contracts.</p><p>We pay close attention to layout, grades and placement, and we verify the work before it is covered, so it performs for the life of the building.</p>',
 'Scope of work',
 ['Building foundations','Slabs on grade','Parking lots and paving','Sidewalks, curbs and ramps','Storm drainage','Site utilities','Grading and earthwork','Erosion control'],
 [('Accuracy','Layout and elevations are checked before any concrete is placed.'),
  ('Quality','Materials and workmanship are inspected and tested to meet the requirements of the project.'),
  ('Scheduling','Site work is sequenced so the rest of the project can proceed without delay.')],
 [12,11,8])

# ============ APPROACH ============
def phase(n,h,p,items):
    return f'<div class="phase" data-reveal><p class="phase-n" aria-hidden="true">{n:02d}</p><div><h2 class="h-lg">{h}</h2><p class="lede mt-s">{p}</p></div>{scope(items)}</div>'
PILLARS=[('Quality','The work is reviewed at every stage against the plans, the specifications and our own standards.'),
      ('Schedule','The schedule is planned in detail, updated regularly and managed through the last day of the project.'),
      ('Safety','We maintain a safe, clean and orderly job site for our crews, our subcontractors and the public.'),
      ('Communication','Owners and architects receive regular updates and prompt answers throughout the project.')]
page('approach.html','How We Work | Ocmand Construction Co., LLC','How Ocmand Construction manages a commercial project: preconstruction, project management, construction and closeout, handled thoroughly from start to finish.',
head([(HOME,'Home'),('','How we work')],'How we work','An organized, thorough approach to every project, from preconstruction through closeout.',n=10)+f'''
<section class="sec"><div class="wrap intro">
  <h2 class="h-lg" data-reveal>Managed carefully from start to finish.</h2>
  <div class="prose" data-reveal style="--d:.08s"><p>A successful project depends on how well the details are managed. Ocmand Construction plans each project carefully, manages it closely and stays involved until the work is complete.</p><p>The services below are part of every project we build. Each one is handled thoroughly, so nothing is overlooked, the work is done correctly and the schedule is met.</p></div>
</div></section>
<section class="sec concrete tight"><div class="wrap phases">
{phase(1,'Preconstruction','We establish the scope, the budget and the schedule before construction begins, so the project starts with a clear plan.',['Estimating and budgeting','Value engineering','Project scheduling','Plan and specification review','Subcontractor bidding','Permitting'])}
{phase(2,'Project management','We keep the documentation, the materials and the trades organized and ahead of the work.',['Submittals','Requests for information','Material procurement','Subcontracts and insurance','Schedule updates','Change orders','Pay applications','Progress meetings and reporting'])}
{phase(3,'Construction','Our superintendent directs the work on site every day and holds every trade to the plans, the specifications and the schedule.',['On-site supervision','Subcontractor coordination','Quality control','Job site safety','Inspections and testing','Daily reports'])}
{phase(4,'Closeout','We finish the details, complete the final inspections and turn the building over with the documents the owner needs to operate it.',['Punch list completion','Final inspections','Operation and maintenance manuals','Warranties','Record documents','Owner training'])}
</div></section>
<section class="sec navy on-navy"><div class="wrap">
  <div class="sec-head"><h2 class="h-lg" data-reveal>Thorough on every project.</h2><p class="lede" data-reveal>We give each of these steps our full attention and follow it through to completion. That is how we make sure nothing is missed, the work is done right and the schedule is met.</p></div>
  {pillars(PILLARS)}
</div></section>{cta()}''')

# ============ PROJECTS ============
cards=''
for n,name,loc,typ,cat,alt in P:
    cards+=f'<button type="button" class="shot" data-cat="{cat}" data-full="project-{n:02d}.jpg" data-name="{name}" data-loc="{loc}" data-type="{typ}" aria-label="View {name} full screen" data-reveal><div class="frame">{img(n,alt,"(max-width:900px) 100vw, 50vw")}</div>{tb(name,loc,typ)}</button>'
page('projects.html','Projects | Ocmand Construction Co., LLC','Commercial projects by Ocmand Construction: restaurants, medical and office buildings, restorations and public facilities.',
head([(HOME,'Home'),('','Projects')],'Projects','A selection of our commercial projects.',n=10)+f'''
{feature()}
<section class="sec"><div class="wrap">
<div class="sec-head"><h2 class="h-lg" data-reveal>Completed work</h2><p class="lede" data-reveal>Select a photo to view it full screen.</p></div>
<div class="work" data-projects>{cards}</div>
</div></section>
<section class="sec concrete"><div class="wrap">
  <div class="sec-head"><h2 class="h-lg" data-reveal>Additional projects</h2><p class="lede" data-reveal>Other work for public and private owners.</p></div>
  <table class="ledger" data-reveal>
    <thead><tr><th scope="col">Project</th><th scope="col">Location</th><th scope="col">Type</th><th scope="col">Owner</th></tr></thead>
    <tbody>
      <tr><td>Nuclear Medicine Replacement</td><td data-l="Location">Iberia Medical Center North Campus<br>600 North Lewis Street, New Iberia</td><td data-l="Type">Hospital renovation</td><td class="status" data-l="Owner">Iberia Medical Center</td></tr>
      <tr><td>Lydia Veterans Memorial</td><td data-l="Location">Lydia</td><td data-l="Type">Site work and concrete</td><td class="status" data-l="Owner">Iberia Parish Government</td></tr>
    </tbody>
  </table>
</div></section>
<dialog class="lb" aria-label="Project photo"><div class="lb-inner">
<div class="lb-bar"><span data-count></span><button type="button" data-close aria-label="Close">&times;</button></div>
<div class="lb-stage"><img src="" alt=""></div>
<div class="lb-foot"><dl class="tb"><div><dt>Project</dt><dd data-name></dd></div><div><dt>Location</dt><dd data-loc></dd></div><div><dt>Type</dt><dd data-type></dd></div></dl>
<div class="lb-nav"><button type="button" data-prev aria-label="Previous photo">&#8249;</button><button type="button" data-next aria-label="Next photo">&#8250;</button></div></div>
</div></dialog>{cta()}''')

# ============ ABOUT ============
VALUES=[('Quality','We take pride in our work and hold every project to a high standard.'),
        ('Integrity','We are honest and fair with owners, architects, subcontractors and suppliers.'),
        ('Reliability','We do what we say we will do, and we see every project through to the end.')]
page('about.html','About | Ocmand Construction Co., LLC','Ocmand Construction is a family-owned commercial general contractor in Louisiana with more than 35 years of construction experience.',
head([(HOME,'Home'),('','About')],'About the company','A family-owned general contractor with more than 35 years of construction experience.',n=1)+f'''
<section class="sec"><div class="wrap intro">
  <h2 class="h-lg" data-reveal>Family owned. Built on experience.</h2>
  <div class="prose" data-reveal style="--d:.08s"><p>Ocmand Construction Co., LLC is a family-owned commercial general contractor based in Louisiana, built on more than 35 years of construction experience. Our work includes restaurants, offices, medical buildings and public projects.</p><p>We serve private owners, developers and public agencies, and we approach every project the same way. We plan it carefully, build it correctly and stand behind the work.</p><p>Our reputation is built on dependable work and lasting relationships with the owners, architects and subcontractors we work with.</p></div>
</div></section>
<section class="sec navy on-navy"><div class="wrap intro">
  <h2 class="h-lg" data-reveal>Our name is on every project.</h2>
  <div class="prose" data-reveal style="--d:.08s"><p>Ocmand Construction is owned and operated by the Ocmand family. The family that owns the company is involved in every project, from the first estimate to the final walk-through.</p><p>For our clients, that means working directly with the people responsible for the outcome. Decisions are made quickly, questions are answered by someone who knows the project, and the commitments we make are kept.</p><p>It is also why we care about our work the way we do. Every project carries our family name, so we build each one as if it were our own. We measure our success by the owners who call us back for the next one.</p></div>
</div></section>
<section class="sec concrete"><div class="wrap">
  <div class="sec-head single"><h2 class="h-lg" data-reveal>Our values</h2></div>
  {cols3(VALUES)}
</div></section>
<section class="sec"><div class="wrap intro">
  <h2 class="h-lg" data-reveal>Qualifications</h2>
  <dl class="facts" data-reveal style="--d:.08s"><div><dt>Licensing</dt><dd>Louisiana commercial contractor, Building Construction</dd></div><div><dt>Bonding</dt><dd>Bid, performance and payment bonds</dd></div><div><dt>Insurance</dt><dd>Fully insured. Certificates available on request</dd></div><div><dt>Services</dt><dd>Preconstruction, general contracting and project management</dd></div><div><dt>Clients</dt><dd>Private owners, developers and public agencies</dd></div></dl>
</div></section>{cta()}''')

# ============ CONTACT ============
page('contact.html','Contact and Bid Requests | Ocmand Construction Co., LLC','Request a bid from Ocmand Construction for a commercial project. Email jobs@ocmandconstruction.com.',
head([(HOME,'Home'),('','Contact')],'Request a bid','Tell us about your project. We respond to every inquiry within one business day.',n=11)+f'''
<section class="sec" id="bid"><div class="wrap contact-grid">
  <form class="form" data-bid novalidate>
    <div><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
    <div><label for="f-company">Company <span class="opt">(optional)</span></label><input id="f-company" name="company" autocomplete="organization"></div>
    <div><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
    <div><label for="f-type">Project type</label><select id="f-type" name="type"><option>Ground-up commercial</option><option>Restaurant or retail</option><option>Healthcare or occupied renovation</option><option>Public works</option><option>Metal building</option><option>Concrete or site work</option><option>Other</option></select></div>
    <div><label for="f-location">Project location</label><input id="f-location" name="location" placeholder="City or address"></div>
    <div><label for="f-timeline">Desired completion</label><input id="f-timeline" name="timeline" placeholder="Month and year"></div>
    <div class="full"><label for="f-drawings">Do you have drawings?</label><select id="f-drawings" name="drawings"><option>Yes, permit or bid set</option><option>Yes, preliminary</option><option>Not yet</option></select></div>
    <div class="full"><label for="f-details">Project details</label><textarea id="f-details" name="details" placeholder="Building size, scope of work, architect"></textarea></div>
    <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="full btn-row"><button class="btn" type="submit">Send bid request</button><p class="form-status" role="status" aria-live="polite"></p></div>
    <p class="note full">Drawings may be sent by email or download link to <a href="mailto:{MAIL}">{MAIL}</a>.</p>
  </form>
  <aside>
    <div class="aside-block"><h2 class="h-sm">Email</h2><a class="big-mail" href="mailto:{MAIL}">{MAIL}</a><p class="note mt-s">Monday to Friday, 7 a.m. to 5 p.m.</p></div>
    <div class="aside-block"><h2 class="h-sm">Mailing address</h2><p>Ocmand Construction Company, L.L.C.<br>P.O. Box 4<br>Youngsville, LA 70592</p></div>
    <div class="aside-block"><h2 class="h-sm">Architects and owners</h2><p class="note" style="font-size:16px">We welcome invitations to bid. Please send bid documents and plan room links to the email above.</p></div>
    </aside>
</div></section>
<section class="sec concrete" id="subs"><div class="wrap contact-grid">
  <form class="form" data-bid data-kind="Subcontractor sign-up" novalidate>
    <div><label for="s-name">Your name</label><input id="s-name" name="name" autocomplete="name" required></div>
    <div><label for="s-company">Company</label><input id="s-company" name="company" autocomplete="organization"></div>
    <div><label for="s-email">Email</label><input id="s-email" name="email" type="email" autocomplete="email" required></div>
    <div><label for="s-type">Trade</label><input id="s-type" name="type" placeholder="Electrical, concrete, roofing"></div>
    <div><label for="s-location">Area you cover</label><input id="s-location" name="location" placeholder="Parishes or cities"></div>
    <div><label for="s-timeline">Louisiana license number <span class="opt">(if required)</span></label><input id="s-timeline" name="timeline"></div>
    <input type="hidden" name="drawings" value=""><input type="hidden" name="details" value="">
    <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="full btn-row"><button class="btn" type="submit">Join our bid list</button><p class="form-status" role="status" aria-live="polite"></p></div>
  </form>
  <aside><h2 class="h-lg">Subcontractors and suppliers</h2><p class="lede mt-s">Ocmand Construction values its relationships with qualified subcontractors and suppliers. Submit your information to be considered for upcoming projects.</p></aside>
</div></section>''')

# ============ 404 ============
page('404.html','Page Not Found | Ocmand Construction Co., LLC','This page does not exist.',
f'''<section class="sec"><div class="wrap center-404"><h1 class="h-xl">Page not found.</h1><p class="lede mt-s">The page you are looking for may have moved.</p><div class="btn-row mt-m"><a class="btn" href="{HOME}">Go to the home page</a><a class="link" href="projects.html">See our projects</a></div></div></section>''')

pages=['','services','commercial-construction','restaurant-retail','healthcare-occupied','public-works','metal-buildings','concrete-sitework','projects','approach','about','contact']
open(OUT+'/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{SITE}/{p}</loc><lastmod>{LASTMOD}</lastmod></url>\n' for p in pages)+'</urlset>\n')
open(OUT+'/robots.txt','w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
open(OUT+'/_redirects','w').write('/custom-homes /services 301\n/outdoor-living /services 301\n/renovations-additions /services 301\n/storm-restoration /services 301\n/residential /services 301\n/reviews /about 301\n/api/* / 302\n/_source/* / 302\n/CLAUDE.md / 302\n')
print('built',len(pages),'pages')
