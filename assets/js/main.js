/* ==========================================================================
   POI – Power of Interest UK | Global JavaScript (v3)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {
  // === 1. SCROLL REVEAL ANIMATIONS (INTERSECTION OBSERVER) ===
  const reveals = document.querySelectorAll('.reveal');
  
  if ('IntersectionObserver' in window && reveals.length > 0) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      threshold: 0.05,
      rootMargin: '0px 0px -20px 0px'
    });

    reveals.forEach(el => revealObserver.observe(el));
  } else {
    // Fallback if IntersectionObserver is not supported
    reveals.forEach(el => el.classList.add('visible'));
  }

  // === 2. MOBILE NAVIGATION MENU ===
  const hamburger = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobile-nav');
  
  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', function () {
      const isOpen = hamburger.classList.toggle('open');
      mobileNav.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', isOpen);
    });

    // Close mobile nav when clicking a link
    mobileNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', function () {
        hamburger.classList.remove('open');
        mobileNav.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
      });
    });

    // Close mobile nav when clicking outside
    document.addEventListener('click', function (e) {
      if (!hamburger.contains(e.target) && !mobileNav.contains(e.target)) {
        hamburger.classList.remove('open');
        mobileNav.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // === 3. HEADER SCROLL & READING PROGRESS BAR & BACK TO TOP ===
  const header = document.querySelector('.site-header');

  // Dynamically inject top progress bar
  let progressBar = document.querySelector('.scroll-progress-bar');
  if (!progressBar) {
    progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress-bar';
    document.body.appendChild(progressBar);
  }

  // Dynamically inject back-to-top button
  let backToTop = document.querySelector('.back-to-top');
  if (!backToTop) {
    backToTop = document.createElement('button');
    backToTop.className = 'back-to-top';
    backToTop.setAttribute('aria-label', 'Back to top');
    backToTop.innerHTML = '&uarr;';
    document.body.appendChild(backToTop);

    backToTop.addEventListener('click', function () {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  const handleScrollEffects = () => {
    const scrollY = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;

    // 1. Update Header Glassmorphism
    if (header) {
      if (scrollY > 40) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    }

    // 2. Update Progress Bar
    if (progressBar && docHeight > 0) {
      const scrollPercent = Math.min(Math.max((scrollY / docHeight) * 100, 0), 100);
      progressBar.style.width = scrollPercent + '%';
    }

    // 3. Update Back To Top Visibility
    if (backToTop) {
      if (scrollY > 350) {
        backToTop.classList.add('visible');
      } else {
        backToTop.classList.remove('visible');
      }
    }
  };

  window.addEventListener('scroll', handleScrollEffects, { passive: true });
  handleScrollEffects();

  // === 4. ACCORDION COMPONENT (FAQ Page) ===
  const accordions = document.querySelectorAll('.accordion-item');
  
  accordions.forEach(item => {
    const trigger = item.querySelector('.accordion-trigger');
    const content = item.querySelector('.accordion-content');
    
    if (trigger && content) {
      trigger.addEventListener('click', function () {
        const isActive = item.classList.contains('active');
        
        // Close other accordions in the same container
        const parent = item.parentElement;
        if (parent) {
          parent.querySelectorAll('.accordion-item.active').forEach(openItem => {
            if (openItem !== item) {
              openItem.classList.remove('active');
              openItem.querySelector('.accordion-content').style.maxHeight = null;
              const t = openItem.querySelector('.accordion-trigger');
              if (t) t.setAttribute('aria-expanded', 'false');
            }
          });
        }
        
        // Toggle current
        if (isActive) {
          item.classList.remove('active');
          content.style.maxHeight = null;
          trigger.setAttribute('aria-expanded', 'false');
        } else {
          item.classList.add('active');
          content.style.maxHeight = content.scrollHeight + 'px';
          trigger.setAttribute('aria-expanded', 'true');
        }
      });
    }
  });

  // Open accordion by URL hash (e.g. faq.html#bp-debate)
  function handleAccordionHash() {
    const hash = window.location.hash;
    if (hash) {
      const targetItem = document.querySelector(hash);
      if (targetItem && targetItem.classList.contains('accordion-item')) {
        const content = targetItem.querySelector('.accordion-content');
        if (content) {
          // Close others in same accordion
          const parent = targetItem.parentElement;
          if (parent) {
            parent.querySelectorAll('.accordion-item.active').forEach(openItem => {
              if (openItem !== targetItem) {
                openItem.classList.remove('active');
                openItem.querySelector('.accordion-content').style.maxHeight = null;
              }
            });
          }
          targetItem.classList.add('active');
          content.style.maxHeight = content.scrollHeight + 'px';

          setTimeout(() => {
            targetItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }, 200);
        }
      }
    }
  }

  handleAccordionHash();
  window.addEventListener('hashchange', handleAccordionHash);

  // === 5. CLOSED ROLES TOGGLE (Volunteering Page) ===
  const closedToggle = document.getElementById('closed-roles-toggle');
  const closedContainer = document.getElementById('closed-roles-container');
  const closedArrow = document.getElementById('closed-roles-arrow');

  if (closedToggle && closedContainer) {
    closedToggle.addEventListener('click', function () {
      const isExpanded = closedContainer.style.maxHeight && closedContainer.style.maxHeight !== '0px';
      if (isExpanded) {
        closedContainer.style.maxHeight = '0px';
        closedContainer.style.opacity = '0';
        if (closedArrow) closedArrow.style.transform = 'rotate(0deg)';
      } else {
        closedContainer.style.maxHeight = closedContainer.scrollHeight + 150 + 'px';
        closedContainer.style.opacity = '1';
        if (closedArrow) closedArrow.style.transform = 'rotate(180deg)';
      }
    });
  }

  // === 6. ADAPTIVE LIGHT / DARK MODE ENGINE ===
  const themeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

  function getCurrentTheme() {
    const savedTheme = localStorage.getItem('poi-theme');
    if (savedTheme === 'light' || savedTheme === 'dark') {
      return savedTheme;
    }
    return themeMediaQuery.matches ? 'dark' : 'light';
  }

  function applyTheme(theme, save = false) {
    if (theme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
      document.documentElement.style.colorScheme = 'dark';
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
      document.documentElement.style.colorScheme = 'light';
    }
    if (save) {
      localStorage.setItem('poi-theme', theme);
    }
    updateToggleIcons(theme);
  }

  function updateToggleIcons(theme) {
    const iconHtml = theme === 'dark'
      ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
      : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    const ariaLabel = theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
    
    document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
      btn.innerHTML = iconHtml;
      btn.setAttribute('aria-label', ariaLabel);
      btn.setAttribute('title', ariaLabel);
    });

    document.querySelectorAll('.theme-toggle-mobile').forEach(btn => {
      const label = theme === 'dark' ? 'Dark' : 'Light';
      btn.innerHTML = `<span>Theme</span><span>${iconHtml} ${label}</span>`;
    });
  }

  // Initialize theme on load
  const initialTheme = getCurrentTheme();
  applyTheme(initialTheme, false);

  // Desktop header theme toggle
  document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || getCurrentTheme();
      applyTheme(current === 'dark' ? 'light' : 'dark', true);
    });
  });

  // Listen to OS-level theme changes dynamically
  themeMediaQuery.addEventListener('change', (e) => {
    // Only adapt automatically if the user hasn't explicitly saved a preference
    if (!localStorage.getItem('poi-theme')) {
      applyTheme(e.matches ? 'dark' : 'light', false);
    }
  });

  // Inject Theme Toggle into Mobile Nav
  const mobileNavContainer = document.querySelector('.mobile-nav');
  if (mobileNavContainer && !document.querySelector('.theme-toggle-mobile')) {
    const mobileToggleBtn = document.createElement('button');
    mobileToggleBtn.type = 'button';
    mobileToggleBtn.className = 'theme-toggle-mobile';
    const mobileIcon = initialTheme === 'dark'
      ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
      : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    mobileToggleBtn.innerHTML = `<span>Theme</span><span>${mobileIcon} ${initialTheme === 'dark' ? 'Dark' : 'Light'}</span>`;

    mobileToggleBtn.addEventListener('click', (e) => {
      // Keep the dropdown open: the icon is re-rendered on theme change, which would
      // otherwise make the outside-click handler think the click was outside the menu.
      e.stopPropagation();
      const current = document.documentElement.getAttribute('data-theme') || getCurrentTheme();
      const nextTheme = current === 'dark' ? 'light' : 'dark';
      applyTheme(nextTheme, true);
    });

    const mobileActions = mobileNavContainer.querySelector('.mobile-nav-actions');
    mobileNavContainer.insertBefore(mobileToggleBtn, mobileActions);
  }

  // Nav Dropdown Menu Interaction (Touch, Click & Keyboard Accessibility)
  document.querySelectorAll('.nav-dropdown').forEach(dropdown => {
    const btn = dropdown.querySelector('.nav-dropdown-btn');
    if (!btn) return;

    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = dropdown.classList.toggle('open');
      btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  });

  // Close dropdown when clicking outside
  document.addEventListener('click', (e) => {
    document.querySelectorAll('.nav-dropdown.open').forEach(dropdown => {
      if (!dropdown.contains(e.target)) {
        dropdown.classList.remove('open');
        const btn = dropdown.querySelector('.nav-dropdown-btn');
        if (btn) btn.setAttribute('aria-expanded', 'false');
      }
    });
  });

  // Close dropdown on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.nav-dropdown.open').forEach(dropdown => {
        dropdown.classList.remove('open');
        const btn = dropdown.querySelector('.nav-dropdown-btn');
        if (btn) {
          btn.setAttribute('aria-expanded', 'false');
          btn.focus();
        }
      });
    }
  });

  // === 5. SITE-WIDE ASSET & PHOTO PROTECTION ===
  // Disable right-click on photos and protected materials
  document.addEventListener('contextmenu', function (e) {
    // Allow unrestricted elements and open unrestricted modal (Motion Guide)
    const activeModal = document.getElementById('resource-viewer-modal');
    if (activeModal && activeModal.classList.contains('viewer-unrestricted')) {
      return true;
    }
    if (e.target.closest('[data-viewer-unrestricted="true"]') || e.target.closest('.resource-action-group')) {
      return true;
    }

    if (
      e.target.closest('img') ||
      e.target.closest('.header-logo') ||
      e.target.closest('.footer-logo') ||
      e.target.closest('#pw-protected') ||
      e.target.closest('#resource-viewer-modal')
    ) {
      e.preventDefault();
      return false;
    }
  });

  // Disable dragging photos
  document.addEventListener('dragstart', function (e) {
    if (e.target.closest('img')) {
      e.preventDefault();
      return false;
    }
  });

  // Block Print & Save Shortcuts (Cmd/Ctrl + P, Cmd/Ctrl + S, PrintScreen)
  window.addEventListener('keydown', function (e) {
    // Allow printing and saving if unrestricted modal (Motion Guide) is open
    const activeModal = document.getElementById('resource-viewer-modal');
    if (activeModal && activeModal.classList.contains('viewer-unrestricted')) {
      return true;
    }

    const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
    const modKey = isMac ? e.metaKey : e.ctrlKey;

    // Block Print
    if (modKey && (e.key === 'p' || e.key === 'P')) {
      e.preventDefault();
      return false;
    }

    // Block Save page
    if (modKey && (e.key === 's' || e.key === 'S')) {
      e.preventDefault();
      return false;
    }

    // Clear clipboard on PrintScreen key (Windows)
    if (e.key === 'PrintScreen' || e.keyCode === 44) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText('');
      }
    }
  });

  // === 6. COPY DONATION LINK HANDLER ===
  const copyBtn = document.getElementById('copy-donate-btn');
  const copyInput = document.getElementById('share-donate-input');
  if (copyBtn && copyInput) {
    copyBtn.addEventListener('click', function () {
      const textToCopy = copyInput.value || 'https://www.zeffy.com/en-GB/donation-form/your-words-your-way';
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(textToCopy).then(() => {
          const original = copyBtn.textContent;
          copyBtn.textContent = 'Copied! ✓';
          setTimeout(() => { copyBtn.textContent = original; }, 2500);
        });
      } else {
        copyInput.select();
        document.execCommand('copy');
        const original = copyBtn.textContent;
        copyBtn.textContent = 'Copied! ✓';
        setTimeout(() => { copyBtn.textContent = original; }, 2500);
      }
    });
  }

  // === 7. SIDE MENU: HIGHLIGHT THE SECTION BEING READ (FAQ & Policies) ===
  const asideLinks = Array.from(document.querySelectorAll('.aside-nav a[href^="#"]'));
  if (asideLinks.length && 'IntersectionObserver' in window) {
    const targets = asideLinks
      .map(link => document.querySelector(link.getAttribute('href')))
      .filter(Boolean);
    const setActive = (id) => {
      asideLinks.forEach(link => {
        const on = link.getAttribute('href') === '#' + id;
        link.classList.toggle('active', on);
        if (on) link.setAttribute('aria-current', 'true'); else link.removeAttribute('aria-current');
      });
    };
    const sectionObserver = new IntersectionObserver((entries) => {
      const visible = entries.filter(e => e.isIntersecting)
        .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (visible.length) setActive(visible[0].target.id);
    }, { rootMargin: '-20% 0px -60% 0px', threshold: 0 });
    targets.forEach(t => sectionObserver.observe(t));
  }

  // === 8. LOCAL TIME CONVERTER (UK session times shown in the visitor's own time zone) ===
  const UK_TZ = 'Europe/London';

  function zoneParts(date, timeZone) {
    const parts = new Intl.DateTimeFormat('en-GB', {
      timeZone, hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', second: '2-digit'
    }).formatToParts(date);
    const get = (type) => Number(parts.find(p => p.type === type).value);
    return { y: get('year'), m: get('month'), d: get('day'), h: get('hour'), mi: get('minute'), s: get('second') };
  }

  // minutes that a time zone is ahead of UTC at a given instant
  function zoneOffset(date, timeZone) {
    const p = zoneParts(date, timeZone);
    return (Date.UTC(p.y, p.m - 1, p.d, p.h, p.mi, p.s) - Math.floor(date.getTime() / 1000) * 1000) / 60000;
  }

  // next instant when it is weekday/hh:mm in the UK (0 = Sunday)
  function nextUkTime(weekday, hh, mm, after) {
    const today = zoneParts(after, UK_TZ);
    for (let i = 0; i < 8; i++) {
      const day = new Date(Date.UTC(today.y, today.m - 1, today.d + i));
      if (day.getUTCDay() !== weekday) continue;
      const guess = Date.UTC(day.getUTCFullYear(), day.getUTCMonth(), day.getUTCDate(), hh, mm);
      const instant = new Date(guess - zoneOffset(new Date(guess), UK_TZ) * 60000);
      if (instant.getTime() > after.getTime()) return instant;
    }
    return null;
  }

  try {
    const localTz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
    const place = localTz.includes('/') ? localTz.split('/').pop().replace(/_/g, ' ') : 'your area';
    const fmtTime = (d) => d.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
    const fmtDay = (d) => d.toLocaleDateString([], { weekday: 'long' });

    document.querySelectorAll('.local-time[data-uk-start]').forEach(el => {
      const [sh, sm] = el.dataset.ukStart.split(':').map(Number);
      const [eh, em] = (el.dataset.ukEnd || el.dataset.ukStart).split(':').map(Number);
      const weekday = Number(el.dataset.weekday || 0);
      const start = nextUkTime(weekday, sh, sm, new Date());
      if (!start) return;
      const end = new Date(start.getTime() + ((eh * 60 + em) - (sh * 60 + sm)) * 60000);
      // same clock time as the UK? nothing to convert
      if (zoneOffset(start, UK_TZ) === -start.getTimezoneOffset()) return;
      el.textContent = `That's ${fmtTime(start)}–${fmtTime(end)} on ${fmtDay(start)} in ${place}`;
      el.hidden = false;
      const row = el.closest('.local-time-row');
      if (row) row.hidden = false;
    });
  } catch (err) { /* older browsers: UK time is still shown */ }

  // === 9. FORMS: send without leaving the page (Formspree) ===
  document.querySelectorAll('form[data-ajax]').forEach(form => {
    const wrap = form.closest('[data-form-wrap]') || form.parentElement;
    const success = wrap ? wrap.querySelector('.form-success') : null;
    const errorEl = form.querySelector('.form-error');
    const submitBtn = form.querySelector('[type="submit"]');

    const showError = (msg) => {
      if (!errorEl) return;
      errorEl.textContent = msg;
      errorEl.hidden = false;
    };

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (errorEl) errorEl.hidden = true;

      for (const group of form.querySelectorAll('[data-require-one]')) {
        if (!group.querySelector('input:checked')) {
          showError(group.dataset.requireOne);
          const first = group.querySelector('input');
          if (first) first.focus();
          return;
        }
      }

      const original = submitBtn ? submitBtn.innerHTML : '';
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Sending…'; }
      try {
        const res = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { Accept: 'application/json' }
        });
        if (!res.ok) throw new Error('Request failed');
        form.hidden = true;
        if (success) { success.hidden = false; success.focus(); }
      } catch (err) {
        showError('Sorry, that didn’t send. Please try again, or email contact@poi.org.uk.');
        if (submitBtn) { submitBtn.disabled = false; submitBtn.innerHTML = original; }
      }
    });
  });

  // === 10. SIGN-UP FORM: time zone + parent/guardian details for under-13s ===
  const signup = document.getElementById('signup-form');
  if (signup) {
    try {
      const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
      const tzInput = document.getElementById('signup-tz');
      const tzOut = signup.querySelector('[data-tz-out]');
      if (tz && tzInput) {
        tzInput.value = tz;
        if (tzOut) { tzOut.textContent = tz.replace(/_/g, ' '); tzOut.closest('.form-tz').hidden = false; }
      }
    } catch (err) { /* optional */ }

    const age = document.getElementById('signup-age');
    const box = document.getElementById('guardian-fields');
    const status = document.getElementById('guardian-status');
    const hint = document.getElementById('guardian-hint');
    const consent = document.getElementById('guardian-consent');
    const guardianInputs = [document.getElementById('signup-parent-name'), document.getElementById('signup-parent-email')];
    const UNDER_13 = ['Under 11', '11', '12'];

    const updateGuardian = () => {
      const needed = UNDER_13.includes(age.value);
      guardianInputs.forEach(inp => { if (inp) inp.required = needed; });
      if (consent) {
        consent.hidden = !needed;
        const cb = consent.querySelector('input');
        if (cb) { cb.required = needed; if (!needed) cb.checked = false; }
      }
      if (box) box.classList.toggle('is-required', needed);
      if (hint) hint.hidden = !needed;
      if (status) { status.textContent = needed ? 'required' : 'optional'; status.classList.toggle('is-required', needed); }
    };
    if (age) { age.addEventListener('change', updateGuardian); updateGuardian(); }
  }

  // Buttons like "Sign Up Free" or "Apply as Judge" pre-tick the matching option in their form
  document.querySelectorAll('[data-pick-for][data-pick]').forEach(link => {
    link.addEventListener('click', () => {
      const target = document.getElementById(link.dataset.pickFor);
      const cb = target ? target.querySelector(`input[data-pick="${link.dataset.pick}"]`) : null;
      if (cb) cb.checked = true;
    });
  });

  // Any form with a [data-tz-field] input records the visitor's time zone
  try {
    const tzName = Intl.DateTimeFormat().resolvedOptions().timeZone;
    if (tzName) document.querySelectorAll('input[data-tz-field]').forEach(inp => { inp.value = tzName; });
  } catch (err) { /* optional */ }

  // === 11. MOTION BANK: search, topic filter, random motion & 15-minute prep timer ===
  const motionGrid = document.getElementById('motion-grid');
  if (motionGrid) {
    const cards = Array.from(motionGrid.querySelectorAll('.motion-card'));
    const search = document.getElementById('motion-search');
    const chips = Array.from(document.querySelectorAll('.chip[data-topic]'));
    const countEl = document.getElementById('motion-count');
    const emptyEl = document.getElementById('motion-empty');
    let topic = 'all';

    const applyFilter = () => {
      const q = (search ? search.value : '').trim();
      const re = q ? new RegExp('\\b' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i') : null;
      let shown = 0;
      cards.forEach(card => {
        const matchTopic = topic === 'all' || card.dataset.topics.split(' ').includes(topic);
        const haystack = card.querySelector('.motion-text').textContent + ' ' + card.querySelector('.motion-topics').textContent;
        const matchText = !re || re.test(haystack);
        card.hidden = !(matchTopic && matchText);
        if (!card.hidden) shown++;
      });
      if (countEl) countEl.textContent = `Showing ${shown} of ${cards.length} motions`;
      if (emptyEl) emptyEl.hidden = shown !== 0;
    };
    if (search) search.addEventListener('input', applyFilter);
    chips.forEach(chip => chip.addEventListener('click', () => {
      topic = chip.dataset.topic;
      chips.forEach(c => { const on = c === chip; c.classList.toggle('active', on); c.setAttribute('aria-pressed', on ? 'true' : 'false'); });
      applyFilter();
    }));
    applyFilter();

    // prep timer
    const PREP = 15 * 60;
    let remaining = PREP;
    let tick = null;
    const display = document.getElementById('timer-display');
    const statusEl = document.getElementById('timer-status');
    const toggle = document.getElementById('timer-toggle');
    const reset = document.getElementById('timer-reset');
    const practiceText = document.getElementById('practice-motion');
    const panel = document.getElementById('practice');

    const render = () => {
      const m = Math.floor(remaining / 60), s = remaining % 60;
      display.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
      display.classList.toggle('is-low', remaining <= 60);
    };
    const stop = () => { clearInterval(tick); tick = null; toggle.textContent = remaining === PREP ? 'Start timer' : 'Resume'; };
    const start = () => {
      if (remaining <= 0) remaining = PREP;
      statusEl.textContent = '';
      toggle.textContent = 'Pause';
      tick = setInterval(() => {
        remaining--;
        render();
        if (remaining === 60) statusEl.textContent = 'One minute left!';
        if (remaining <= 0) { stop(); toggle.textContent = 'Start again'; statusEl.textContent = 'Time’s up — to the dispatch box!'; }
      }, 1000);
    };
    const resetTimer = () => { stop(); remaining = PREP; render(); statusEl.textContent = ''; toggle.textContent = 'Start timer'; };

    if (toggle) toggle.addEventListener('click', () => (tick ? stop() : start()));
    if (reset) reset.addEventListener('click', resetTimer);

    const pick = (card) => {
      cards.forEach(c => c.classList.remove('is-picked'));
      card.classList.add('is-picked');
      practiceText.textContent = card.querySelector('.motion-text').textContent.trim();
      practiceText.classList.add('is-set');
      resetTimer();
      panel.scrollIntoView({ behavior: 'smooth', block: 'center' });
    };
    const randomBtn = document.getElementById('random-motion');
    if (randomBtn) randomBtn.addEventListener('click', () => {
      const pool = cards.filter(c => !c.hidden);
      const list = pool.length ? pool : cards;
      let choice = list[Math.floor(Math.random() * list.length)];
      if (list.length > 1 && choice.classList.contains('is-picked')) {
        choice = list[(list.indexOf(choice) + 1) % list.length];
      }
      pick(choice);
    });
    cards.forEach(card => {
      const btn = card.querySelector('.motion-practise');
      if (btn) btn.addEventListener('click', () => pick(card));
    });
    render();
  }

  // === 12. PRIVACY-FRIENDLY VISITOR STATISTICS (GoatCounter, no cookies) ===
  // Paste your GoatCounter code here (e.g. 'poi' for https://poi.goatcounter.com) to switch it on.
  const GOATCOUNTER_CODE = '';
  if (GOATCOUNTER_CODE && !/^(localhost|127\.0\.0\.1)$/.test(location.hostname)) {
    const gc = document.createElement('script');
    gc.async = true;
    gc.src = 'https://gc.zgo.at/count.js';
    gc.dataset.goatcounter = `https://${GOATCOUNTER_CODE}.goatcounter.com/count`;
    document.head.appendChild(gc);
  }
});
