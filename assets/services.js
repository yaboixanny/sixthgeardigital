const exampleTabs = [...document.querySelectorAll('[role="tab"]')];
function activateExample(tab) {
  for (const candidate of exampleTabs) {
    const active = candidate === tab;
    candidate.setAttribute('aria-selected', String(active));
    candidate.tabIndex = active ? 0 : -1;
    document.getElementById(candidate.getAttribute('aria-controls')).hidden = !active;
  }
}
exampleTabs.forEach((tab, index) => {
  tab.addEventListener('click', () => activateExample(tab));
  tab.addEventListener('keydown', event => {
    let next;
    if (event.key === 'ArrowRight') next = (index + 1) % exampleTabs.length;
    if (event.key === 'ArrowLeft') next = (index + exampleTabs.length - 1) % exampleTabs.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = exampleTabs.length - 1;
    if (next !== undefined) {
      event.preventDefault();
      activateExample(exampleTabs[next]);
      exampleTabs[next].focus();
    }
  });
});
