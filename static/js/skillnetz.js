/* ============================================================
   SkillNetz — interactions & animations
   ============================================================ */
(function () {
  'use strict';

  /* ---------- Navbar: glass on scroll ---------- */
  var navbar = document.querySelector('.navbar');
  var backToTop = document.querySelector('.back-to-top');
  function onScroll() {
    var y = window.scrollY || 0;
    if (navbar) navbar.classList.toggle('scrolled', y > 30);
    if (backToTop) backToTop.classList.toggle('show', y > 500);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile menu ---------- */
  var navToggle = document.querySelector('.nav-toggle');
  var navLinks = document.querySelector('.nav-links');
  var navOverlay = document.querySelector('.nav-overlay');
  function closeMenu() {
    if (navLinks) navLinks.classList.remove('open');
    if (navOverlay) navOverlay.classList.remove('show');
    document.body.style.overflow = '';
  }
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      var open = navLinks.classList.toggle('open');
      if (navOverlay) navOverlay.classList.toggle('show', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }
  if (navOverlay) navOverlay.addEventListener('click', closeMenu);
  if (navLinks) {
    navLinks.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', closeMenu);
    });
  }

  /* ---------- User dropdown ---------- */
  var navUser = document.querySelector('.nav-user');
  if (navUser) {
    navUser.querySelector('.nav-user-btn').addEventListener('click', function (e) {
      e.stopPropagation();
      navUser.classList.toggle('open');
    });
    document.addEventListener('click', function () {
      navUser.classList.remove('open');
    });
  }

  /* ---------- Back to top ---------- */
  if (backToTop) {
    backToTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- Scroll reveal ---------- */
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('in');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- Animated counters ---------- */
  var counters = document.querySelectorAll('[data-count]');
  function animateCounter(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var suffix = el.getAttribute('data-suffix') || '';
    var decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
    var dur = 1800;
    var start = null;
    function tick(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      var val = target * eased;
      el.textContent = (decimals ? val.toFixed(decimals) : Math.round(val).toLocaleString()) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  if ('IntersectionObserver' in window && counters.length) {
    var cio = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            cio.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach(function (el) { cio.observe(el); });
  } else {
    counters.forEach(animateCounter);
  }

  /* ---------- Hero slideshow ---------- */
  var slides = document.querySelectorAll('.hero-frame .slide');
  var dots = document.querySelectorAll('.hero-frame .slide-dots span');
  if (slides.length > 1) {
    var current = 0;
    var timer = null;
    function goTo(idx) {
      slides.forEach(function (s, i) { s.classList.toggle('active', i === idx); });
      dots.forEach(function (d, i) { d.classList.toggle('active', i === idx); });
      current = idx;
    }
    function next() { goTo((current + 1) % slides.length); }
    function start() { timer = setInterval(next, 4200); }
    function stop() { clearInterval(timer); }
    dots.forEach(function (d, i) {
      d.addEventListener('click', function () { stop(); goTo(i); start(); });
    });
    start();
    var frame = document.querySelector('.hero-frame');
    if (frame) {
      frame.addEventListener('mouseenter', stop);
      frame.addEventListener('mouseleave', start);
    }
  }

  /* ---------- Typing rotator ---------- */
  var typeEl = document.querySelector('[data-type-words]');
  if (typeEl) {
    var words = JSON.parse(typeEl.getAttribute('data-type-words'));
    var wi = 0, ci = 0, deleting = false;
    (function type() {
      var word = words[wi];
      typeEl.textContent = word.slice(0, ci);
      if (!deleting && ci < word.length) {
        ci++;
        setTimeout(type, 75);
      } else if (!deleting) {
        deleting = true;
        setTimeout(type, 1700);
      } else if (ci > 0) {
        ci--;
        setTimeout(type, 38);
      } else {
        deleting = false;
        wi = (wi + 1) % words.length;
        setTimeout(type, 350);
      }
    })();
  }

  /* ---------- Testimonial slider ---------- */
  var testiTrack = document.querySelector('.testi-track');
  if (testiTrack) {
    var cards = testiTrack.querySelectorAll('.testi-card');
    var prevBtn = document.querySelector('.testi-nav .t-prev');
    var nextBtn = document.querySelector('.testi-nav .t-next');
    var idx = 0;
    function perView() {
      var w = window.innerWidth;
      if (w <= 640) return 1;
      if (w <= 1024) return 2;
      return 3;
    }
    function maxIdx() { return Math.max(0, cards.length - perView()); }
    function render() {
      if (idx > maxIdx()) idx = 0;
      var cardW = cards[0].getBoundingClientRect().width + 25.6;
      testiTrack.style.transform = 'translateX(-' + idx * cardW + 'px)';
    }
    if (prevBtn) prevBtn.addEventListener('click', function () { idx = idx <= 0 ? maxIdx() : idx - 1; render(); });
    if (nextBtn) nextBtn.addEventListener('click', function () { idx = idx >= maxIdx() ? 0 : idx + 1; render(); });
    window.addEventListener('resize', render);
    render();
    setInterval(function () { idx = idx >= maxIdx() ? 0 : idx + 1; render(); }, 5000);
  }

  /* ---------- FAQ accordion ---------- */
  document.querySelectorAll('.faq-item').forEach(function (item) {
    var q = item.querySelector('.faq-q');
    var a = item.querySelector('.faq-a');
    if (!q || !a) return;
    q.addEventListener('click', function () {
      var isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(function (other) {
        other.classList.remove('open');
        other.querySelector('.faq-a').style.maxHeight = null;
      });
      if (!isOpen) {
        item.classList.add('open');
        a.style.maxHeight = a.scrollHeight + 'px';
      }
    });
  });

  /* ---------- Footer feedback stars ---------- */
  var starBox = document.querySelector('.footer-feedback .stars');
  var ratingInput = document.getElementById('feedback-rating');
  if (starBox && ratingInput) {
    var stars = Array.prototype.slice.call(starBox.children);
    function paint(n, cls) {
      stars.forEach(function (s, i) { s.classList.toggle(cls, i < n); });
    }
    stars.forEach(function (star, i) {
      var n = i + 1;
      star.addEventListener('mouseenter', function () { paint(n, 'hovered'); });
      star.addEventListener('mouseleave', function () { paint(0, 'hovered'); });
      star.addEventListener('click', function () {
        ratingInput.value = n;
        paint(n, 'selected');
        showToast('Thanks! Rating ' + n + ' star' + (n > 1 ? 's' : '') + ' selected.');
      });
    });
  }

  /* ---------- Toast helper ---------- */
  var toastEl = null;
  window.showToast = function (msg) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'toast';
      toastEl.innerHTML = '<i class="bx bx-check-circle"></i><span></span>';
      document.body.appendChild(toastEl);
    }
    toastEl.querySelector('span').textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastEl._t);
    toastEl._t = setTimeout(function () { toastEl.classList.remove('show'); }, 2800);
  };

  /* ---------- Skill pills (signup / post job) ---------- */
  window.initSkillPills = function (container, hiddenInput) {
    var pills = container.querySelectorAll('.skill-pill');
    var selected = [];
    pills.forEach(function (pill) {
      pill.addEventListener('click', function () {
        var name = pill.getAttribute('data-skill');
        var pos = selected.indexOf(name);
        if (pos === -1) { selected.push(name); pill.classList.add('selected'); }
        else { selected.splice(pos, 1); pill.classList.remove('selected'); }
        if (hiddenInput) hiddenInput.value = selected.join(',');
      });
    });
  };

  /* ---------- Image upload preview ---------- */
  window.initUploadPreview = function (inputEl, boxEl) {
    if (!inputEl || !boxEl) return;
    inputEl.addEventListener('change', function () {
      var file = inputEl.files && inputEl.files[0];
      if (!file) return;
      if (!/^image\//.test(file.type)) return;
      var reader = new FileReader();
      reader.onload = function (e) {
        boxEl.querySelector('img').src = e.target.result;
        boxEl.classList.add('has-image');
      };
      reader.readAsDataURL(file);
    });
    ['dragenter', 'dragover'].forEach(function (ev) {
      boxEl.addEventListener(ev, function (e) { e.preventDefault(); boxEl.classList.add('drag'); });
    });
    ['dragleave', 'drop'].forEach(function (ev) {
      boxEl.addEventListener(ev, function (e) { e.preventDefault(); boxEl.classList.remove('drag'); });
    });
    boxEl.addEventListener('drop', function (e) {
      if (e.dataTransfer.files.length) {
        inputEl.files = e.dataTransfer.files;
        inputEl.dispatchEvent(new Event('change'));
      }
    });
  };

  /* ---------- Budget range fill ---------- */
  var budget = document.getElementById('budget-range');
  var budgetValue = document.getElementById('budget-value');
  if (budget && budgetValue) {
    var min = parseFloat(budget.min) || 0;
    var max = parseFloat(budget.max) || 100;
    function updateBudget() {
      var pct = ((budget.value - min) / (max - min)) * 100;
      budget.style.setProperty('--fill', pct + '%');
      budgetValue.textContent = '₹' + parseInt(budget.value, 10).toLocaleString('en-IN');
    }
    budget.addEventListener('input', updateBudget);
    updateBudget();
  }
})();
