(function () {
  var doc = document.documentElement;
  doc.classList.add('js');

  // Old single-page legal anchors (sidecarhq.cc/#terms, /#privacy) now have their own pages.
  var legacy = { '#terms': 'terms.html', '#privacy': 'privacy.html' };
  function legacyRedirect() {
    if (legacy[location.hash] && document.body.dataset.page === 'index') { location.replace(legacy[location.hash]); return true; }
    return false;
  }
  if (legacyRedirect()) return;
  window.addEventListener('hashchange', legacyRedirect);

  // Sticky nav gets a rule once the page scrolls.
  var nav = document.querySelector('.site-nav');
  function onScroll() { if (nav) nav.classList.toggle('scrolled', window.scrollY > 8); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile panel.
  var toggle = document.querySelector('.nav-toggle');
  var panel = document.getElementById('mobile-panel');
  if (toggle && panel) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      toggle.querySelector('use').setAttribute('href', 'assets/icons.svg#' + (open ? 'i-close' : 'i-menu'));
      panel.classList.toggle('open', open);
      document.body.classList.toggle('menu-open', open);
    });
    panel.addEventListener('click', function (e) {
      if (e.target.closest('a') && e.target.closest('a').getAttribute('href').charAt(0) === '#') toggle.click();
    });
  }

  // The one orchestrated moment: the data sheet builds when it enters view.
  var sheets = document.querySelectorAll('.sheet[data-build]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('built'); io.unobserve(en.target); }
      });
    }, { threshold: 0.35 });
    sheets.forEach(function (s) { io.observe(s); });
  } else {
    sheets.forEach(function (s) { s.classList.add('built'); });
  }

  // Pricing: monthly / annual.
  var billBtns = document.querySelectorAll('[data-bill]');
  billBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var mode = b.dataset.bill;
      billBtns.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      document.querySelectorAll('[data-bill-show]').forEach(function (el) {
        el.hidden = el.dataset.billShow !== mode;
      });
    });
  });


  // Inventory demo: sample messages update a sample table.
  var demo = document.querySelector('[data-invdemo]');
  if (demo) {
    var START = [
      ['tito', "Tito's Handmade 1L", 1, 6, 'Harbor'],
      ['aperol', 'Aperol 1L', 4, 5, 'Harbor'],
      ['modelo', 'Modelo Especial 1/2 bbl', 2, 2, 'Eastside'],
      ['campari', 'Campari 1L', 3, 4, 'Harbor'],
      ['jameson', 'Jameson 1L', 5, 4, 'Harbor'],
      ['lime', 'Fresh lime juice, qt', 6, 4, 'Produce']
    ];
    var items, log = demo.querySelector('.demo-log'), rows = demo.querySelector('[data-rows]');
    var updated = demo.querySelector('[data-updated]');
    var firstMsg = log.innerHTML;
    function reset() {
      items = START.map(function (r) { return { id: r[0], name: r[1], on: r[2], par: r[3], sup: r[4] }; });
      log.innerHTML = firstMsg; updated.textContent = 'Last count: Wed, 11:40 PM';
      demo.querySelectorAll('[data-say]').forEach(function (b) { b.disabled = false; });
      render([]);
    }
    function find(id) { return items.filter(function (i) { return i.id === id; })[0]; }
    function status(i) {
      if (i.on < i.par) return '<span class="chip low">Order</span>';
      if (i.on === i.par) return '<span class="chip order">Watch</span>';
      return '<span class="chip fc">OK</span>';
    }
    function render(changed) {
      rows.innerHTML = items.map(function (i) {
        var pct = Math.min(100, Math.round(i.on / i.par * 100));
        var cls = i.on < i.par ? 'warn' : (i.on === i.par ? '' : 'ok');
        return '<tr' + (changed.indexOf(i.id) > -1 ? ' class="flash"' : '') + '><td class="name">' + i.name +
          '</td><td class="r">' + i.on + '</td><td class="r">' + i.par +
          '</td><td class="hide-sm"><span class="meter ' + cls + '"><i style="width:' + pct + '%"></i></span></td><td>' + status(i) + '</td></tr>';
      }).join('');
      if (changed.length) setTimeout(function () { rows.querySelectorAll('.flash').forEach(function (r) { r.classList.remove('flash'); }); }, 900);
    }
    function add(who, html) {
      var d = document.createElement('div');
      d.className = 'turn ' + (who === 'me' ? 'me' : 'sc');
      d.innerHTML = '<span class="who">' + (who === 'me' ? 'You' : 'Sidecar') + '</span><div class="say">' + html + '</div>';
      log.appendChild(d); log.scrollTop = log.scrollHeight;
    }
    function low() { return items.filter(function (i) { return i.on < i.par; }); }
    var scripts = {
      count: ["Tito's 0.5, Aperol 2", function () {
        find('tito').on = 0.5; find('aperol').on = 2; render(['tito', 'aperol']);
        updated.textContent = 'Last count: just now';
        return "Updated 2 items. Tito's (0.5) and Aperol (2) are now below par. I'll include them in tomorrow's 7 a.m. order.";
      }],
      keg: ['Keg kicked: Modelo', function () {
        find('modelo').on = Math.max(0, find('modelo').on - 1); render(['modelo']);
        return 'Logged. Modelo is down to ' + find('modelo').on + ' half barrel on hand, par 2. Added 1 to your Eastside order.';
      }],
      receipt: ['[Photo of Harbor delivery receipt]', function () {
        find('tito').on += 6; find('campari').on += 2; render(['tito', 'campari']);
        return "Read your Harbor receipt: Tito's 1L x6, Campari 1L x2. Inventory updated.";
      }],
      order: ['What should I order this week?', function () {
        var l = low();
        if (!l.length) return "You're at or above par on everything. Nothing to order right now.";
        var lines = l.map(function (i) {
          return '<div><span>' + i.name + ' (' + i.sup + ')</span><span>' + Math.ceil(i.par - i.on) + '</span></div>';
        }).join('');
        return 'Based on your counts and pars, ' + l.length + (l.length === 1 ? ' item needs' : ' items need') +
          ' ordering:<div class="order-lines">' + lines + '</div>Reply APPROVE and I\'ll email you the orders to forward.';
      }]
    };
    demo.querySelectorAll('[data-say]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.say;
        if (k === 'reset') { reset(); return; }
        var sc = scripts[k]; if (!sc) return;
        add('me', sc[0]);
        if (k !== 'order') b.disabled = true;
        var reply = sc[1]();
        setTimeout(function () { add('sc', reply); }, 450);
      });
    });
    reset();
  }

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
