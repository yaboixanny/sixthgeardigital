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
    status.textContent = 'Thank you. Your request has been submitted. We’ll be in touch using the email address you provided.';
  } catch {
    status.textContent = 'Your request could not be sent. Please try again. Your entries have been kept.';
  } finally { button.disabled = false; }
});
