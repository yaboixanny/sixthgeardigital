// Desktop navigation opens on hover; keyboard and touch users can expand it too.
const websiteDropdowns = [...document.querySelectorAll('.website-nav-dropdown')];
function closeWebsiteDropdown(dropdown) {
  dropdown.querySelector('button').setAttribute('aria-expanded', 'false');
  dropdown.querySelector('.website-nav-panel').hidden = true;
}
for (const dropdown of websiteDropdowns) {
  const trigger = dropdown.querySelector('button');
  const panel = dropdown.querySelector('.website-nav-panel');
  function open() {
    websiteDropdowns.filter(other => other !== dropdown).forEach(closeWebsiteDropdown);
    trigger.setAttribute('aria-expanded', 'true');
    panel.hidden = false;
  }
  dropdown.addEventListener('mouseenter', open);
  dropdown.addEventListener('mouseleave', () => {
    if (!dropdown.contains(document.activeElement)) closeWebsiteDropdown(dropdown);
  });
  trigger.addEventListener('click', () => {
    if (panel.hidden) open();
    else if (!window.matchMedia('(hover: hover)').matches) closeWebsiteDropdown(dropdown);
  });
  trigger.addEventListener('keydown', event => {
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      open();
      panel.querySelector('a')?.focus();
    }
  });
  dropdown.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      event.preventDefault();
      closeWebsiteDropdown(dropdown);
      trigger.focus();
    }
  });
  dropdown.addEventListener('focusout', event => {
    if (!dropdown.contains(event.relatedTarget)) closeWebsiteDropdown(dropdown);
  });
}
document.addEventListener('click', event => {
  if (!event.target.closest('.website-nav-dropdown')) websiteDropdowns.forEach(closeWebsiteDropdown);
});
window.matchMedia('(min-width: 1024px)').addEventListener('change', () => websiteDropdowns.forEach(closeWebsiteDropdown));
