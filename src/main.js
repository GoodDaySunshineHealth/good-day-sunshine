const SOCIAL_LINKS = {
  instagram: 'https://www.instagram.com/gooddaysunshinehealth',
  tiktok: 'https://www.tiktok.com/@gooddaysunshinehealth',
  youtube: 'https://www.youtube.com/@GoodDaySunshineHealth',
  pinterest: 'https://pin.it/4hj5CgU6v',
  facebook: 'https://www.facebook.com/profile.php?id=61590338638023',
};

function initNav() {
  const nav = document.getElementById('nav');
  const toggle = document.getElementById('nav-toggle');
  const menu = document.getElementById('mobile-menu');

  window.addEventListener('scroll', () => {
    nav?.classList.toggle('scrolled', window.scrollY > 20);
  });

  toggle?.addEventListener('click', () => {
    const isOpen = menu?.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(isOpen));
  });

  menu?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => menu.classList.remove('open'));
  });
}

function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      const id = anchor.getAttribute('href');
      if (!id || id === '#') return;

      e.preventDefault();

      if (id === '#top') {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return;
      }

      const target = document.querySelector(id);
      if (!target) return;

      const navHeight = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--nav-height'), 10) || 72;
      const top = target.getBoundingClientRect().top + window.scrollY - navHeight;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });
}

function initSignupForms() {
  document.querySelectorAll('[data-signup-form]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const emailInput = form.querySelector('input[type="email"]');
      const successEl = form.parentElement?.querySelector('[data-signup-success]');

      if (!emailInput?.value.includes('@')) {
        emailInput?.classList.add('invalid');
        setTimeout(() => emailInput?.classList.remove('invalid'), 1500);
        return;
      }

      form.style.display = 'none';
      successEl?.classList.add('visible');
    });
  });
}

function initYear() {
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());
}

document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initSmoothScroll();
  initSignupForms();
  initYear();
});

