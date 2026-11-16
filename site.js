/* Ocmand Construction Co., LLC — site behavior */
(function () {
  var d = document, root = d.documentElement;
  if (!('startViewTransition' in d)) root.classList.add('no-vt');

  /* header: shrink on scroll, mobile menu */
  var header = d.querySelector('.site-header');
  var onScroll = function () { header.classList.toggle('is-stuck', window.scrollY > 24); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  var burger = d.querySelector('.burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = d.body.classList.toggle('nav-open');
      burger.setAttribute('aria-expanded', open);
    });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && d.body.classList.contains('nav-open')) { d.body.classList.remove('nav-open'); burger.setAttribute('aria-expanded', false); burger.focus(); }
    });
  }

  /* footer year */
  var yr = d.querySelector('[data-year]'); if (yr) yr.textContent = new Date().getFullYear();

  /* quiet reveal, once */
  var items = [].slice.call(d.querySelectorAll('[data-reveal]'));
  if ('IntersectionObserver' in window && items.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add('is-in'); }); }

  /* projects: filter + viewer */
  var grid = d.querySelector('[data-projects]');
  if (grid) {
    var shots = [].slice.call(grid.querySelectorAll('.shot'));
    var buttons = [].slice.call(d.querySelectorAll('.filter button'));
    buttons.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-filter');
        buttons.forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
        shots.forEach(function (s) {
          var show = f === 'all' || s.getAttribute('data-cat') === f;
          s.hidden = !show; s.classList.remove('is-in');
          if (show) { void s.offsetWidth; s.classList.add('is-in'); }
        });
      });
    });
    var lb = d.querySelector('dialog.lb');
    if (lb && lb.showModal) {
      var img = lb.querySelector('img'), count = lb.querySelector('[data-count]');
      var fName = lb.querySelector('[data-name]'), fLoc = lb.querySelector('[data-loc]'), fType = lb.querySelector('[data-type]');
      var cur = 0;
      var visible = function () { return shots.filter(function (s) { return !s.hidden; }); };
      var show = function (i) {
        var v = visible(); cur = (i + v.length) % v.length; var s = v[cur];
        img.src = s.getAttribute('data-full'); img.alt = s.querySelector('img').alt;
        fName.textContent = s.getAttribute('data-name'); fLoc.textContent = s.getAttribute('data-loc'); fType.textContent = s.getAttribute('data-type');
        count.textContent = (cur + 1) + ' of ' + v.length;
      };
      shots.forEach(function (s) { s.addEventListener('click', function () { show(visible().indexOf(s)); lb.showModal(); }); });
      lb.querySelector('[data-close]').addEventListener('click', function () { lb.close(); });
      lb.querySelector('[data-prev]').addEventListener('click', function () { show(cur - 1); });
      lb.querySelector('[data-next]').addEventListener('click', function () { show(cur + 1); });
      lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb-stage')) lb.close(); });
      lb.addEventListener('keydown', function (e) { if (e.key === 'ArrowLeft') show(cur - 1); if (e.key === 'ArrowRight') show(cur + 1); });
    }
  }

  /* hero: slow drift on scroll */
  var hb = d.querySelector('.hero-bg');
  if (hb && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var tick = false;
    window.addEventListener('scroll', function () {
      if (tick) return; tick = true;
      requestAnimationFrame(function () { var y = window.scrollY; if (y < 1200) hb.style.transform = 'translate3d(0,' + (y * 0.14).toFixed(1) + 'px,0)'; tick = false; });
    }, { passive: true });
  }

  /* bid request and subcontractor forms */
  [].slice.call(d.querySelectorAll('form[data-bid]')).forEach(function (form) {
    var status = form.querySelector('.form-status'), btn = form.querySelector('button[type=submit]');
    var kind = form.getAttribute('data-kind');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = function (n) { return form.elements[n] ? (form.elements[n].value || '').trim() : ''; };
      if (v('website')) return;
      if (!v('name') || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v('email'))) { status.className = 'form-status err'; status.textContent = 'Add your name and a working email address so we can reply.'; return; }
      status.className = 'form-status'; status.textContent = 'Sending.'; btn.disabled = true;
      var data = { access_key: '7ebf5b2b-bfba-48a3-a382-c277ca3a5970', from_name: 'Ocmand website', name: v('name'), company: v('company'), email: v('email'), replyto: v('email') };
      if (kind) {
        data.subject = kind + ': ' + (v('type') || 'trade not given') + (v('company') ? ' / ' + v('company') : '');
        data.trade = v('type'); data.area_covered = v('location'); data.license_number = v('timeline');
      } else {
        data.subject = 'Bid request: ' + (v('type') || 'project') + (v('company') ? ' / ' + v('company') : '');
        data.project_type = v('type'); data.location = v('location'); data.timeline = v('timeline'); data.drawings = v('drawings'); data.details = v('details');
      }
      fetch('https://api.web3forms.com/submit', {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data)
      }).then(function (r) { return r.json(); }).then(function (res) {
        btn.disabled = false;
        if (res && res.success) { form.reset(); status.className = 'form-status ok'; status.textContent = kind ? 'Received. We will add you to our bid list.' : 'Request sent. We will reply by email within one business day.'; }
        else { throw new Error('send failed'); }
      }).catch(function () {
        btn.disabled = false; status.className = 'form-status err';
        status.textContent = 'This did not send. Email us directly at jobs@ocmandconstruction.com.';
      });
    });
  });
})();
