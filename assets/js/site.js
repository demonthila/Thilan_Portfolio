(function(){
  var root = document.documentElement;
  root.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Nav: border after scrolling, hide on scroll down, show on scroll up
  var nav = document.querySelector('.nav'), lastY = 0, toTop = document.querySelector('.to-top');
  function onScroll(){
    var y = window.scrollY;
    if (nav){
      nav.classList.toggle('scrolled', y > 8);
      if (!nav.classList.contains('open')) nav.classList.toggle('hide', y > 320 && y > lastY);
    }
    if (toTop) toTop.classList.toggle('show', y > 900);
    lastY = y;
  }
  window.addEventListener('scroll', onScroll, {passive:true}); onScroll();

  var menu = document.querySelector('.menu-btn');
  if (menu) menu.addEventListener('click', function(){
    var open = nav.classList.toggle('open');
    menu.setAttribute('aria-expanded', open);
    menu.textContent = open ? 'Close' : 'Menu';
  });

  // Home hero: a field of contour rings that slowly breathes, bends away from the pointer
  // and shifts as the page scrolls. Runs only while the hero is on screen.
  var field = document.querySelector('.contour'), hero = document.querySelector('.sig-hero');
  if (field && field.getContext && hero){
    var ctx = field.getContext('2d'), fw = 0, fh = 0, dpr = 1, t0 = performance.now();
    var ptr = {x: -9999, y: -9999, tx: -9999, ty: -9999, s: 0, ts: 0};
    var heroVisible = true, raf = 0, soft = hero.classList.contains('sig-sub') ? 0.6 : 1;
    // Accent rings take the page's project colour on case studies
    var hex = (getComputedStyle(hero).getPropertyValue('--project') || '').trim(), rgb = '178,77,44';
    var mh = /^#([0-9a-f]{6})$/i.exec(hex);
    if (mh){ var n = parseInt(mh[1], 16); rgb = [(n >> 16) & 255, (n >> 8) & 255, n & 255].join(','); }
    function size(){
      fw = field.clientWidth; fh = field.clientHeight; dpr = Math.min(window.devicePixelRatio || 1, 2);
      field.width = fw * dpr; field.height = fh * dpr;
    }
    function draw(now){
      if (!fw || !fh) return;
      var t = reduce ? 0 : (now - t0) / 1000, sy = Math.min(window.scrollY, fh);
      ptr.x += (ptr.tx - ptr.x) * 0.08; ptr.y += (ptr.ty - ptr.y) * 0.08; ptr.s += (ptr.ts - ptr.s) * 0.06;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, fw, fh);
      var cx = fw * 0.6, cy = fh * 0.46 - sy * 0.35, max = Math.hypot(fw, fh) * 0.8, step = fw < 600 ? 11 : 13, ring = 0;
      var grow = 1 + sy / fh * 0.35;
      for (var R = 18; R < max; R += step, ring++){
        ctx.beginPath();
        for (var a = 0; a <= Math.PI * 2 + 0.03; a += 0.03){
          var k = 1 + 0.06 * Math.sin(3 * a + R * 0.012 + t * 0.35) + 0.035 * Math.sin(5 * a - R * 0.021 - t * 0.22) + 0.02 * Math.cos(2 * a + R * 0.007 + t * 0.15);
          var x = cx + Math.cos(a) * R * k * 1.12 * grow, y = cy + Math.sin(a) * R * k * 0.86 * grow;
          if (ptr.s > 0.01){
            var dx = x - ptr.x, dy = y - ptr.y, d = Math.sqrt(dx * dx + dy * dy) || 1, f = Math.exp(-(d * d) / 9000) * 34 * ptr.s * soft;
            x += dx / d * f; y += dy / d * f;
          }
          if (a === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        var accent = ring % 9 === 4;
        ctx.strokeStyle = accent ? 'rgba(' + rgb + ',' + (0.3 * soft).toFixed(3) + ')' : 'rgba(22,20,15,' + ((0.13 - Math.min(R / max, 1) * 0.07) * soft).toFixed(3) + ')';
        ctx.lineWidth = accent ? 1.1 : 0.8;
        ctx.stroke();
      }
    }
    function loop(now){ draw(now); raf = heroVisible && !document.hidden ? requestAnimationFrame(loop) : 0; }
    function start(){ if (!raf && !reduce) raf = requestAnimationFrame(loop); }
    size(); draw(performance.now()); field.classList.add('drawn');
    if (!reduce){
      start();
      if ('IntersectionObserver' in window) new IntersectionObserver(function(es){ heroVisible = es[0].isIntersecting; if (heroVisible) start(); }).observe(hero);
      document.addEventListener('visibilitychange', start);
      var glow = hero.querySelector('.hero-glow');
      hero.addEventListener('pointermove', function(e){
        var r = field.getBoundingClientRect(), h = hero.getBoundingClientRect();
        ptr.tx = e.clientX - r.left; ptr.ty = e.clientY - r.top; ptr.ts = 1;
        if (ptr.x < -999){ ptr.x = ptr.tx; ptr.y = ptr.ty; }
        if (glow) glow.style.transform = 'translate(' + (e.clientX - h.left) + 'px,' + (e.clientY - h.top) + 'px)';
      });
      hero.addEventListener('pointerleave', function(){ ptr.ts = 0; });
    }
    var rt;
    window.addEventListener('resize', function(){ clearTimeout(rt); rt = setTimeout(function(){ size(); draw(performance.now()); }, 150); });
  }

  // Magnetic button: leans toward the pointer, springs back on leave
  if (!reduce && window.matchMedia('(hover: hover)').matches){
    document.querySelectorAll('[data-magnetic]').forEach(function(b){
      b.addEventListener('pointermove', function(e){
        var r = b.getBoundingClientRect();
        b.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * 0.25).toFixed(1) + 'px,' + ((e.clientY - r.top - r.height / 2) * 0.35).toFixed(1) + 'px)';
      });
      b.addEventListener('pointerleave', function(){ b.style.transform = ''; });
    });
  }

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce){
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
    }, {rootMargin:'0px 0px -8% 0px'});
    items.forEach(function(el){ io.observe(el); });
  } else items.forEach(function(el){ el.classList.add('in'); });
  // Safety: never leave content hidden
  setTimeout(function(){ items.forEach(function(el){ el.classList.add('in'); }); }, 4000);

  // Scroll parallax: images drift inside their frames, marked headings slide sideways,
  // and the home hero text lifts and fades as you scroll away. One rAF per scroll.
  // Give every page the same treatment without per-page markup:
  // images in frames get parallax, section headings drift, and the hero text lifts away.
  document.querySelectorAll('.work-media, .portrait, .plate, .dcard .dimg, .lab-media, .slide .simg, .mosaic .simg').forEach(function(el, i){
    if (!el.classList.contains('parallax')){ el.classList.add('parallax'); if (!el.hasAttribute('data-speed')) el.setAttribute('data-speed', el.closest('.mosaic') ? 18 + (i % 3) * 10 : 34); }
  });
  document.querySelectorAll('.sec-head h2, .chapter > h2, .prose > h2').forEach(function(h, i){
    if (!h.hasAttribute('data-drift')) h.setAttribute('data-drift', i % 2 ? 26 : -26);
  });
  var subHero = document.querySelector('.sig-sub > .wrap');
  if (subHero && !document.querySelector('[data-hero-drift]')) subHero.setAttribute('data-hero-drift', '');

  var px = [].slice.call(document.querySelectorAll('.parallax')).map(function(el){
    return {el: el, img: el.querySelector('img'), speed: parseFloat(el.getAttribute('data-speed')) || 40};
  }).filter(function(p){ return p.img; });
  var drifts = [].slice.call(document.querySelectorAll('[data-drift]'));
  var heroDrift = document.querySelector('[data-hero-drift]');
  if (!reduce && (px.length || drifts.length || heroDrift)){
    var ticking = false;
    var update = function(){
      var vh = window.innerHeight;
      px.forEach(function(p){
        var r = p.el.getBoundingClientRect();
        if (r.bottom < -100 || r.top > vh + 100) return;
        var k = (r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2);   // -1 … 1 across the viewport
        p.img.style.translate = '0 ' + (k * -p.speed).toFixed(1) + 'px';
      });
      drifts.forEach(function(d){
        var r = d.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        var k = (r.top + r.height / 2 - vh / 2) / vh;
        d.style.translate = (k * parseFloat(d.getAttribute('data-drift'))).toFixed(1) + 'px 0';
      });
      if (heroDrift){
        var y = Math.min(window.scrollY, vh);
        heroDrift.style.translate = '0 ' + (y * 0.22).toFixed(1) + 'px';
        heroDrift.style.opacity = Math.max(0, 1 - y / (vh * 0.95)).toFixed(3);
      }
      ticking = false;
    };
    window.addEventListener('scroll', function(){ if (!ticking){ ticking = true; requestAnimationFrame(update); } }, {passive:true});
    window.addEventListener('resize', update);
    update();
  }

  // Selected work: the section washes into the colour of the project in the middle of the screen,
  // or the one under the pointer. CSS transitions the background.
  var sw = document.querySelector('.selected-work');
  if (sw){
    var cards = [].slice.call(sw.querySelectorAll('[data-project]')), hoverCard = null, inView = null;
    var setActive = function(card){
      cards.forEach(function(c){ c.classList.toggle('is-active', c === card); });
      if (card) sw.setAttribute('data-active-project', card.getAttribute('data-project'));
      else sw.removeAttribute('data-active-project');
    };
    if ('IntersectionObserver' in window){
      var wo = new IntersectionObserver(function(es){
        es.forEach(function(e){
          if (e.isIntersecting) inView = e.target;
          else if (inView === e.target) inView = null;
        });
        if (!hoverCard) setActive(inView);
      }, {rootMargin:'-42% 0px -42% 0px'});
      cards.forEach(function(c){ wo.observe(c); });
    }
    cards.forEach(function(c){
      c.addEventListener('pointerenter', function(){ hoverCard = c; setActive(c); });
      c.addEventListener('pointerleave', function(){ hoverCard = null; setActive(inView); });
      c.addEventListener('focus', function(){ setActive(c); });
    });
  }

  // Carousels with 01 / 05 counters
  document.querySelectorAll('.carousel').forEach(function(c){
    var track = c.querySelector('.car-track'), slides = track.children, count = c.querySelector('.car-count');
    var pad = function(n){ return (n < 10 ? '0' : '') + n; };
    function current(){
      var i = Math.round(track.scrollLeft / (slides[0].getBoundingClientRect().width + 16));
      return Math.max(0, Math.min(slides.length - 1, i));
    }
    function update(){ if (count) count.textContent = pad(current() + 1) + ' / ' + pad(slides.length); }
    function go(d){
      var i = Math.max(0, Math.min(slides.length - 1, current() + d));
      track.scrollTo({left: slides[i].offsetLeft - track.offsetLeft, behavior: reduce ? 'auto' : 'smooth'});
    }
    var prev = c.querySelector('[data-prev]'), next = c.querySelector('[data-next]');
    if (prev) prev.addEventListener('click', function(){ go(-1); });
    if (next) next.addEventListener('click', function(){ go(1); });
    track.addEventListener('scroll', function(){ requestAnimationFrame(update); }, {passive:true});
    update();
  });

  // Lightbox
  var lb = document.createElement('div');
  lb.className = 'lightbox'; lb.setAttribute('role','dialog'); lb.setAttribute('aria-modal','true'); lb.setAttribute('aria-label','Expanded image');
  lb.innerHTML = '<button type="button">Close ×</button><img alt="">';
  document.body.appendChild(lb);
  var lbImg = lb.querySelector('img'), opener = null;
  function close(){
    if (!lb.classList.contains('open')) return;
    lb.classList.remove('open');
    if (opener) opener.focus();
  }
  lb.addEventListener('click', function(e){ if (e.target !== lbImg) close(); });
  document.addEventListener('keydown', function(e){
    if (e.key !== 'Escape') return;
    close();
    if (nav && nav.classList.contains('open')){ nav.classList.remove('open'); menu.setAttribute('aria-expanded', false); menu.textContent = 'Menu'; menu.focus(); }
  });
  document.querySelectorAll('[data-zoom]').forEach(function(el){
    el.setAttribute('tabindex','0');
    el.setAttribute('role','button');
    el.setAttribute('aria-label','Enlarge image: ' + (el.querySelector('img').alt || 'screen'));
    var open = function(){ opener = el; var i = el.querySelector('img'); lbImg.src = i.src; lbImg.alt = i.alt; lb.classList.add('open'); lb.querySelector('button').focus(); };
    el.addEventListener('click', open);
    el.addEventListener('keydown', function(e){ if (e.key === 'Enter') open(); });
  });

  // Case study: highlight the current chapter in "On this page"
  var links = document.querySelectorAll('.toc a');
  if (links.length && 'IntersectionObserver' in window){
    var map = {};
    links.forEach(function(a){ map[a.getAttribute('href').slice(1)] = a; });
    var so = new IntersectionObserver(function(es){
      es.forEach(function(e){
        if (e.isIntersecting){ links.forEach(function(a){ a.classList.remove('active'); }); var a = map[e.target.id]; if (a) a.classList.add('active'); }
      });
    }, {rootMargin:'-40% 0px -55% 0px'});
    Object.keys(map).forEach(function(id){ var s = document.getElementById(id); if (s) so.observe(s); });
  }

  // Copy email
  document.querySelectorAll('[data-copy]').forEach(function(b){
    b.addEventListener('click', function(){
      var t = b.getAttribute('data-copy'), label = b.textContent;
      var done = function(){ b.textContent = 'Copied'; setTimeout(function(){ b.textContent = label; }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(done, function(){});
    });
  });

  // Contact form: inline validation, then post to mail.php (which answers "success" or "error: ...")
  var form = document.getElementById('contact-form');
  if (form){
    var started = form.querySelector('[name="form_started"]');
    if (started) started.value = Date.now();
    var status = form.querySelector('.form-status'), submit = form.querySelector('[type="submit"]');
    var fields = [['f-name', function(v){ return v.trim() !== ''; }],
                  ['f-mail', function(v){ return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()); }],
                  ['f-msg',  function(v){ return v.trim() !== ''; }]];
    function check(id, test){
      var input = document.getElementById(id), ok = test(input.value), wrap = input.closest('.field');
      wrap.classList.toggle('invalid', !ok);
      input.setAttribute('aria-invalid', ok ? 'false' : 'true');
      return ok;
    }
    fields.forEach(function(f){
      document.getElementById(f[0]).addEventListener('blur', function(){ if (this.value) check(f[0], f[1]); });
    });
    form.addEventListener('submit', function(ev){
      ev.preventDefault();
      var firstBad = null;
      fields.forEach(function(f){ if (!check(f[0], f[1]) && !firstBad) firstBad = document.getElementById(f[0]); });
      if (firstBad){ firstBad.focus(); return; }
      var label = submit.innerHTML;
      submit.disabled = true; submit.textContent = 'Sending…';
      status.className = 'form-status'; status.textContent = '';
      fetch(form.getAttribute('action'), {method:'POST', body:new FormData(form)})
        .then(function(res){ return res.text(); })
        .then(function(t){
          if (t.trim() === 'success'){
            form.reset(); if (started) started.value = Date.now();
            status.className = 'form-status ok'; status.textContent = 'Thanks, your message is on its way. I’ll reply within two working days.';
          } else throw new Error(t.replace(/^error:\s*/, ''));
        })
        .catch(function(err){
          status.className = 'form-status bad';
          status.textContent = (err && err.message && err.message.length < 120 ? err.message + ' ' : '') + 'You can also email sanjulathilan12321@gmail.com.';
        })
        .then(function(){ submit.disabled = false; submit.innerHTML = label; });
    });
  }

  // Melbourne local time
  var clock = document.querySelectorAll('[data-clock]');
  function time(){
    try{
      var s = new Intl.DateTimeFormat('en-AU',{hour:'numeric',minute:'2-digit',timeZone:'Australia/Melbourne'}).format(new Date());
      clock.forEach(function(c){ c.textContent = s; });
    }catch(e){}
  }
  if (clock.length){ time(); setInterval(time, 30000); }
})();
