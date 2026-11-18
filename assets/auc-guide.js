/* Architect U'r Career: keyboard access for the guides.
   Many guide controls are plain elements with a click handler. A keyboard or switch
   user cannot reach those. This script makes every such control focusable and lets
   Enter or Space activate it. It adds nothing else: no tracking, no storage, no network. */
(function () {
  'use strict';
  var NATIVE = /^(A|BUTTON|INPUT|SELECT|TEXTAREA|SUMMARY|LABEL)$/;
  var SELECTOR = '[onclick], [data-auc-click]';

  function upgrade(el) {
    if (el.nodeType !== 1 || el.hasAttribute('data-auc-kbd')) { return; }
    if (NATIVE.test(el.tagName) && !(el.tagName === 'A' && !el.hasAttribute('href'))) { return; }
    el.setAttribute('data-auc-kbd', '');
    if (!el.hasAttribute('tabindex')) { el.setAttribute('tabindex', '0'); }
    if (!el.hasAttribute('role')) { el.setAttribute('role', 'button'); }
  }

  function scan(root) {
    if (!root || !root.querySelectorAll) { return; }
    if (root.matches && root.matches(SELECTOR)) { upgrade(root); }
    var list = root.querySelectorAll(SELECTOR);
    for (var i = 0; i < list.length; i++) { upgrade(list[i]); }
  }

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ' && e.key !== 'Spacebar') { return; }
    var el = e.target;
    if (!el || !el.hasAttribute || !el.hasAttribute('data-auc-kbd')) { return; }
    e.preventDefault();
    el.click();
  });

  /* A page that has not been reviewed for more than six months says so, by itself.
     The date is read from the header strip: "Last reviewed: November 2026". */
  var MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];

  function staleBanner() {
    var rev = document.querySelector('.auc-bar .auc-bar-rev');
    var bar = document.querySelector('.auc-bar');
    if (!rev || !bar || document.querySelector('.auc-stale')) { return; }
    var m = /([A-Za-z]+)\s+(\d{4})/.exec(rev.textContent || '');
    if (!m) { return; }
    var month = MONTHS.indexOf(m[1].toLowerCase());
    if (month < 0) { return; }
    var now = new Date();
    var age = (now.getFullYear() - parseInt(m[2], 10)) * 12 + (now.getMonth() - month);
    if (age <= 6) { return; }
    var note = document.createElement('div');
    note.className = 'auc-note auc-stale';
    note.setAttribute('role', 'note');
    note.textContent = 'This page was last reviewed in ' + m[1] + ' ' + m[2] + ', more than six months ago. ' +
      'Prices, versions, exam codes and product names may have changed since then: check them against the linked sources.';
    bar.parentNode.insertBefore(note, bar.nextSibling);
  }

  function start() {
    staleBanner();
    scan(document.body);
    if (!('MutationObserver' in window)) { return; }
    var pending = false;
    new MutationObserver(function () {
      if (pending) { return; }
      pending = true;
      window.setTimeout(function () { pending = false; scan(document.body); }, 120);
    }).observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
