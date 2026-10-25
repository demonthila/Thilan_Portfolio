#!/usr/bin/env python3
"""Builds the portfolio into this folder. Edit the content here, then run: python3 build.py"""
import os, html

OUT = os.path.dirname(os.path.abspath(__file__))
IMG = "assets/img/"
EMAIL = "sanjulathilan12321@gmail.com"
PHONE = "+61 450 679 814"
CAL = "https://cal.com/sanjula-thilan-0zg8h3/quick-chat"
LINKEDIN = "https://www.linkedin.com/in/sanjula-thilan-17b77b243"
# Replace with a direct link to your CV PDF (e.g. assets/sanjula-thilan-cv.pdf) once uploaded
RESUME = "https://drive.google.com/drive/folders/1NQNNcfjlyc8VsQzhDZt6k7sk8ydUlZBM"
SITE = "https://thilan.novalinkinnovations.com/"

e = html.escape

def head(title, desc, r, path="", og="home.jpg", noindex=False):
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="author" content="Sanjula Thilan">
<meta name="theme-color" content="#f4f1eb">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_AU">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}assets/img/og/{og}">
<meta name="twitter:card" content="summary_large_image">
{robots}<link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="{r}assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def nav(r, current):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f"""<header class="nav">
  <div class="wrap">
    <a class="logo" href="{r}index.html" aria-label="Sanjula Thilan, home">s<span class="logo-t">t</span><span class="logo-dot">.</span></a>
    <nav class="nav-links" aria-label="Main">
      {a(r+'index.html#work','Work','work')}
      {a(r+'play.html','Play','play')}
      {a(r+'about.html','About','about')}
      {a(r+'contact.html','Contact','contact')}
    </nav>
    <div class="nav-cta">
      <a class="btn btn-ghost" href="{RESUME}" target="_blank" rel="noopener">Resume <i class="ar ar-d" aria-hidden="true">↓</i></a>
      <a class="btn btn-dark" href="{r}contact.html">Say hello <i class="ar ar-ne" aria-hidden="true">↗</i></a>
      <button class="menu-btn" type="button" aria-expanded="false">Menu</button>
    </div>
  </div>
</header>
"""

def closing(r):
    return f"""<footer class="closing">
  <div class="wrap">
    <span class="eyebrow reveal">A good conversation is a good start.</span>
    <p class="muted reveal">A product that needs untangling, a team that needs a designer who can also build, or a quick chat about Melbourne's design scene? I'm listening.</p>
    <a class="big-link reveal" href="mailto:{EMAIL}"><span>Let's talk about</span><span>what comes next.</span><small>{EMAIL}</small></a>
    <div class="copy-row reveal">
      <a class="btn btn-dark" href="{r}contact.html">Send a project brief</a>
      <button class="btn btn-ghost" type="button" data-copy="{EMAIL}">Copy email</button>
      <a class="btn btn-ghost" href="{CAL}" target="_blank" rel="noopener">Book a 15-minute call</a>
      <a class="btn btn-ghost" href="tel:{PHONE.replace(' ','')}">{PHONE}</a>
    </div>
    <div class="foot">
      <span>Sanjula Thilan © 2026 · Melbourne, <span data-clock></span> local time</span>
      <nav aria-label="Footer">
        <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
        <a href="{RESUME}" target="_blank" rel="noopener">Download resume</a>
        <a href="{r}contact.html">Contact</a>
        <a href="https://novalinkinnovations.com" target="_blank" rel="noopener">NovaLink Innovations</a>
      </nav>
    </div>
  </div>
