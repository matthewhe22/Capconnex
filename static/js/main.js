/* ============================
   Capconnex — main.js
   - Nav scroll state
   - Mobile menu toggle
   - Scroll reveal (IntersectionObserver)
   - Count-up stats
   - Contact form (Web3Forms)
   ============================ */

(function () {
  'use strict';

  // ----- Nav scroll state + active link -----
  const nav = document.querySelector('.nav');
  function onScroll() {
    if (!nav) return;
    nav.classList.toggle('scrolled', window.scrollY > 20);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // ----- Mobile menu -----
  const toggle = document.querySelector('.nav-toggle');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      nav.classList.toggle('open');
    });
    // Close on link click
    nav.querySelectorAll('.nav-link, .nav-dropdown-item').forEach((el) => {
      el.addEventListener('click', () => nav.classList.remove('open'));
    });
  }

  // ----- Active link -----
  const path = window.location.pathname.replace(/\/index\.html$/, '/').replace(/\.html$/, '') || '/';
  document.querySelectorAll('.nav-link, .nav-dropdown-item').forEach((el) => {
    const href = el.getAttribute('href') || '';
    const hrefClean = href.replace(/\/index\.html$/, '/').replace(/\.html$/, '') || '/';
    if (hrefClean === path && href !== '#') {
      el.classList.add('active');
      // Also light up parent dropdown trigger
      const dd = el.closest('.nav-dropdown');
      if (dd) dd.querySelector('.nav-dropdown-trigger')?.classList.add('active');
    }
  });

  // ----- Scroll reveal -----
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -10% 0px' });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('visible'));
  }

  // ----- Count-up stats -----
  function countUp(el, target, opts) {
    const duration = (opts && opts.duration) || 1400;
    const suffix = (opts && opts.suffix) || '';
    const prefix = (opts && opts.prefix) || '';
    const isFloat = !Number.isInteger(target);
    const start = performance.now();
    const startVal = 0;

    function frame(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // easeOutCubic
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = startVal + (target - startVal) * eased;
      const display = isFloat ? current.toFixed(1) : Math.round(current).toLocaleString();
      el.textContent = prefix + display + suffix;
      if (progress < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  function parseStatTarget(raw) {
    // Parse e.g. "$2M+" "50+" "5–32" "$0" — extract leading non-digit prefix + numeric + trailing
    const m = raw.match(/^([^\d-]*)([\d.]+)(.*)$/);
    if (!m) return null;
    return { prefix: m[1], num: parseFloat(m[2]), suffix: m[3] };
  }

  const statEls = document.querySelectorAll('[data-countup]');
  if ('IntersectionObserver' in window && statEls.length) {
    const sio = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = el.getAttribute('data-countup') || el.textContent.trim();
          const parsed = parseStatTarget(target);
          if (parsed) countUp(el, parsed.num, { prefix: parsed.prefix, suffix: parsed.suffix });
          else el.textContent = target;
          sio.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    statEls.forEach((el) => sio.observe(el));
  }

  // ----- Contact form (Web3Forms) -----
  const form = document.querySelector('#contact-form');
  if (form) {
    const status = form.querySelector('.form-status');
    const submit = form.querySelector('button[type="submit"]');
    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      if (status) { status.className = 'form-status'; status.textContent = ''; }
      if (submit) { submit.disabled = true; submit.dataset._label = submit.textContent; submit.textContent = 'Sending…'; }

      const data = new FormData(form);
      try {
        const res = await fetch('https://api.web3forms.com/submit', { method: 'POST', body: data });
        const json = await res.json();
        if (json.success) {
          if (status) { status.className = 'form-status success'; status.textContent = 'Thanks — your message is on its way. We\'ll be in touch shortly.'; }
          form.reset();
        } else {
          throw new Error(json.message || 'Submission failed');
        }
      } catch (err) {
        if (status) { status.className = 'form-status error'; status.textContent = 'Something went wrong. Please email us directly at matthew.he@capconnex.com.au.'; }
      } finally {
        if (submit) { submit.disabled = false; submit.textContent = submit.dataset._label || 'Send message'; }
      }
    });
  }

  // ----- Year in footer -----
  document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
})();
