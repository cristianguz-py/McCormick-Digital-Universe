/* =========================================================
   McCORMICK DIGITAL UNIVERSE — ANALYTICS FRONTEND
   Envía eventos reales a /analytics/track/. No inventa datos:
   sólo reporta lo que el usuario realmente hizo.
   ========================================================= */
(() => {
  function getCookie(name){
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
  }

  function track(eventType, page, metadata){
    const csrftoken = getCookie('csrftoken');
    if (!csrftoken) return; // sin CSRF no se envía (evita errores silenciosos raros)
    fetch('/analytics/track/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ event_type: eventType, page: page || '', metadata: metadata || '' }),
      keepalive: true,
    }).catch(() => { /* fallo silencioso: la analítica nunca debe romper la UI */ });
  }
  window.mccormickTrack = track;

  document.addEventListener('DOMContentLoaded', () => {
    // Clicks marcados explícitamente con data-track-event="..."
    document.querySelectorAll('[data-track-event]').forEach((el) => {
      el.addEventListener('click', () => {
        track(el.dataset.trackEvent, el.dataset.trackPage || '', el.dataset.trackNote || '');
      });
    });

    // Redes sociales: cualquier link externo a instagram/tiktok/threads
    document.querySelectorAll('a[href*="instagram.com"], a[href*="tiktok.com"], a[href*="threads.com"]').forEach((el) => {
      el.addEventListener('click', () => track('social_click', document.body.dataset.page || '', el.href));
    });

    // Botón flotante de WhatsApp = contact_click
    const wa = document.getElementById('whatsappFloat');
    if (wa){
      wa.addEventListener('click', () => track('contact_click', document.body.dataset.page || ''));
    }

    // Apertura de galería (lightbox) = gallery_open
    document.querySelectorAll('.g-item').forEach((el) => {
      if (el.querySelector('img')){
        el.addEventListener('click', () => track('gallery_open', document.body.dataset.page || ''), { once: true });
      }
    });
  });
})();