</footer>
<a class="to-top" href="#top" aria-label="Back to top"><i class="ar ar-n" aria-hidden="true">↑</i></a>
<script src="{r}assets/js/site.js"></script>
</body>
</html>
"""

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

# ---------------------------------------------------------------- Case study data
# Where you see "metric", replace with a measured result as soon as you have one.
CASES = [
 dict(
  slug="dela", og="dela.jpg", brand="Dela", year="2025", region="Australia",
  role_short="UI/UX Designer & UX Business Analyst",
  card_title="Taking the fear out of buying from strangers.",
  card_text="I designed a buyer–seller platform where every step of a deal is visible, protected and confirmed.",
  metric=("Request → delivery", "One tracked flow for both sides", "Held payments built in"),
  cover="dela-1.webp",
  title="Dela.", promise="From a stranger's offer to a deal both sides trust. Designing safe transactions for an Australian marketplace.",
  role_line=("UI/UX Designer & UX Business Analyst", "User flows, interaction design, requirements"),
  problem="Online deals between strangers fall apart through scams, ghosting and unclear next steps. Neither side trusts the other.",
  solution="A confidence-first flow. Sellers send a request, buyers confirm it, the platform holds payment, and delivery is tracked in the app.",
  impact_big="Request → delivery", impact="Every step of the deal tracked in one place, for buyer and seller.",
  myrole="I designed the complete UI/UX, from requirements to final screens, as part of the DelaExchange team at Digiratina Technologies.",
  central="Design for trust first. Payment holding, delivery tracking and request confirmation came before every secondary feature.",
  scope="Buyer and seller journeys across a web dashboard and mobile: sign-in, deal requests, payment status and order tracking.",
  previews=[("dela-3.webp","Evidence of progress","Make the deal state impossible to miss","Every transaction shows where it stands and who is waiting on whom.","decisions"),
            ("dela-5.webp","Buyer control","Give the buyer the final yes","Sellers start the request. Nothing moves until the buyer accepts.","decisions")],
  mandate_h="Two strangers. One deal. No reason to trust each other.",
  mandate=["Peer-to-peer marketplaces run on uncertainty. Sellers worry a buyer will vanish after agreeing. Buyers worry the item will never arrive, or won't match the listing.",
           "Dela set out to make these deals safer and less stressful for Australian users. One product had to serve two people with opposite fears, inside the same transaction."],
  stakes="If either side felt unsure at any step, the deal would be abandoned, and the platform would lose both users.",
  mandate_list=["Building trust without face-to-face contact","Preventing ghosting partway through a deal","Making every step clear for buyer and seller"],
  turn_h="The obvious answer was another listings site. The useful answer was a protected deal.",
  turn=["I researched peer-to-peer marketplaces, escrow-style payment models and user complaints about scams and failed deals. The pattern was clear: people could already find things to buy. What broke was finishing the deal safely.",
        "So the product shifted from browse-and-message to a structured transaction. The seller initiates, the buyer confirms, and the platform holds payment until delivery is tracked."],
  tradeoff=("Trust takes a few extra steps","Confirmations add friction. I kept that friction only at the moments where it builds trust, and removed it everywhere else."),
  decision_quote="Make trust visible. Let the transaction carry the reassurance, not the copy.",
  decisions=[("Show the deal state","Every transaction carries a clear status: requested, confirmed, paid, shipped, delivered. Both sides always know what happens next."),
             ("Give buyers the final yes","Sellers start the request, but nothing moves until the buyer accepts or declines. Buyers stay in control without slowing sellers down."),
             ("Plain language over finance terms","“Your payment is held safely until delivery” replaced escrow jargon. Clear calls to action and status labels reduce decision fatigue.")],
  gallery=[("dela-2.webp","Seller dashboard","Transaction stats and sales at a glance"),
           ("dela-3.webp","Order tracking","Delivery status shown step by step"),
           ("dela-4.webp","Sign in","Security stated up front, before the first deal"),
           ("dela-5.webp","Purchase requests","Buyers accept or decline from mobile")],
  impact_h="A clearer, safer way to close a deal.",
  impact_text="The final design gave the DelaExchange development team a complete, developer-ready flow for both sides of the marketplace.",
  stats=[("2","Sides of every deal designed for"),("5","Clear deal states, request to delivery"),("Web + mobile","Seller dashboard and buyer app")],
  quote=("Sanjula Thilan was a valuable member of my Dela dev team. He delivered quality work, was pro-active in problem solving, open to feedback and easy to work with.","Megan van der Velde","Co-Founder, Dela Australia","t-megan.webp"),
  lesson="Trust is built through visible states, not promises. I now start transaction products by mapping what each person is afraid of at every step.",
 ),
 dict(
  slug="active-care", og="active-care.jpg", brand="Active Care", year="Nov 2025 to Mar 2026", region="United Kingdom",
  role_short="Associate UX Designer",
  card_title="Less screen time. More care time.",
  card_text="I designed one role-based system for residents, medication, incidents and shifts, for staff who decide under pressure.",
  metric=("4 roles", "One system across several care homes", "Role-based dashboards"),
  cover="activecare-1.webp",
  title="Active Care.", promise="One calm system for a high-pressure job. Designing care home software for nurses, carers and managers in the UK.",
  role_line=("Associate UX Designer", "UX business analysis, UI/UX, design system, developer collaboration"),
  problem="Care homes juggled resident records, medication, incidents and rosters across scattered tools, while staying compliant with UK regulations.",
  solution="A centralised, role-based system. Each role sees its priority tasks first, on accessible, high-contrast screens built from one design system.",
  impact_big="Fewer errors", impact="The client reported smoother daily operations and fewer errors in medication processes.",
  myrole="I ran requirements meetings with UK stakeholders, mapped user journeys, designed the UI in Figma, built the design system and supported developers so components shipped as designed.",
  central="Design around roles, not modules. A nurse, a carer and a manager open the same system and see different priorities.",
  scope="Multi-home management for administrators, nurses, carers and managers: residents, medication, compliance, incidents, scheduling and daily care notes.",
  previews=[("activecare-2.webp","Role-based views","Start every shift with the right list","Each role lands on its own priority tasks.","decisions"),
            ("activecare-3.webp","Daily logging","Fewer taps for repeat work","Checklists replace free-text forms for routine checks.","decisions")],
  mandate_h="Four roles. Sensitive data. No time to search for it.",
  mandate=["Active Care needed one place to run several care homes. Administrators, nurses, carers and managers all used it, each with different priorities.",
           "Care staff make time-sensitive decisions during busy shifts. They need resident details, medication schedules and incident forms in seconds, not after a hunt through menus."],
  stakes="In healthcare, a confusing screen can lead to a missed dose or an incomplete record. Clarity is a safety requirement.",
  mandate_list=["Several user roles with different priorities","Readability on the floor, often on shared devices","Documentation fatigue from repetitive daily logging","Large volumes of sensitive resident data"],
  turn_h="One dashboard for everyone would have been simpler to build. It would have served no one well.",
  turn=["Each role starts its shift with a different question. A carer asks what needs doing now. A manager asks whether anything is at risk. A single shared home screen answered neither.",
        "So the dashboards became role-driven, surfacing the right tasks first, while every module shared the same components underneath."],
  tradeoff=("More views to maintain","Role-based screens mean more to design and keep in sync. A modular design system made that manageable for the developers."),
  decision_quote="Design for the busiest moment of the shift, not the average one.",
  decisions=[("Role-driven dashboards","Each user lands on their own priority tasks, which cuts navigation during busy shifts."),
             ("Accessibility as the baseline","High-contrast type, large touch targets and clear status colours support readability in real care settings."),
             ("Structured logging","Checklists and structured forms for routine checks, such as kitchen items, reduce typing and documentation fatigue."),
             ("One modular design system","Reusable components kept every module consistent and made developer handover faster.")],
  gallery=[("activecare-2.webp","Staff list","Roles and status for every team member"),
           ("activecare-3.webp","Kitchen checklist","Routine checks in a few taps"),
           ("activecare-4.webp","Scheduled checks","Checklists paired with a calendar")],
  impact_h="A calmer system for a high-pressure job.",
  impact_text="The client reported improved daily operations, smoother care workflows and fewer errors in medication processes.",
  stats=[("4","User roles, each with its own priorities"),("1","Design system across every module"),("UK","Regulated healthcare setting")],
  quote=("Sanjula Thilan transformed our complex care home workflows into a clean, intuitive, and highly efficient system that has significantly improved our daily operations.","Al Patel","Director, Active Care Organization, UK",None),
  lesson="In regulated environments, clarity is part of safety. I design for the worst moment of a shift, then make sure the calm moments still feel simple.",
 ),
 dict(
  slug="iom-world", og="iom.jpg", brand="IOM World", year="2025", region="Singapore",
  role_short="UX Engineer",
  card_title="From paper requests to a tap and a face scan.",
  card_text="I designed a mobile workforce app for leave, overtime and attendance, with location-checked face recognition and automated approvals.",
  metric=("Face + location", "Attendance verified on mobile", "Automated approvals"),
  cover="iom-1.webp",
  title="IOM World.", promise="Leave, overtime and attendance in one secure app. Designing a workforce tool that non-technical staff actually use.",
  role_line=("UX Engineer", "UI/UX design, UX business analysis, front-end components"),
  problem="Leave, overtime and attendance were handled manually, which caused delays, inconsistent records and slow approvals.",
  solution="A mobile app where employees request leave or overtime in a few taps, sign in with location-checked face recognition, and managers approve from one list.",
  impact_big="Clear + secure", impact="The client reported better management of attendance, leave and overtime, with stronger security.",
  myrole="I designed the complete UI/UX, worked with the team to integrate AI-based location and face recognition, and built front-end components aligned with the selected theme.",
  central="Keep security invisible. Face and location checks run as one quick moment, so employees experience a simple sign-in.",
  scope="Employee and manager mobile flows: home summary, leave and overtime requests, approvals, attendance dashboard and notifications.",
  previews=[("iom-3.webp","Status at a glance","Answer “where is my request?” on the home screen","Balances and pending requests up front.","decisions"),
            ("iom-2.webp","Manager approvals","Approve or reject from one list","Requests stop waiting in inboxes.","decisions")],
  mandate_h="Every request touched three people and a spreadsheet.",
  mandate=["Employees filled in requests, managers approved them later, and HR reconciled attendance by hand. Data arrived slowly and often didn't match.",
           "The new system had to stay accurate, secure and compliant with company policy, while working for employees who are not technical."],
  stakes="If sign-in felt slow or invasive, staff would avoid it, and the data would be no better than before.",
  mandate_list=["Location-based face recognition for attendance","Several leave types, each with its own approval chain","Simple enough for non-technical users","Real-time validation and data privacy"],
  turn_h="Face recognition sounded like a barrier. Designed well, it became the fastest way in.",
  turn=["I researched enterprise HR systems, AI attendance tools and the pain points in the existing manual process. Security features tend to fail when they feel like extra work.",
        "So the check was designed as a single moment with clear feedback, instead of a multi-step security form."],
  tradeoff=("Security needs explanation","Biometric features need clear consent and clear error states. The happy path stays short; the recovery path stays obvious."),
  decision_quote="Security succeeds when people barely notice it.",
  decisions=[("Status at a glance","The home screen summarises leave balance and pending requests, so employees rarely need a menu."),
             ("Approvals in one list","Managers see each request with approve and reject side by side, cutting the time a request waits."),
             ("Notify at every change","Employees hear when a request is approved, rejected or needs action, which removes follow-up messages.")],
  gallery=[("iom-2.webp","Leave requests","Approve and reject actions side by side"),
           ("iom-3.webp","Home","Leave and overtime summary"),
           ("iom-4.webp","Attendance","Dashboard and face sign-in")],
  impact_h="Faster requests, cleaner data, stronger security.",
  impact_text="The client reported that the system greatly improved how they manage attendance, leave and overtime.",
  stats=[("3","Workflows in one app: leave, overtime, attendance"),("2","Roles designed for: employee and manager"),("Mobile","Built for staff on the move")],
  quote=("The UI is clear and easy to use, and the AI-based face recognition with geo-location adds a strong layer of security.","Jitendra","Operations Manager, IOM World","t-jit.webp"),
  lesson="Security features succeed when users barely notice them. I design the happy path first, then the clearest possible error states.",
 ),
 dict(
  slug="novalink", og="novalink.jpg", brand="NovaLink", year="2026", region="Internal SaaS",
  role_short="Lead UX Engineer",
  card_title="Designed it, built it, used it every day.",
  card_text="I designed and built an internal project management app in React, with AI-assisted planning and real-time email alerts.",
  metric=("Hours saved", "In manual planning, reported by the team", "React 18 + AI"),
  cover="novalink-3.webp",
  title="NovaLink.", promise="A focused project tool for a small team. From Figma to React, with AI doing the planning work nobody enjoys.",
  role_line=("Lead UX Engineer", "UI/UX design, front-end development, AI integration"),
  problem="The team tracked projects across scattered tools. Updates were missed and planning took hours of manual work.",
  solution="A single-page app with dashboards, task tracking, AI-suggested priorities and schedules, and automatic email alerts for assignments and deadlines.",
  impact_big="Hours saved", impact="The team reported that the AI integration saved hours of manual planning.",
  myrole="I owned it end to end: workflow mapping, UI/UX, the component system, the front-end build in React 18, TypeScript, Vite and Tailwind CSS, and the AI planning integration.",
  central="Prioritise the handful of actions people repeat every day, and keep everything else one click away.",
  scope="Ongoing projects, project settings, team management, task creation, dashboards, AI planning and email notifications.",
  previews=[("novalink-1.webp","Daily focus","Dashboards answer “what needs me now?”","Priority tasks and deadlines first.","decisions"),
            ("novalink-2.webp","Built in code","Components designed with their states","One library from Figma to React.","decisions")],
  mandate_h="A small team running many projects, and nobody sure what changed today.",
  mandate=["NovaLink needed one system to manage internal projects and keep every team member informed in real time. It also had to help plan ahead, not only record what had happened."],
  stakes="Project tools fail when they feel heavier than the work. If updating the system took longer than sending a message, the team would stop using it.",
  mandate_list=["A fast, responsive single-page app","AI-based task prioritisation and scheduling","Automatic email alerts for updates and deadlines","Dashboards showing progress at a glance","Consistency across many modules"],
  turn_h="The temptation was to copy a full-featured tool. The useful answer was a focused one.",
  turn=["I mapped our own workflows against modern project management tools. Most of what big tools offer was never used by a small team.",
        "So the core stayed small: create a task, track a project, act on a notification. AI took on the planning work people disliked doing."],
  tradeoff=("Suggestions, not decisions","AI suggestions can feel like the system is deciding for you. They stay as suggestions the team can edit."),
  decision_quote="Make the frequent things fast, and let AI carry the tedious ones.",
  decisions=[("Dashboards answer “what needs me now?”","High-priority tasks, timelines and upcoming deadlines appear first."),
             ("Email where people already are","Assignment, deadline and update emails remove the need to keep checking the app."),
             ("A modular component library","Shared React components kept every module consistent and made new features faster to ship.")],
  gallery=[("novalink-1.webp","Ongoing projects","Progress across every project"),
           ("novalink-2.webp","Project settings","Team members and permissions"),
           ("novalink-3.webp","Workspace","The app the team uses daily")],
  impact_h="Less time planning. More time delivering.",
  impact_text="The internal product manager reported that the AI integration had already saved the team hours of manual planning.",
  stats=[("React 18","TypeScript, Vite and Tailwind CSS"),("AI","Assisted planning and scheduling"),("1 person","Design and front-end, end to end")],
  quote=("They took the time to understand our complex project management requirements and translated them into a highly efficient and visually stunning system. The AI integration has already saved our team hours of manual planning.","Internal Product Manager","NovaLink Innovations",None),
  lesson="Building my own design in React showed me which details matter in code. I now design components with their states and edge cases already defined.",
 ),
]

def card(c, r, i):
    m = c["metric"]
    return f"""<a class="work reveal card-{c['slug']}" href="{r}work/{c['slug']}.html" id="project-{c['slug']}" data-project="{c['slug']}">
  <div class="work-media parallax" data-speed="48"><img src="{r}{IMG}{c['cover']}" alt="{e(c['brand'])} product screens" loading="{'eager' if i==0 else 'lazy'}"></div>
  <div class="work-body">
    <div class="work-tag"><span class="brand">{e(c['brand'])}</span><span class="eyebrow">{e(c['region'])} · {e(c['year'])}</span></div>
    <span class="muted">{e(c['brand'])} · {e(c['role_short'])}</span>
    <h3 class="h2">{e(c['card_title'])}</h3>
    <p class="muted">{e(c['card_text'])}</p>
    <div class="metric"><b>{e(m[0])}</b><span>{e(m[1])}</span><span>{e(m[2])}</span></div>
    <span class="link-arrow">View case study</span>
  </div>
