/* =========================================================
   McCORMICK DIGITAL UNIVERSE — JS GLOBAL
   Nav, menú móvil, reveal, lightbox reutilizable, footer año,
   y el botón de contacto/WhatsApp con número placeholder.
   ========================================================= */

/* ---------------------------------------------------------
   CONFIGURACIÓN DE CONTACTO
   El número real vive en el backend: settings.CONTACT_PHONE (.env).
   Django lo inyecta una sola vez como data-attribute en <body>
   (ver templates/base_public.html) para no repetirlo en el código.
--------------------------------------------------------- */
const CONTACT_PHONE = document.body.dataset.contactPhone || "+57 XXX XXX XXXX";

function isContactPhoneReady(phone){
  return document.body.dataset.contactReady === '1' && !/x/i.test(phone);
}

function whatsappLink(phone, message){
  const digits = phone.replace(/[^\d]/g, '');
  const text = encodeURIComponent(message || 'Hola, quiero más información.');
  return `https://wa.me/${digits}?text=${text}`;
}

(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Nav scroll state
  const nav = document.getElementById('siteNav');
  if (nav){
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 40);
    }, { passive: true });
  }

  // Mobile menu
  const toggle = document.getElementById('navToggle');
  const menu = document.getElementById('mobileMenu');
  if (toggle && menu){
    function setMenu(open){
      toggle.classList.toggle('open', open);
      menu.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    }
    toggle.addEventListener('click', () => setMenu(!menu.classList.contains('open')));
    menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  }

  // Reveal on scroll — reserved for section heads and single hero statements
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reducedMotion){
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting){
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('in'));
  }

  // Subtle parallax on large banner/photo elements marked [data-parallax]
  if (!reducedMotion){
    const parallaxTargets = Array.from(document.querySelectorAll('[data-parallax]'));
    let ticking = false;
    function updateParallax(){
      parallaxTargets.forEach(img => {
        const rect = img.parentElement.getBoundingClientRect();
        const progress = rect.top / window.innerHeight;
        const shift = Math.max(-12, Math.min(12, progress * 14));
        img.style.transform = `translateY(${shift}px)`;
      });
      ticking = false;
    }
    if (parallaxTargets.length){
      window.addEventListener('scroll', () => {
        if (!ticking){ requestAnimationFrame(updateParallax); ticking = true; }
      }, { passive: true });
      updateParallax();
    }
  }

  // Lightbox with keyboard support and prev/next navigation
  const lightbox = document.getElementById('lightbox');
  if (lightbox){
    const lightboxImg = document.getElementById('lightboxImg');
    const lightboxClose = document.getElementById('lightboxClose');
    const lightboxPrev = document.getElementById('lightboxPrev');
    const lightboxNext = document.getElementById('lightboxNext');
    const galleryImgs = Array.from(document.querySelectorAll('.g-item img'));
    let currentIndex = 0;
    let lastFocused = null;

    function showImage(index){
      if (!galleryImgs.length) return;
      currentIndex = (index + galleryImgs.length) % galleryImgs.length;
      const img = galleryImgs[currentIndex];
      lightboxImg.src = img.src;
      lightboxImg.alt = img.alt;
    }
    function openLightbox(index){
      lastFocused = document.activeElement;
      showImage(index);
      lightbox.classList.add('open');
      document.body.style.overflow = 'hidden';
      lightboxClose.focus();
    }
    function closeLightbox(){
      lightbox.classList.remove('open');
      document.body.style.overflow = '';
      if (lastFocused) lastFocused.focus();
    }
    // Only items that actually contain a photo are clickable — placeholder
    // tiles (no image yet) stay purely visual, no empty lightbox.
    let photoIndex = 0;
    document.querySelectorAll('.g-item').forEach((btn) => {
      if (!btn.querySelector('img')) return;
      const index = photoIndex++;
      btn.addEventListener('click', () => openLightbox(index));
    });
    lightboxClose.addEventListener('click', closeLightbox);
    lightboxPrev.addEventListener('click', () => showImage(currentIndex - 1));
    lightboxNext.addEventListener('click', () => showImage(currentIndex + 1));
    lightbox.addEventListener('click', (e) => { if (e.target === lightbox) closeLightbox(); });
    window.addEventListener('keydown', (e) => {
      if (!lightbox.classList.contains('open')) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') showImage(currentIndex - 1);
      if (e.key === 'ArrowRight') showImage(currentIndex + 1);
    });
  }

  // WhatsApp / contact floating button
  const waFloat = document.getElementById('whatsappFloat');
  if (waFloat){
    const status = waFloat.querySelector('.whatsapp-float__status');
    if (isContactPhoneReady(CONTACT_PHONE)){
      waFloat.setAttribute('href', whatsappLink(CONTACT_PHONE));
      waFloat.setAttribute('target', '_blank');
      waFloat.setAttribute('rel', 'noopener');
      if (status) status.textContent = 'Escríbenos por WhatsApp';
    } else {
      // No real number yet: keep it visible but clearly not a live link.
      waFloat.removeAttribute('href');
      waFloat.setAttribute('role', 'button');
      waFloat.setAttribute('tabindex', '0');
      waFloat.setAttribute('aria-disabled', 'true');
      if (status) status.textContent = 'Número en configuración';
      waFloat.addEventListener('click', (e) => e.preventDefault());
    }
  }

  // Footer year
  document.querySelectorAll('[data-year]').forEach(el => {
    el.textContent = '© ' + new Date().getFullYear() + ' McCormick';
  });
})();
