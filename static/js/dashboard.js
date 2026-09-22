/* =========================================================
   DASHBOARD — toggle de sidebar móvil + sistema de toasts
   ========================================================= */
(() => {
  const toggle = document.getElementById('dashSidebarToggle');
  const sidebar = document.getElementById('dashSidebar');
  if (toggle && sidebar){
    toggle.addEventListener('click', () => sidebar.classList.toggle('open'));
    document.addEventListener('click', (e) => {
      if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== toggle){
        sidebar.classList.remove('open');
      }
    });
  }

  // Toasts: lee mensajes de Django (django.contrib.messages) ya renderizados
  // en el DOM con data-toast, y los muestra con animación + auto-cierre.
  const stack = document.getElementById('toastStack');
  if (stack){
    stack.querySelectorAll('[data-toast]').forEach((el) => {
      setTimeout(() => { el.style.opacity = '0'; setTimeout(() => el.remove(), 300); }, 4500);
    });
  }

  // Loading state genérico para formularios marcados con data-loading-text
  document.querySelectorAll('form[data-loading-text]').forEach((form) => {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('button[type="submit"]');
      if (btn){ btn.disabled = true; btn.textContent = form.dataset.loadingText; }
    });
  });
})();