</a>"""

# ---------------------------------------------------------------- Home
def home():
    r = ""
    cards = "\n".join(card(c, r, i) for i, c in enumerate(CASES))
    chips = "".join(f'<a class="chip card-{c["slug"]}" data-for href="#project-{c["slug"]}" style="--c:var(--project)">{e(c["brand"])}</a>' for c in CASES)
    play = [("orangehrm-1.webp","OrangeHRM redesign","Web · HR system",""),
            ("gd-2.webp","Brand identities","Logos · Graphic design",""),
            ("vid-brand-intro.webp","AI marketing videos","Video · NovaLink","#ai-videos"),
            ("web-7.webp","Visual studies","Web and app interfaces","#studies")]
    play_html = "".join(f"""<a class="play-card reveal d{i%3+1}" href="play.html{p[3]}"><div class="work-media parallax" data-speed="{24 + i%2*22}"><img src="{r}{IMG}{p[0]}" alt="{e(p[1])}" loading="lazy"></div><h3>{e(p[1])}</h3><span class="eyebrow">{e(p[2])}</span></a>""" for i,p in enumerate(play))
    svcs = [("UI/UX design","User-centred research, flows, wireframes and prototypes that make complex products easier to use.",["Research","User flows","Wireframes","Prototypes","Design systems"],"work/dela.html","See it in Dela"),
            ("Custom software & business analysis","Requirements, workflows and scalable software built with a development team, from SaaS and POS to internal tools.",["Requirements","SaaS","POS","Web apps"],"work/novalink.html","See it in NovaLink"),
            ("Website development","Fast, responsive and accessible websites, designed and built in code or WordPress around business goals.",["Front-end","React","WordPress","Performance"],"play.html#studies","See the studies"),
            ("Graphic design & branding","Logos, brand patterns, signage and product graphics that stay recognisable at every size.",["Identity","Logos","Print","Illustration"],"play.html","See the brands"),
            ("Digital marketing & AI video","Marketing videos produced with AI tools, plus SEO and social campaigns that bring in the right people.",["AI video","SEO","Social media","Campaigns"],"play.html#ai-videos","Watch the videos")]
    svc_html = "".join(f"""<a class="svc reveal" href="{sv[3]}"><span class="svc-num">{i+1:03d}</span><span class="svc-main"><b class="svc-title">{e(sv[0])}</b><span class="svc-text">{e(sv[1])}</span><span class="svc-tags">{"".join(f"<span>{e(t)}</span>" for t in sv[2])}</span></span><span class="svc-link">{e(sv[4])} <i class="ar ar-ne" aria-hidden="true">↗</i></span></a>""" for i,sv in enumerate(svcs))
    body = f"""{head("Sanjula Thilan · UX Engineer, Melbourne","Sanjula Thilan, UX engineer and UI/UX designer in Melbourne. Case studies from Australia, the UK and Singapore: marketplaces, care homes, HR and SaaS.", r)}
{nav(r,'home')}
<main id="main">
<section class="sig-hero" id="top" aria-label="Introduction">
  <canvas class="contour" aria-hidden="true"></canvas>
  <span class="hero-glow" aria-hidden="true"></span>
  <div class="wrap sig-content" data-hero-drift>
    <p class="hero-name" data-arrive>Sanjula Thilan <span>UX Engineer · Melbourne</span></p>
    <h1 class="sig-h1"><span class="hero-line"><span>Making complex</span></span><span class="hero-line"><span>work <em>feel simple.</em></span></span></h1>
    <div class="hero-foot">
      <div class="hero-cred" data-arrive>
        <p>UX Engineer and founder of <strong>NovaLink Innovations.</strong><br>I turn tangled workflows into products people can understand, trust and use.</p>
        <p>4+ years with teams in Australia, the UK, Singapore and Sri Lanka.</p>
      </div>
      <div class="hero-actions" data-arrive>
        <a class="primary-link" href="#work" data-magnetic>Explore my work <svg class="nudge" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v16m-7-7 7 7 7-7"/></svg></a>
      </div>
    </div>
  </div>
  <a class="hero-scroll" href="#work"><span class="scroll-track" aria-hidden="true"><i></i></span>Scroll to explore</a>
