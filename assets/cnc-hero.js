// Keep the overlay menu readable as the visitor leaves the top of the page.
const cncHeader = document.querySelector('.cnc-hero-page .site-header');
if (cncHeader) {
  const updateCncHeader = () => cncHeader.classList.toggle('is-scrolled', window.scrollY > 8);
  updateCncHeader();
  window.addEventListener('scroll', updateCncHeader, { passive: true });
}
