/* ==========================================================================
   Sanjula Thilan — Portfolio 2026 · motion system
   GSAP + ScrollTrigger + SplitText, Lenis smooth scroll.
   ENTRY   : split-line reveals, image masks, fade/translate
   SCROLL  : parallax, pinned signature, horizontal work, colour canvas
   HOVER   : magnetic buttons, cursor labels, list previews
   PAGE    : curtain transitions between routes
   ========================================================================== */
(() => {
  const d = document;
  const root = d.documentElement;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  const isNarrow = () => innerWidth <= 900;
  const $ = (s, c = d) => c.querySelector(s);
  const $$ = (s, c = d) => [...c.querySelectorAll(s)];

  root.classList.add("js");
  if (reduce) root.classList.add("reduced");

  if (!window.gsap) { root.classList.remove("js", "is-entering"); return; }
  gsap.registerPlugin(ScrollTrigger, SplitText);
  gsap.defaults({ ease: "expo.out", duration: 1.1 });

  /* ---------- Colour canvas ---------- */
  const THEMES = {
    paper:  ["#F1EEE6", "#0F0E0C", "#9F8BE7"],
    night:  ["#111015", "#F1EEE6", "#DDF160"],
    violet: ["#9F8BE7", "#0F0E0C", "#0F0E0C"],
    lime:   ["#DDF160", "#0F0E0C", "#0F0E0C"],
    ember:  ["#FF5B22", "#0F0E0C", "#0F0E0C"],
    plum:   ["#241A4D", "#F1EEE6", "#DDF160"],
    cobalt: ["#3346FF", "#F1EEE6", "#DDF160"],
    blush:  ["#F6B9DA", "#0F0E0C", "#0F0E0C"],
    sand:   ["#E6DFD0", "#0F0E0C", "#FF5B22"],
  };
  let currentTheme = null;
  function setTheme(name, instant) {
    const t = THEMES[name];
    if (!t || name === currentTheme) return;
    currentTheme = name;
    gsap.to(root, {
      "--bg": t[0], "--fg": t[1], "--accent": t[2],
      duration: instant || reduce ? 0 : 0.9, ease: "power2.out", overwrite: true,
    });
  }
  const themed = $$("[data-theme]");
  if (themed.length) setTheme(themed[0].dataset.theme, true);

  /* ---------- Smooth scroll ---------- */
  let lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new Lenis({ lerp: 0.095, wheelMultiplier: 1, smoothWheel: true });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    window.lenis = lenis;
  }
  const scrollTo = (target) => {
    if (lenis) lenis.scrollTo(target, { duration: 1.6, easing: (t) => 1 - Math.pow(1 - t, 4) });
    else (typeof target === "number" ? scrollTo_(target) : target.scrollIntoView({ behavior: reduce ? "auto" : "smooth" }));
  };
  const scrollTo_ = (y) => window.scrollTo({ top: y, behavior: reduce ? "auto" : "smooth" });

  $$('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (id === "#") return;
      const el = id === "#top" ? 0 : $(id);
      if (el === null) return;
      e.preventDefault();
      closeMenu();
      scrollTo(el);
    });
  });

  /* ---------- Header: clock, hide/show ---------- */
  const clocks = $$("[data-clock]");
  const tick = () => {
    const now = new Date();
    const time = new Intl.DateTimeFormat("en-AU", { hour: "2-digit", minute: "2-digit", hour12: true, timeZone: "Australia/Melbourne" }).format(now);
    const tz = new Intl.DateTimeFormat("en-AU", { timeZoneName: "short", timeZone: "Australia/Melbourne" }).formatToParts(now).find((p) => p.type === "timeZoneName");
    clocks.forEach((c) => (c.textContent = `${time.toUpperCase()} ${tz ? tz.value : ""}`.trim()));
  };
  if (clocks.length) { tick(); setInterval(tick, 20000); }

  const header = $(".header");
  if (header) {
    let last = 0;
    ScrollTrigger.create({
      start: 0, end: "max",
      onUpdate: (self) => {
        const y = self.scroll();
        if (root.classList.contains("menu-open")) return;
        header.classList.toggle("is-hidden", y > 240 && self.direction === 1 && y > last);
        last = y;
      },
    });
  }

  /* ---------- Mobile menu ---------- */
  const menu = $(".menu");
  const menuBtn = $(".menu-btn");
  let menuTl = null;
  if (menu && menuBtn) {
    menuTl = gsap.timeline({ paused: true })
      .set(menu, { visibility: "visible" })
      .to(menu, { clipPath: "circle(150% at calc(100% - 45px) 43px)", duration: 0.9, ease: "power3.inOut" })
      .from($$(".menu__list a", menu), { yPercent: 110, stagger: 0.06, duration: 0.9 }, "-=.45")
      .from($(".menu__foot", menu), { opacity: 0, y: 20, duration: 0.6 }, "-=.6");
    menuBtn.addEventListener("click", () => (root.classList.contains("menu-open") ? closeMenu() : openMenu()));
    d.addEventListener("keydown", (e) => e.key === "Escape" && closeMenu());
  }
  function openMenu() {
    if (!menuTl) return;
    root.classList.add("menu-open");
    menuBtn.setAttribute("aria-expanded", "true");
    menu.removeAttribute("inert");
    lenis && lenis.stop();
    menuTl.timeScale(1).play();
  }
  function closeMenu() {
    if (!menuTl || !root.classList.contains("menu-open")) return;
    root.classList.remove("menu-open");
    menuBtn.setAttribute("aria-expanded", "false");
    menu.setAttribute("inert", "");
    lenis && lenis.start();
    menuTl.timeScale(1.6).reverse();
  }

  /* ---------- Cursor ---------- */
  const cursor = $(".cursor");
  if (cursor && fine && !reduce) {
    root.classList.add("has-cursor");
    const label = $(".cursor__ring", cursor);
    const xTo = gsap.quickTo(cursor, "x", { duration: 0.45, ease: "power3" });
    const yTo = gsap.quickTo(cursor, "y", { duration: 0.45, ease: "power3" });
    addEventListener("pointermove", (e) => { xTo(e.clientX); yTo(e.clientY); }, { passive: true });
    d.addEventListener("pointerover", (e) => {
      const lab = e.target.closest("[data-cursor]");
      if (lab) { label.textContent = lab.dataset.cursor; cursor.classList.add("is-label"); cursor.classList.remove("is-hover"); return; }
      cursor.classList.remove("is-label");
      cursor.classList.toggle("is-hover", !!e.target.closest("a, button, [role=button], input, textarea, label"));
    });
    d.addEventListener("pointerleave", () => cursor.classList.remove("is-label", "is-hover"));
  }

  /* ---------- Magnetic ---------- */
  if (fine && !reduce) {
    $$("[data-magnetic]").forEach((el) => {
      const strength = parseFloat(el.dataset.magnetic) || 0.35;
      const xTo = gsap.quickTo(el, "x", { duration: 0.8, ease: "power3" });
      const yTo = gsap.quickTo(el, "y", { duration: 0.8, ease: "power3" });
      el.addEventListener("pointermove", (e) => {
        const r = el.getBoundingClientRect();
        xTo((e.clientX - (r.left + r.width / 2)) * strength);
        yTo((e.clientY - (r.top + r.height / 2)) * strength);
      });
      el.addEventListener("pointerleave", () => { xTo(0); yTo(0); });
    });
  }

  /* ---------- Page transitions ---------- */
  const curtain = $(".curtain");
  const curtainWord = curtain && $(".curtain__word span", curtain);
  function leaveTo(href, word) {
    if (!curtain || reduce) { location.href = href; return; }
    try { sessionStorage.setItem("pt", "1"); } catch (_) {}
    if (curtainWord) curtainWord.textContent = word || "Loading";
    lenis && lenis.stop();
    gsap.timeline({ onComplete: () => (location.href = href) })
      .fromTo(curtain, { yPercent: 100 }, { yPercent: 0, duration: 0.85, ease: "power4.inOut" })
      .from(curtainWord, { yPercent: 110, duration: 0.6 }, "-=.35");
  }
  d.addEventListener("click", (e) => {
    const a = e.target.closest("a[href]");
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
    if (a.target === "_blank" || a.hasAttribute("download") || a.dataset.noTransition !== undefined) return;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin || !/^https?:/.test(url.protocol)) return;
    if (url.pathname === location.pathname && url.hash) return;
    e.preventDefault();
    leaveTo(url.href, a.dataset.label || a.textContent.trim().split("\n")[0].slice(0, 24));
  });
  function enterFromCurtain() {
    let entering = false;
    try { entering = sessionStorage.getItem("pt") === "1"; sessionStorage.removeItem("pt"); } catch (_) {}
    if (!curtain) return 0;
    if (entering && !reduce) {
      gsap.set(curtain, { yPercent: 0 });
      root.classList.remove("is-entering");
      gsap.to(curtain, { yPercent: -100, duration: 1, ease: "power4.inOut", delay: 0.1 });
      return 0.55;
    }
    root.classList.remove("is-entering");
    gsap.set(curtain, { yPercent: 100 });
    return 0;
  }
  addEventListener("pageshow", (e) => {
    if (e.persisted && curtain) { gsap.set(curtain, { yPercent: 100 }); lenis && lenis.start(); }
  });

  /* ---------- Reveals ---------- */
  function initReveals() {
    // split-line headings
    $$("[data-split]").forEach((el) => {
      if (reduce) return;
      const mode = el.dataset.split || "lines";
      SplitText.create(el, {
        type: mode === "chars" ? "lines,chars" : mode === "words" ? "lines,words" : "lines",
        mask: "lines",
        linesClass: "split-line",
        autoSplit: true,
        onSplit(self) {
          const targets = mode === "chars" ? self.chars : mode === "words" ? self.words : self.lines;
          return gsap.from(targets, {
            yPercent: 115, rotate: mode === "chars" ? 4 : 0,
            stagger: mode === "chars" ? 0.025 : mode === "words" ? 0.04 : 0.09,
            duration: 1.2,
            scrollTrigger: { trigger: el, start: "top 88%", once: true },
          });
        },
      });
    });

    // word-by-word scrub statements
    $$("[data-scrub]").forEach((el) => {
      if (reduce) return;
      const split = SplitText.create(el, { type: "words", wordsClass: "w" });
      gsap.to(split.words, {
        opacity: 1, stagger: 0.1, ease: "none",
        scrollTrigger: { trigger: el, start: "top 82%", end: "bottom 50%", scrub: 0.6 },
      });
      $$(".statement-inline-img", el).forEach((img) =>
        gsap.from(img, { width: 0, duration: 1.4, ease: "expo.inOut", scrollTrigger: { trigger: el, start: "top 70%", once: true } })
      );
    });

    // fade up
    if (!reduce) {
      ScrollTrigger.batch("[data-fade]", {
        start: "top 92%", once: true,
        onEnter: (batch) => gsap.to(batch, { opacity: 1, y: 0, stagger: 0.08, duration: 1.2, overwrite: true }),
      });
    }

    // image mask reveals
    $$("[data-img]").forEach((el) => {
      if (reduce) return;
      const img = $("img", el);
      const tl = gsap.timeline({ scrollTrigger: { trigger: el, start: "top 90%", once: true } });
      tl.to(el, { clipPath: "inset(0% 0 0 0)", duration: 1.4, ease: "expo.inOut" });
      if (img) tl.from(img, { scale: 1.35, duration: 1.8, ease: "expo.out" }, 0.1);
    });

    // parallax
    if (!reduce) {
      $$("[data-speed]").forEach((el) => {
        const s = parseFloat(el.dataset.speed) || 0.2;
        gsap.fromTo(el, { yPercent: -s * 50 }, { yPercent: s * 50, ease: "none", scrollTrigger: { trigger: el.parentElement, start: "top bottom", end: "bottom top", scrub: true } });
      });
      $$("[data-parallax-img]").forEach((img) => {
        gsap.fromTo(img, { yPercent: -8 }, { yPercent: 8, ease: "none", scrollTrigger: { trigger: img.parentElement, start: "top bottom", end: "bottom top", scrub: true } });
      });
    }

    // rules draw
    if (!reduce) $$(".rule").forEach((r) => gsap.from(r, { scaleX: 0, duration: 1.6, ease: "expo.inOut", scrollTrigger: { trigger: r, start: "top 92%", once: true } }));

    // theme sections
    themed.forEach((sec) => {
      ScrollTrigger.create({
        trigger: sec, start: "top 55%", end: "bottom 55%",
        onToggle: (self) => self.isActive && setTheme(sec.dataset.theme),
      });
    });
  }

  /* ---------- Marquees (scroll-direction aware) ---------- */
  function initMarquees() {
    $$(".marquee").forEach((m) => {
      const track = $(".marquee__track", m);
      if (!track) return;
      // fill to at least 2x the viewport so the loop never shows a gap
      const base = track.innerHTML;
      let guard = 0;
      while (track.scrollWidth < innerWidth * 2 && guard++ < 12) track.insertAdjacentHTML("beforeend", base);
      track.insertAdjacentHTML("beforeend", track.innerHTML);
      $$(":scope > *", track).forEach((n, i) => i >= track.children.length / 2 && n.setAttribute("aria-hidden", "true"));
      if (reduce) return;
      const speed = parseFloat(m.dataset.speed || 1);
      const baseDir = m.dataset.dir === "right" ? -1 : 1;
      let x = 0, dir = 1, half = track.scrollWidth / 2;
      addEventListener("resize", () => (half = track.scrollWidth / 2));
      let visible = true;
      ScrollTrigger.create({ trigger: m, start: "top bottom", end: "bottom top", onToggle: (s) => (visible = s.isActive) });
      gsap.ticker.add((_, dt) => {
        if (!visible) return;
        const v = lenis ? Math.min(Math.abs(lenis.velocity) * 0.08, 6) : 0;
        if (lenis && lenis.direction) dir = lenis.direction;
        x -= (0.045 * dt * speed * (1 + v)) * baseDir * dir;
        if (x <= -half) x += half;
        if (x > 0) x -= half;
        track.style.transform = `translate3d(${x}px,0,0)`;
      });
    });
  }

  /* ---------- HERO ---------- */
  function heroIntro(delay = 0) {
    const hero = $(".hero");
    if (!hero) return;
    // letter split (manual so the display words keep their glyph shapes)
    $$(".hero__word", hero).forEach((w) => {
      const txt = w.textContent.trim();
      w.setAttribute("aria-hidden", "true");
      w.textContent = "";
      [...txt].forEach((c) => { const s = d.createElement("span"); s.className = "ch"; s.textContent = c; w.appendChild(s); });
    });
    if (reduce) return;
    const tl = gsap.timeline({ delay });
    tl.from(".hero__meta > *", { y: 20, opacity: 0, stagger: 0.08, duration: 1 })
      .from(".hero__row--1 .ch", { yPercent: 110, rotate: 8, stagger: 0.045, duration: 1.3 }, 0.05)
      .from(".hero__row--2 .ch", { yPercent: 110, rotate: -8, stagger: { each: 0.045, from: "end" }, duration: 1.3 }, 0.18)
      .from(".hero__pill", { scaleX: 0, duration: 1.4, ease: "expo.inOut" }, 0.35)
      .from(".hero__pill img", { scale: 1.6, duration: 1.8 }, 0.4)
      .from(".hero__star", { rotate: -180, scale: 0, duration: 1.4 }, 0.6)
      .from(".hero__index", { opacity: 0, y: 10 }, 0.8)
      .from(".based__big > *", { yPercent: 110, opacity: 0, stagger: 0.08, duration: 1.1 }, 0.7)
      .from(".based__big .dash", { scaleX: 0, duration: 1, ease: "expo.inOut" }, 0.85)
      .from(".based__geo, .based__roles", { opacity: 0, y: 16, stagger: 0.1 }, 0.9)
      .from(".hero .band", { yPercent: 120, rotate: 0, duration: 1.3 }, 0.8);

    // scroll-out: rows drift apart, title gets lighter
    gsap.to(".hero__row--1", { xPercent: -8, ease: "none", scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });
    gsap.to(".hero__row--2", { xPercent: 8, ease: "none", scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });

    // pointer parallax
    if (fine) {
      const r1 = gsap.quickTo(".hero__row--1 .hero__word", "x", { duration: 1.2, ease: "power3" });
      const r2 = gsap.quickTo(".hero__row--2 .hero__word", "x", { duration: 1.2, ease: "power3" });
      const pi = gsap.quickTo(".hero__pill img", "xPercent", { duration: 1.2, ease: "power3" });
      const st = gsap.quickTo(".hero__star", "rotate", { duration: 1.2, ease: "power3" });
      hero.addEventListener("pointermove", (e) => {
        const nx = e.clientX / innerWidth - 0.5;
        r1(nx * -24); r2(nx * 24); pi(nx * -8); st(nx * 120);
      });
    }
  }

  function rolesSwap() {
    $$(".roles-swap").forEach((box) => {
      const items = $$("span", box);
      if (items.length < 2 || reduce) { items.slice(1).forEach((i) => (i.style.display = "none")); return; }
      let i = 0;
      gsap.set(items.slice(1), { yPercent: 110 });
      setInterval(() => {
        const cur = items[i], next = items[(i + 1) % items.length];
        gsap.to(cur, { yPercent: -110, duration: 0.9, ease: "expo.inOut" });
        gsap.fromTo(next, { yPercent: 110 }, { yPercent: 0, duration: 0.9, ease: "expo.inOut" });
        i = (i + 1) % items.length;
      }, 2400);
    });
  }

  /* ---------- Signature pinned reveal ---------- */
  function initSignature() {
    const sig = $(".signature");
    if (!sig || reduce) return;
    const tl = gsap.timeline({
      scrollTrigger: { trigger: sig, start: "top top", end: "+=140%", pin: true, scrub: 0.8, anticipatePin: 1 },
    });
    tl.to(".signature__media", { clipPath: "inset(0% 0% 0% 0% round 0px)", ease: "power2.inOut" }, 0)
      .to(".signature__media img", { scale: 1, ease: "power2.inOut" }, 0)
      .to(".signature__line--1", { xPercent: -28, ease: "none" }, 0)
      .to(".signature__line--2", { xPercent: 22, ease: "none" }, 0)
      .to(".signature__line--3", { xPercent: -14, ease: "none" }, 0)
      .from(".signature__cap", { opacity: 0, y: 20, duration: 0.3 }, 0.55);
  }

  /* ---------- Horizontal work ---------- */
  function initWork() {
    const wrap = $(".hscroll");
    if (!wrap) return;
    const track = $(".hscroll__track", wrap);
    const bar = $(".hscroll__bar i");
    const mm = gsap.matchMedia();
    mm.add("(min-width: 901px) and (prefers-reduced-motion: no-preference)", () => {
      const dist = () => track.scrollWidth - innerWidth;
      const tween = gsap.to(track, {
        x: () => -dist(), ease: "none",
        scrollTrigger: {
          trigger: wrap, pin: true, scrub: 0.9, start: "top top",
          end: () => "+=" + dist(), invalidateOnRefresh: true, anticipatePin: 1,
          onUpdate: (s) => bar && gsap.set(bar, { scaleX: s.progress }),
        },
      });
      $$(".panel", track).forEach((p) => {
        const img = $$(".panel__media img, .panel__imgs img", p);
        img.forEach((im, k) =>
          gsap.fromTo(im, { xPercent: k % 2 ? 6 : -6 }, { xPercent: k % 2 ? -6 : 6, ease: "none", scrollTrigger: { trigger: p, containerAnimation: tween, start: "left right", end: "right left", scrub: true } })
        );
        const name = $(".panel__name", p);
        if (name) gsap.from(name, { xPercent: 12, opacity: 0.2, ease: "none", scrollTrigger: { trigger: p, containerAnimation: tween, start: "left 95%", end: "left 35%", scrub: true } });
      });
    });
    mm.add("(max-width: 900px), (prefers-reduced-motion: reduce)", () => {
      if (reduce) return;
      $$(".panel", track).forEach((p) => gsap.from(p, { y: 60, opacity: 0, duration: 1.2, scrollTrigger: { trigger: p, start: "top 90%", once: true } }));
    });
  }

  /* ---------- Work list w/ cursor preview ---------- */
  function initWorkList() {
    const list = $(".wlist");
    const pv = $(".wpreview");
    if (!list || !pv || !fine) return;
    const imgs = $$("img", pv);
    const xTo = gsap.quickTo(pv, "x", { duration: 0.7, ease: "power3" });
    const yTo = gsap.quickTo(pv, "y", { duration: 0.7, ease: "power3" });
    const rTo = gsap.quickTo(pv, "rotate", { duration: 0.9, ease: "power3" });
    let lx = 0;
    list.addEventListener("pointermove", (e) => {
      const w = pv.offsetWidth, h = pv.offsetHeight;
      xTo(e.clientX - w / 2); yTo(e.clientY - h / 2);
      rTo(gsap.utils.clamp(-12, 12, (e.clientX - lx) * 0.6)); lx = e.clientX;
    });
    $$(".wrow", list).forEach((row, i) => {
      row.addEventListener("pointerenter", () => {
        imgs.forEach((im, k) => im.classList.toggle("is-on", k === i));
        gsap.to(pv, { opacity: 1, scale: 1, duration: 0.6, overwrite: "auto" });
      });
    });
    list.addEventListener("pointerleave", () => gsap.to(pv, { opacity: 0, scale: 0.6, duration: 0.5, overwrite: "auto" }));
  }

  /* ---------- Accordions ---------- */
  function initAccordions() {
    $$("[data-acc]").forEach((item) => {
      const btn = $("[data-acc-btn]", item);
      const panel = $("[data-acc-panel]", item);
      if (!btn || !panel) return;
      const open = (state, instant) => {
        item.classList.toggle("is-open", state);
        btn.setAttribute("aria-expanded", String(state));
        gsap.to(panel, { height: state ? "auto" : 0, duration: instant || reduce ? 0 : 0.8, ease: "expo.inOut", onComplete: () => ScrollTrigger.refresh() });
      };
      if (item.hasAttribute("data-acc-open")) open(true, true);
      btn.addEventListener("click", () => {
        const group = item.parentElement;
        const willOpen = !item.classList.contains("is-open");
        if (group.hasAttribute("data-acc-single")) $$("[data-acc].is-open", group).forEach((o) => o !== item && o._acc && o._acc(false));
        open(willOpen);
      });
      item._acc = open;
    });
  }

  /* ---------- Experience year ---------- */
  function initXpYear() {
    const out = $(".xp__year");
    if (!out) return;
    $$(".job[data-year]").forEach((job) =>
      ScrollTrigger.create({ trigger: job, start: "top 60%", end: "bottom 60%", onToggle: (s) => {
        if (!s.isActive || out.textContent === job.dataset.year) return;
        if (reduce) { out.textContent = job.dataset.year; return; }
        gsap.to(out, { yPercent: -30, opacity: 0, duration: 0.25, ease: "power2.in", onComplete: () => {
          out.textContent = job.dataset.year;
          gsap.fromTo(out, { yPercent: 30, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 0.6 });
        } });
      } })
    );
  }

  /* ---------- Testimonials ---------- */
  function initQuotes() {
    const box = $(".quotes");
    if (!box) return;
    const quotes = $$(".quote", box);
    const dots = $$(".qdot", box);
    const bar = $(".qbar i", box);
    let i = 0, timer = null, inView = false;
    const go = (n) => {
      if (n === i) return;
      const cur = quotes[i], next = quotes[n];
      dots[i].classList.remove("is-active"); dots[i].setAttribute("aria-selected", "false");
      dots[n].classList.add("is-active"); dots[n].setAttribute("aria-selected", "true");
      if (reduce) { cur.classList.remove("is-active"); next.classList.add("is-active"); i = n; return; }
      gsap.to(cur, { y: -30, opacity: 0, duration: 0.5, ease: "power2.in", onComplete: () => cur.classList.remove("is-active") });
      next.classList.add("is-active");
      gsap.fromTo(next, { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 1, delay: 0.35 });
      i = n;
      restart();
    };
    const restart = () => {
      if (timer) timer.kill();
      if (reduce || !inView) return;
      timer = gsap.fromTo(bar, { scaleX: 0 }, { scaleX: 1, duration: 8, ease: "none", onComplete: () => go((i + 1) % quotes.length) });
    };
    dots.forEach((dot, n) => dot.addEventListener("click", () => go(n)));
    ScrollTrigger.create({ trigger: box, start: "top 80%", end: "bottom 20%", onToggle: (s) => { inView = s.isActive; inView ? restart() : timer && timer.pause(); } });
  }

  /* ---------- CV ---------- */
  function initCV() {
    const docEl = $(".doc");
    if (!docEl) return;
    if (!reduce) {
      gsap.from($$(".doc__l", docEl), { scaleX: 0, stagger: 0.04, duration: 1, ease: "expo.out", scrollTrigger: { trigger: docEl, start: "top 80%", once: true } });
      gsap.from(docEl, { rotate: 14, yPercent: 20, duration: 1.6, scrollTrigger: { trigger: docEl, start: "top 90%", once: true } });
      gsap.from(".cv__arrow", { yPercent: -60, opacity: 0, duration: 1.2, scrollTrigger: { trigger: ".cv__title", start: "top 80%", once: true } });
    }
    if (fine && !reduce) {
      const holder = $(".cv__doc");
      const rx = gsap.quickTo(docEl, "rotationX", { duration: 0.8, ease: "power3" });
      const ry = gsap.quickTo(docEl, "rotationY", { duration: 0.8, ease: "power3" });
      holder.addEventListener("pointermove", (e) => {
        const r = holder.getBoundingClientRect();
        ry(((e.clientX - r.left) / r.width - 0.5) * 22);
        rx(-((e.clientY - r.top) / r.height - 0.5) * 18);
      });
      holder.addEventListener("pointerleave", () => { rx(0); ry(0); });
    }
  }

  /* ---------- Copy email ---------- */
  $$("[data-copy]").forEach((btn) => {
    const orig = btn.textContent;
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      try { await navigator.clipboard.writeText(btn.dataset.copy); btn.textContent = "Copied ✓"; }
      catch (_) { location.href = "mailto:" + btn.dataset.copy; return; }
      btn.classList.add("is-done");
      setTimeout(() => { btn.textContent = orig; btn.classList.remove("is-done"); }, 2200);
    });
  });

  /* ---------- Contact form ----------
     Static hosting (GitHub Pages) can't run mail.php. If EmailJS keys are set
     in window.EMAILJS_CONFIG the form sends directly; otherwise it opens the
     visitor's email app with the message pre-filled. */
  const form = $("#contact-form");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const note = $(".form__note", form);
      const data = Object.fromEntries(new FormData(form));
      const cfg = window.EMAILJS_CONFIG || {};
      if (window.emailjs && cfg.publicKey && cfg.serviceId && cfg.templateId) {
        note.textContent = "Sending…";
        try {
          emailjs.init(cfg.publicKey);
          await emailjs.sendForm(cfg.serviceId, cfg.templateId, form);
          note.textContent = "Thanks — your message is on its way. I'll get back to you soon.";
          form.reset();
        } catch (_) { note.textContent = "Couldn't send right now — please email sanjulathilan12321@gmail.com directly."; }
        return;
      }
      const subject = encodeURIComponent(`Portfolio enquiry from ${data.Name || ""}`.trim());
      const body = encodeURIComponent(`${data.Message || ""}\n\n— ${data.Name || ""}\n${data["E-mail"] || ""}`);
      note.textContent = "Opening your email app…";
      location.href = `mailto:sanjulathilan12321@gmail.com?subject=${subject}&body=${body}`;
    });
  }

  /* ---------- Footer wordmark ---------- */
  function initWordmark() {
    const wm = $(".wordmark");
    if (!wm) return;
    const letters = $$("span", wm);
    // fit the wordmark edge-to-edge
    const fit = () => {
      wm.style.fontSize = "";
      const avail = wm.clientWidth, used = letters.reduce((w, l) => w + l.offsetWidth, 0);
      if (used) wm.style.fontSize = (parseFloat(getComputedStyle(wm).fontSize) * (avail / used) * 0.97) + "px";
    };
    fit();
    addEventListener("resize", fit);
    if (reduce) return;
    gsap.from(letters, { yPercent: 100, stagger: 0.04, ease: "expo.out", duration: 1.4, scrollTrigger: { trigger: wm, start: "top 98%", once: true } });
  }

  /* ---------- Preloader ---------- */
  function preloader() {
    const loader = $(".loader");
    let seen = false;
    try { seen = sessionStorage.getItem("seen") === "1"; sessionStorage.setItem("seen", "1"); } catch (_) {}
    if (!loader || seen || reduce) { loader && loader.remove(); return Promise.resolve(0); }
    return new Promise((res) => {
      const num = $(".loader__count", loader);
      const obj = { v: 0 };
      lenis && lenis.stop();
      gsap.timeline({ onComplete: () => { loader.remove(); lenis && lenis.start(); } })
        .to(obj, { v: 100, duration: 1.6, ease: "power2.inOut", onUpdate: () => (num.textContent = String(Math.round(obj.v)).padStart(3, "0")) })
        .to(".loader__bar i", { scaleX: 1, duration: 1.6, ease: "power2.inOut" }, 0)
        .add(() => res(0.15))
        .to(loader, { yPercent: -100, duration: 1.1, ease: "power4.inOut" });
    });
  }

  /* ---------- Boot ---------- */
  const fontsReady = d.fonts && d.fonts.ready ? d.fonts.ready : Promise.resolve();
  const enterDelay = enterFromCurtain();
  Promise.race([fontsReady, new Promise((r) => setTimeout(r, 2500))]).then(async () => {
    const extra = await preloader();
    initMarquees();
    heroIntro(enterDelay + extra);
    rolesSwap();
    initSignature();
    initWork();
    initReveals();
    initWorkList();
    initAccordions();
    initXpYear();
    initQuotes();
    initCV();
    initWordmark();
    ScrollTrigger.refresh();
  });
  addEventListener("load", () => ScrollTrigger.refresh());
})();