</section>

<section id="work" class="selected-work">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="h-xl reveal" data-drift="-40">Selected work</h2>
      <p class="muted reveal">Products for marketplaces, care homes, HR teams and project teams, each taken from requirements to interface.</p>
      <div class="chips reveal">{chips}</div>
    </div>
    <div class="work-list">
{cards}
    </div>
  </div>
</section>

<section id="services" class="services-sec">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow reveal">What I do</span>
      <h2 class="h-xl reveal" data-drift="-30">Five ways <em>I can help.</em></h2>
      <p class="muted reveal" style="max-width:56ch">For teams hiring a UX engineer, and for businesses working with NovaLink Innovations. Each one links to work that shows it.</p>
    </div>
    <div class="services">{svc_html}</div>
    <div class="svc-cta reveal"><p class="muted">Not sure which one you need? Most projects mix two or three.</p><a class="btn btn-dark" href="{CAL}" target="_blank" rel="noopener">Book a 15-minute call <i class="ar ar-ne" aria-hidden="true">↗</i></a><a class="btn btn-ghost" href="contact.html#brief">Send a brief <i class="ar ar-e" aria-hidden="true">→</i></a></div>
  </div>
</section>

<section style="background:var(--paper-2)">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow reveal">The other side of my brain</span>
      <h2 class="h-xl reveal" data-drift="40">Brands, videos <em>and</em> side work.</h2>
      <p class="muted reveal" style="max-width:52ch">Not every project needs a full case study. Redesigns, identities and experiments live in the playground.</p>
    </div>
    <div class="play-grid">{play_html}</div>
    <p style="margin-top:32px"><a class="link-arrow" href="play.html">Inside the playground</a></p>
  </div>
</section>

<section>
  <div class="wrap split">
    <div class="reveal">
      <div class="portrait parallax" data-speed="60"><img src="{r}{IMG}portrait-wall.webp" alt="Sanjula Thilan standing in front of a stone wall" loading="lazy"></div>
      <div class="route">
        <div><b>Colombo</b><span>Studied</span></div>
        <div><b>Remote</b><span>UK · SG · AU clients</span></div>
        <div><b>Melbourne</b><span>Home</span></div>
      </div>
    </div>
    <div class="prose">
      <span class="eyebrow reveal">Designer at work. Engineer at heart.</span>
      <h2 class="h2 reveal">Software roots. <em>A user-first</em> practice.</h2>
      <p class="reveal">I'm Thilan. I trained as a software engineer, then found the part I loved most: the space between what a business needs and what a person can actually use. I work across research, UI/UX, front-end code and business analysis.</p>
      <p class="reveal">I also run NovaLink Innovations, a small studio building websites and software for local businesses, and I'm studying at Swinburne University in Melbourne.</p>
      <p class="reveal"><a class="link-arrow" href="about.html">The longer version</a></p>
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <span class="eyebrow reveal" style="display:block;margin-bottom:24px">The people side of design</span>
    <figure class="quote reveal" style="margin:0">
      <blockquote>He has a great sense to design with the user in mind. His designs are simple yet impactful, and he has a great eye for colour, look and feel.</blockquote>
      <figcaption><img src="{r}{IMG}t-yusra.webp" alt="" loading="lazy"><div><b>Yusra Aziz-Eliyas</b><br><span>Head of Business Consultancy</span></div></figcaption>
    </figure>
    <p style="margin-top:28px"><a class="link-arrow" href="about.html#working-together">More from clients and teammates</a></p>
  </div>
