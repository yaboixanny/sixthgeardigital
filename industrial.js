const menuButton = document.querySelector('.menu-toggle');
const menu = document.querySelector('#mobile-menu');
function closeMenu() {
  menu.hidden = true;
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Open navigation');
}
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menu.hidden = !open;
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
});
menu.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', event => { if (event.key === 'Escape' && !menu.hidden) { closeMenu(); menuButton.focus(); } });
window.matchMedia('(min-width: 1024px)').addEventListener('change', event => { if (event.matches) closeMenu(); });
const contactDialog = document.querySelector('#contact-dialog');
if (contactDialog) {
  let contactOpener;
  function openContact(trigger) {
    if (contactDialog.open) return;
    contactOpener = trigger;
    contactDialog.showModal();
    document.body.classList.add('contact-dialog-open');
  }
  document.addEventListener('click', event => {
    const trigger = event.target.closest('[data-contact-open], a[href="#growth-plan"]');
    if (!trigger || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    openContact(trigger);
  });
  contactDialog.querySelector('[data-contact-close]').addEventListener('click', () => contactDialog.close());
  contactDialog.addEventListener('click', event => { if (event.target === contactDialog) contactDialog.close(); });
  contactDialog.addEventListener('close', () => {
    document.body.classList.remove('contact-dialog-open');
    if (document.activeElement !== document.body && !contactDialog.contains(document.activeElement)) return;
    const fallback = menuButton.getClientRects().length ? menuButton : document.querySelector('[data-contact-open]');
    const returnTarget = contactOpener?.getClientRects().length ? contactOpener : fallback;
    returnTarget?.focus({ preventScroll: true });
  });
  const openContactFromHash = () => { if (location.hash === '#growth-plan') openContact(); };
  window.addEventListener('hashchange', openContactFromHash);
  openContactFromHash();
}
const form = document.querySelector('#growth-plan-form');
const status = document.querySelector('#form-status');
if (form && status) form.addEventListener('submit', async event => {
  event.preventDefault();
  status.hidden = false;
  if (['localhost', '127.0.0.1'].includes(location.hostname)) {
    status.textContent = 'This is a local preview. Submissions are available on the hosted website.';
    return;
  }
  const button = form.querySelector('button[type="submit"]');
  button.disabled = true;
  status.textContent = 'Sending your request…';
  try {
    const response = await fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(form)).toString() });
    if (!response.ok) throw new Error('Submission failed');
    form.hidden = true;
    status.textContent = 'Thanks for your message. We’ll reply to the email address you provided.';
  } catch {
    status.textContent = 'Your message could not be sent. Please try again. Your details are still in the form.';
  } finally { button.disabled = false; }
});