</section>
</main>
{closing(r)}"""
    write("index.html", body)

# ---------------------------------------------------------------- Case study
TOC = [("overview","Overview"),("solutions","Solution previews"),("mandate","The mandate"),("turning-point","The turning point"),("decisions","Key decisions"),("process","Process & screens"),("impact","Impact & reflection")]

def case_page(idx):
    c = CASES[idx]; r = "../"
    nxt = CASES[(idx+1) % len(CASES)]
    n = f"{idx+1:02d}"
    toc = "".join(f'<a href="#{k}">{v}</a>' for k,v in TOC)
    previews = "".join(f"""<a class="dcard reveal d{i+1}" href="#{p[4]}"><div class="dimg parallax" data-speed="30"><img src="{r}{IMG}{p[0]}" alt="{e(p[2])}" loading="lazy"></div><div class="dbody"><span class="eyebrow">{i+1:02d} / {e(p[1])}</span><h3 class="h3">{e(p[2])}</h3><p class="muted">{e(p[3])}</p><span class="link-arrow">Read the decision</span></div></a>""" for i,p in enumerate(c["previews"]))
    mand = "".join(f'<p class="reveal">{e(p)}</p>' for p in c["mandate"])
    mlist = "".join(f"<li>{e(x)}</li>" for x in c["mandate_list"])
    turn = "".join(f'<p class="reveal">{e(p)}</p>' for p in c["turn"])
    decs = "".join(f'<div class="dec reveal"><span class="eyebrow">Decision {i+1:02d}</span><h3 class="h3">{e(d[0])}</h3><p class="muted">{e(d[1])}</p></div>' for i,d in enumerate(c["decisions"]))
    total = len(c["gallery"])
    slides = "".join(f'<figure class="slide"><div class="simg" data-zoom><img src="{r}{IMG}{g[0]}" alt="{e(g[1])}: {e(g[2])}" loading="lazy"></div><figcaption><b>{e(g[1])}</b><span>{e(g[2])}</span></figcaption></figure>' for g in c["gallery"])
    stats = "".join(f'<div class="reveal"><b>{e(s[0])}</b><span>{e(s[1])}</span></div>' for s in c["stats"])
    q = c["quote"]
    qimg = f'<img src="{r}{IMG}{q[3]}" alt="" loading="lazy">' if q[3] else ""
    body = f"""{head(f"{c['brand']} · Sanjula Thilan", c['promise'], r, f"work/{c['slug']}.html", c["og"])}
{nav(r,'work')}
<main id="main" class="case-{c['slug']}">
<section class="sig-hero sig-sub sig-case" id="top" aria-label="Introduction">
  <canvas class="contour" aria-hidden="true"></canvas>
<div class="wrap cs-hero">
  <a class="crumb" href="{r}index.html#project-{c['slug']}"><i class="ar ar-w" aria-hidden="true">←</i> Selected work</a>
  <div id="overview">
    <h1 class="sig-h1"><span class="hero-line"><span>{e(c['title'].rstrip('.'))}<em>.</em></span></span></h1>
    <p class="lede reveal">{e(c['promise'])}</p>
    <div class="cs-role reveal"><b>{e(c['role_line'][0])}</b><span class="muted">{e(c['role_line'][1])}</span></div>
    <div class="cs-actions reveal"><a class="btn btn-dark" href="#solutions">See the solutions <i class="ar ar-d" aria-hidden="true">↓</i></a><a class="btn btn-ghost" href="#impact">Jump to impact <i class="ar ar-d" aria-hidden="true">↓</i></a></div>
  </div>
</div>
</section>
<div class="wrap">
  <figure style="margin:0">
    <div class="plate parallax reveal" data-speed="70"><img src="{r}{IMG}{c['cover']}" alt="{e(c['brand'])} cover" loading="eager"></div>
    <figcaption class="plate-cap"><span>{e(c['brand'])} · final design</span><span>{e(c['region'])}</span></figcaption>
  </figure>

  <div class="triad">
    <div class="reveal"><h2>The problem</h2><p>{e(c['problem'])}</p></div>
    <div class="reveal d1"><h2>The solution</h2><p>{e(c['solution'])}</p></div>
    <div class="reveal d2"><h2>The impact</h2><p class="big">{e(c['impact_big'])}</p><p class="muted" style="font-size:16px">{e(c['impact'])}</p><!-- Replace with a measured result when you have one, e.g. "3 days → 4 hours" --></div>
  </div>
  <div class="facts">
    <div class="reveal"><span class="eyebrow">My role</span><p>{e(c['myrole'])}</p></div>
    <div class="reveal d1"><span class="eyebrow">The central decision</span><p>{e(c['central'])}</p></div>
    <div class="reveal d2"><span class="eyebrow">Project scope</span><p>{e(c['scope'])}</p></div>
  </div>

  <section id="solutions" style="padding-bottom:0">
    <div class="sec-head"><h2 class="h2 reveal">The decisions behind the experience</h2><p class="muted reveal">See the interface. Follow the decision.</p></div>
    <div class="decisions">{previews}</div>
    <a class="story-intro reveal" href="#mandate"><span><span class="eyebrow">The story behind the decisions</span><br><b>Research, exploration, and what I learned</b></span><i class="ar ar-d" aria-hidden="true">↓</i></a>
  </section>
</div>

<div class="wrap cs-body">
  <aside class="toc" aria-label="On this page"><span class="eyebrow">On this page</span>{toc}<a href="{r}index.html#work" style="margin-top:14px"><i class="ar ar-w" aria-hidden="true">←</i> All selected work</a></aside>
  <div>
    <section class="chapter" id="mandate">
      <span class="eyebrow">01 / The mandate</span>
      <h2 class="h2 reveal">{e(c['mandate_h'])}</h2>
      <div class="prose">{mand}</div>
      <div class="callout reveal"><span class="eyebrow">The stakes</span><p>{e(c['stakes'])}</p></div>
      <ol class="list-num reveal">{mlist}</ol>
    </section>

    <section class="chapter" id="turning-point">
      <span class="eyebrow">02 / The turning point</span>
      <h2 class="h2 reveal">{e(c['turn_h'])}</h2>
      <div class="prose">{turn}</div>
      <div class="callout reveal"><span class="eyebrow">The trade-off</span><h3 class="h3">{e(c['tradeoff'][0])}</h3><p class="muted" style="font-size:17px">{e(c['tradeoff'][1])}</p></div>
      <div class="callout decision reveal"><span class="eyebrow">The design decision</span><p>{e(c['decision_quote'])}</p></div>
    </section>

    <section class="chapter" id="decisions">
      <span class="eyebrow">03 / Key decisions</span>
      <h2 class="h2 reveal">What shaped the interface.</h2>
      <div class="dec-grid">{decs}</div>
    </section>

    <section class="chapter" id="process">
      <span class="eyebrow">04 / Process & screens</span>
      <h2 class="h2 reveal">From requirements to a working model.</h2>
      <!-- Add process images here as extra slides: user flows, wireframes, journey maps, a direction you set aside. -->
      <div class="carousel reveal">
        <div class="car-head"><span class="muted">The final design, screen by screen</span><div class="car-ctrl"><button type="button" data-prev aria-label="Previous image">←</button><span class="car-count">01 / {total:02d}</span><button type="button" data-next aria-label="Next image">→</button></div></div>
        <div class="car-track">{slides}</div>
      </div>
    </section>

    <section class="chapter" id="impact">
      <span class="eyebrow">05 / Impact & reflection</span>
      <h2 class="h2 reveal">{e(c['impact_h'])}</h2>
      <div class="prose"><p class="reveal">{e(c['impact_text'])}</p></div>
      <div class="stats">{stats}</div>
      <p class="note reveal">Figures describe the scope of the design work. Measured results will be added as they become available.</p>
      <figure class="quote reveal" style="margin:24px 0 0"><span class="eyebrow" style="display:block;margin-bottom:18px">On working together</span><blockquote>{e(q[0])}</blockquote><figcaption>{qimg}<div><b>{e(q[1])}</b><br><span>{e(q[2])}</span></div></figcaption></figure>
      <div class="callout reveal" style="margin-top:24px"><span class="eyebrow">What this changed about how I design</span><p>{e(c['lesson'])}</p></div>
    </section>
  </div>
</div>

<div class="wrap" style="padding-bottom:clamp(72px,9vw,120px)">
  <a class="next reveal" href="{nxt['slug']}.html">
    <div class="work-body"><span class="eyebrow">Next project · {e(nxt['brand'].upper())}</span><h2 class="h2">{e(nxt['card_title'])}</h2><p class="muted">{e(nxt['card_text'])}</p><span class="link-arrow">Explore the project</span></div>
    <div class="work-media parallax" data-speed="30"><img src="{r}{IMG}{nxt['cover']}" alt="{e(nxt['brand'])} cover" loading="lazy"></div>
  </a>
</div>
</main>
{closing(r)}"""
    write(f"work/{c['slug']}.html", body)

# ---------------------------------------------------------------- About
def about():
    r = ""
    journey = [
      ("Dec 2025 to now","Flash Line Transport","Senior UX Engineer · Australia","Redesigning a logistics platform for driver and operations teams, WCAG-compliant web and mobile UI built with developers in React.",None),
      ("Nov 2025 to Mar 2026","Active Care","Associate UX Designer · United Kingdom","Role-based care home software for nurses, carers and managers.","work/active-care.html"),
      ("Nov 2025 to Mar 2026","LK Domain Registry","Senior UX Engineer · Sri Lanka","End-to-end registry flows and onboarding, with detailed specs for front-end handover.",None),
      ("Nov 2025 to Mar 2026","Nice & Tidy","UX Engineer & Developer · Melbourne","Responsive, accessible websites in WordPress and Tailwind CSS, including EcoWax.",None),
      ("Until Nov 2025","Digiratina Technologies","UX Engineer · Sri Lanka","UI/UX for four Australian-client platforms: DelaExchange, NewsQueck, UPS Delivery and MoneyGram.","work/dela.html"),
      ("Mar 2025","IOM World","UX Engineer · Singapore","A mobile leave, overtime and attendance app with face recognition.","work/iom-world.html"),
      ("Jan 2025 to now","NovaLink Innovations","Founder & Lead UX Engineer","UI/UX and front-end for client systems and our own project management SaaS.","work/novalink.html"),
    ]
    jrows = "".join(f"""<div class="jrow reveal"><span class="when">{e(j[0])}</span><div class="what"><b>{e(j[1])}</b><i>{e(j[2])}</i><span class="muted" style="font-size:15px">{e(j[3])}</span></div>{f'<a href="{j[4]}">Explore <i class="ar ar-ne" aria-hidden="true">↗</i></a>' if j[4] else '<span></span>'}</div>""" for j in journey)
    principles = [("Requirements before pixels.","Start with the work people need to do and the business rules around it. A clear requirement makes a simple screen possible.","work/active-care.html#mandate","Requirements in Active Care"),
                  ("Trust lives in the interface.","Show status, show progress, explain what happens next. People trust what they can see.","work/dela.html#decisions","Visible states in Dela"),
                  ("Design it so it can be built.","I design components with their states defined, then help build them. Handover should be a conversation, not a surprise.","work/novalink.html#decisions","From Figma to React")]
    pcards = "".join(f'<div class="pcard reveal d{i+1}"><span class="num">{i+1:02d}</span><h3>{e(p[0])}</h3><p class="muted">{e(p[1])}</p><a href="{p[2]}">{e(p[3])} <i class="ar ar-ne" aria-hidden="true">↗</i></a></div>' for i,p in enumerate(principles))
    quotes = [("Sanjula Thilan was a valuable member of my Dela dev team. He delivered quality work, was pro-active in problem solving, open to feedback and easy to work with.","Megan van der Velde","Founder, Dela (Australia)","t-megan.webp"),
              ("Thilan is an individual with amazing ideas and has a great sense to design with the user in mind. His designs are simple yet impactful and he has a great eye for colour, look and feel.","Yusra Aziz-Eliyas","Head of Business Consultancy","t-yusra.webp"),
              ("Thilan is a talented UX Business Analyst, blending design and development to deliver user-focused solutions.","Varatharaja Kajamugan","Head of Software, LK Domain Registry","t-kajan.webp"),
              ("Working with Thilan was a pleasure; talented in multiple software, he delivered a user-friendly, beautifully designed website.","Jitendra","Operations Manager, IOM World","t-jit.webp")]
    qcards = "".join(f'<figure class="qcard reveal"><blockquote>{e(q[0])}</blockquote><figcaption><img src="{r}{IMG}{q[3]}" alt="" loading="lazy"><span><b>{e(q[1])}</b>{e(q[2])}</span></figcaption></figure>' for q in quotes)
    edu = [("BSc (Hons) Software Engineering","NSBM Green University · Specialisation in UX business analysis"),
           ("Swinburne University of Technology","Melbourne · Current study"),
           ("AI / ML course","SLIIT University, Malabe"),
           ("Web Design Program","University of Moratuwa"),
           ("Diploma in Information Technology","Esoft Metro Campus"),
           ("Diploma in English","Esoft Metro Campus · Pearson")]
    eduh = "".join(f'<div class="reveal"><b>{e(a)}</b><span>{e(b)}</span></div>' for a,b in edu)
    body = f"""{head("About · Sanjula Thilan","Meet Sanjula Thilan: UX engineer in Melbourne, founder of NovaLink Innovations, working across UI/UX, front-end and business analysis.", r, "about.html", "about.jpg")}
{nav(r,'about')}
<main id="main">
<section class="sig-hero sig-sub" id="top" aria-label="Introduction">
  <canvas class="contour" aria-hidden="true"></canvas>
  <div class="wrap split">
    <div class="prose" style="max-width:none">
      <span class="eyebrow">Hi, I'm Thilan.</span>
      <h1 class="sig-h1"><span class="hero-line"><span>Designer.</span></span><span class="hero-line"><span>Engineer.</span></span><span class="hero-line"><span><em>Problem-solver.</em></span></span></h1>
      <p class="lede reveal">I'm a UX engineer working across UI/UX design, front-end development and business analysis, based in Melbourne.</p>
      <p class="reveal">I turn messy requirements into a direction a team can build: user flows, a design system, and front-end components that make the decisions real. Across marketplaces, care homes, HR tools and SaaS, I've stayed close to both the system and the details.</p>
      <p class="reveal"><a class="btn btn-dark" href="{RESUME}" target="_blank" rel="noopener">Download my resume <i class="ar ar-d" aria-hidden="true">↓</i></a></p>
      <div class="jump reveal"><a class="chip" href="#journey">My journey <i class="ar ar-d" aria-hidden="true">↓</i></a><a class="chip" href="#principles">How I work <i class="ar ar-d" aria-hidden="true">↓</i></a><a class="chip" href="#working-together">Working together <i class="ar ar-d" aria-hidden="true">↓</i></a><a class="chip" href="#learning">Learning <i class="ar ar-d" aria-hidden="true">↓</i></a></div>
    </div>
    <figure class="reveal d1" style="margin:0">
      <div class="portrait parallax"><img src="{r}{IMG}portrait-grad.webp" alt="Sanjula Thilan at his graduation" loading="eager"></div>
      <figcaption class="plate-cap"><span>Educated in Colombo. Based in Melbourne.</span></figcaption>
    </figure>
  </div>
</section>

<section id="journey" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow reveal">The journey so far</span><h2 class="h-xl reveal">Different clients. <em>A connected</em> point of view.</h2></div>
    <div class="journey">{jrows}</div>
  </div>
</section>

<section id="principles" style="background:var(--paper-2)">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow reveal">How I think about design</span><h2 class="h-xl reveal">Good design makes <em>work feel lighter.</em></h2></div>
    <div class="principles on-tint">{pcards}</div>
  </div>
</section>

<section id="working-together">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow reveal">From the other side of the table</span><h2 class="h-xl reveal">What it's like <em>to work together.</em></h2><p class="muted reveal">A few words from the people I've built with.</p></div>
    <div class="quotes">{qcards}</div>
  </div>
</section>

<section id="learning" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow reveal">Always learning</span><h2 class="h2 reveal">Education</h2></div>
    <div class="edu">{eduh}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap split">
    <div class="prose">
      <span class="eyebrow reveal">Off the clock</span>
      <h2 class="h2 reveal">A small studio <em>on the side.</em></h2>
      <p class="reveal">Outside client and employed work, I run NovaLink Innovations, building websites, custom software and brands for small businesses. It keeps me close to real customers and real budgets, which makes me a more practical designer.</p>
      <p class="reveal"><a class="link-arrow" href="play.html">See what I've been making</a></p>
    </div>
    <div class="lab-media parallax reveal"><img src="{r}{IMG}web-1.webp" alt="A client website designed by NovaLink Innovations" loading="lazy"></div>
  </div>
</section>
</main>
{closing(r)}"""
    write("about.html", body)

# ---------------------------------------------------------------- Play
def play():
    r = ""
    items = [
      ("orangehrm-2.webp","OrangeHRM redesign","Web · HR system · 2024","A redesign of a feature-rich HR system for leave, attendance and employee records.","Could a dense HR tool feel quick for everyday tasks?","I focused on the three most-used workflows: leave, records and attendance. Clearer hierarchy, shorter forms and the team calendar beside the leave form.","In an enterprise redesign, respecting what users already know matters as much as improving it."),
      ("gd-2.webp","NextStop identity","Brand identity · 2025","Logo, orange brand pattern and staff ID badge for NextStop.","How does a brand stay recognisable on a badge and a screen?","A simple mark with a repeatable pattern, so the identity works at any size and on any surface.","A good identity system is mostly rules: colour, spacing and where the mark goes."),
      ("gd-3.webp","Pet Mate graphics","Brand graphics · 2025","A hanging sign and community welcome banner for Pet Mate.","What makes a local brand feel friendly from across the street?","Warm colour, rounded shapes and short, readable lines of text.","Signage is read in seconds. Fewer words, bigger shapes."),
      ("gd-1.webp","Workforce platform graphics","Illustration · Dashboard graphics · IOM World","Illustrations and dashboard graphics for an AI attendance platform.","How do you explain face recognition without a manual?","Clean illustrations for location and face checks, plus status icons and chart graphics for manager dashboards.","Graphics in a product are part of the UX. They should explain, not decorate."),
      ("vid-brand-intro.webp","AI marketing videos","Video · NovaLink Innovations · 2026","A motion brand intro, an explainer with AI voiceover and a vertical social reel for NovaLink Innovations.","Can a small studio publish brand video every month?","Scripted and directed by me, generated with AI tools, then edited by hand so every piece keeps NovaLink's blue palette, logo and type.","AI speeds up production. Taste and editing still decide whether it feels like your brand.","#ai-videos"),
    ]
    def media(it, i):
        if len(it) > 7:
            return f'''<a class="lab-media lab-play parallax reveal" href="{it[7]}"><img src="{r}{IMG}{it[0]}" alt="{e(it[1])}" loading="lazy"><span class="play-pill">Watch the videos ↓</span></a>'''
        return f'''<div class="lab-media parallax reveal" data-zoom><img src="{r}{IMG}{it[0]}" alt="{e(it[1])}" loading="{'eager' if i==0 else 'lazy'}"></div>'''
    videos = [("novalink-brand-intro.mp4","vid-brand-intro.webp","Brand intro","Motion branding · 0:16","wide"),
              ("novalink-custom-software.mp4","vid-custom-software.webp","Custom software development","Explainer · AI voiceover · 0:27","wide"),
              ("novalink-reel.mp4","vid-reel.webp","Social reel","Vertical 9:16 · Reels, Shorts and Stories · 1:15","tall")]
    vids = "".join(f'''<figure class="vid vid-{v[4]} reveal d{i+1}"><div class="vid-frame"><video src="{r}assets/video/{v[0]}" poster="{r}{IMG}{v[1]}" controls playsinline preload="none" aria-label="{e(v[2])} video"></video></div><figcaption><b>{e(v[2])}</b><span>{e(v[3])}</span></figcaption></figure>''' for i,v in enumerate(videos))
    rows = "".join(f"""<article class="lab-item">
  {media(it, i)}
  <div class="lab-body">
    <span class="eyebrow reveal">{e(it[2])}</span>
    <h2 class="reveal">{e(it[1])}</h2>
    <p class="muted reveal">{e(it[3])}</p>
    <div class="qbox reveal"><span class="eyebrow">The question behind it</span><h3>{e(it[4])}</h3></div>
    <div class="qbox reveal"><span class="eyebrow">Inside the idea</span><p>{e(it[5])}</p></div>
    <div class="qbox reveal"><span class="eyebrow">The design lesson</span><p>{e(it[6])}</p></div>
  </div>
</article>""" for i,it in enumerate(items))
    studies = ["web-1.webp","web-2.webp","web-3.webp","web-4.webp","web-5.webp","web-6.webp","web-7.webp","zendirib.webp"]
    mosaic = "".join(f'<div class="simg reveal" data-zoom><img src="{r}{IMG}{s}" alt="Interface study {i+1}" loading="lazy"></div>' for i,s in enumerate(studies))
    body = f"""{head("Play · Sanjula Thilan","Redesigns, brand identities, AI marketing videos and interface studies by Sanjula Thilan, with the ideas behind them.", r, "play.html", "graphic-design.jpg")}
{nav(r,'play')}
<main id="main">
<section class="sig-hero sig-sub" id="top" aria-label="Introduction">
  <canvas class="contour" aria-hidden="true"></canvas>
  <div class="wrap">
    <span class="eyebrow">Side projects · Designed and made by me</span>
    <h1 class="sig-h1"><span class="hero-line"><span>Made for the</span></span><span class="hero-line"><span><em>love of it.</em></span></span></h1>
    <p class="lede reveal" style="margin-top:28px">Redesigns, brands and experiments that didn't need a full case study, with notes on the decisions behind them.</p>
  </div>
</section>
<section style="padding-top:0"><div class="wrap lab">{rows}</div></section>
<section id="ai-videos" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow reveal">AI marketing videos · NovaLink Innovations</span><h2 class="h2 reveal">Three formats, <em>one brand.</em></h2><p class="muted reveal" style="max-width:52ch">An opener for socials and the website, an explainer for the custom software service, and a vertical reel. Press play; sound is on.</p></div>
    <div class="vids">{vids}</div>
  </div>
</section>
<section id="studies" style="background:var(--paper-2)">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow reveal">Visual studies</span><h2 class="h2 reveal">Interfaces from client and studio work.</h2><p class="muted reveal">Tap any image to take a closer look.</p></div>
    <div class="mosaic">{mosaic}</div>
  </div>
</section>
</main>
{closing(r)}"""
    write("play.html", body)

# ---------------------------------------------------------------- Contact
def contact():
    r = ""
    ways = [("01","Send a project brief","Tell me what you're building. I reply within two working days.","#brief","Write a brief ↓"),
            ("02","Book a 15-minute call","A quick chat to see if we're a good fit, no preparation needed.",CAL,"Pick a time ↗"),
            ("03","Email or call","For anything else, including roles in Melbourne.",f"mailto:{EMAIL}",EMAIL)]
    NEWTAB = ' target="_blank" rel="noopener"'
    wcards = "".join(f'<a class="pcard way reveal d{i+1}" href="{w[3]}"{NEWTAB if w[3].startswith("http") else ""}><span class="num">{w[0]}</span><h3>{e(w[1])}</h3><p class="muted">{e(w[2])}</p><span class="link-arrow-plain">{e(w[4])}</span></a>' for i,w in enumerate(ways))
    body = f"""{head("Contact · Sanjula Thilan","Start a project with Sanjula Thilan, UX engineer in Melbourne: send a brief, book a 15-minute call or email directly.", r, "contact.html")}
{nav(r,'contact')}
<main id="main">
<section class="sig-hero sig-sub" id="top" aria-label="Introduction">
  <canvas class="contour" aria-hidden="true"></canvas>
  <div class="wrap">
    <span class="eyebrow">Contact · Melbourne, <span data-clock></span></span>
    <h1 class="sig-h1"><span class="hero-line"><span>Three ways</span></span><span class="hero-line"><span><em>to say hello.</em></span></span></h1>
    <p class="lede reveal" style="margin-top:28px">Freelance projects through NovaLink Innovations, full-time UX roles, or a question about your product. Pick whichever suits you.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap"><div class="principles">{wcards}</div></div>
</section>
<section id="brief" style="background:var(--paper-2)">
  <div class="wrap split">
    <div class="prose">
      <span class="eyebrow reveal">Project brief</span>
      <h2 class="h2 reveal">Tell me about <em>the problem,</em> not just the screens.</h2>
      <p class="reveal">A few lines is plenty: who it's for, what's getting in their way, and when you'd like to start. Budgets and timelines help, but they're optional.</p>
      <div class="route reveal" style="grid-template-columns:repeat(2,minmax(0,1fr))">
        <div><b>Wyndham Vale, VIC</b><span>Melbourne, Australia</span></div>
        <div><b><a href="tel:{PHONE.replace(' ','')}" style="text-decoration:none">{PHONE}</a></b><span>Mon to Fri, Melbourne time</span></div>
      </div>
    </div>
    <form class="form reveal" id="contact-form" action="{r}mail.php" method="post" novalidate>
      <input type="hidden" name="form_started" value="">
      <div class="trap" aria-hidden="true"><label for="f-website">Leave this field empty</label><input id="f-website" type="text" name="website" tabindex="-1" autocomplete="off"></div>
      <div class="field"><label for="f-name">Your name</label><input id="f-name" type="text" name="Name" aria-describedby="e-name" autocomplete="name" maxlength="100" required><span class="err" id="e-name">Please add your name.</span></div>
      <div class="field"><label for="f-mail">Email</label><input id="f-mail" type="email" name="E-mail" aria-describedby="e-mail" autocomplete="email" required><span class="err" id="e-mail">Please add an email I can reply to.</span></div>
      <div class="field"><label for="f-msg">What are you working on?</label><textarea id="f-msg" name="Message" aria-describedby="e-msg" rows="6" maxlength="5000" required></textarea><span class="hint">Who it's for, what's in the way, and when you'd like to start.</span><span class="err" id="e-msg">Please add a short message.</span></div>
      <div class="form-foot"><button class="btn btn-dark" type="submit">Send message <i class="ar ar-ne" aria-hidden="true">↗</i></button><p class="form-status" role="status" aria-live="polite"></p></div>
    </form>
  </div>
</section>
</main>
{closing(r)}"""
    write("contact.html", body)

# ---------------------------------------------------------------- 404
def not_found():
    r = "/"
    body = f"""{head("Page not found · Sanjula Thilan","This page has moved or no longer exists.", r, "404.html", noindex=True)}
{nav(r,'')}
<main id="main">
<section class="sig-hero sig-sub" id="top" aria-label="Introduction">
  <canvas class="contour" aria-hidden="true"></canvas>
  <div class="wrap">
    <span class="eyebrow">Error 404</span>
    <h1 class="sig-h1"><span class="hero-line"><span>This page</span></span><span class="hero-line"><span><em>took a detour.</em></span></span></h1>
    <p class="lede reveal" style="margin-top:28px">It may have moved when the portfolio was rebuilt. The work is still here.</p>
    <div class="cs-actions reveal"><a class="btn btn-dark" href="/index.html#work">See selected work</a><a class="btn btn-ghost" href="/contact.html">Get in touch</a></div>
  </div>
</section>
</main>
{closing(r)}"""
    write("404.html", body)

if __name__ == "__main__":
    home(); about(); play(); contact(); not_found()
    for i in range(len(CASES)): case_page(i)
    print("Built into", OUT)
