(function () {
  // Embed mode
  if (/(?:^|[?&])embed=1(?:&|$)/.test(location.search)) {
    document.documentElement.classList.add('embed-mode');
  }

  // Tab switcher (notes pane tabs)
  window.switchTab = function (id, btn) {
    if (!btn) return;
    var pane = btn.closest('.notes-pane');
    if (!pane) return;
    pane.querySelectorAll('.tab-panel').forEach(function (p) { p.classList.remove('active'); });
    pane.querySelectorAll('.tab-btn').forEach(function (b) { b.classList.remove('active'); });
    var panel = document.getElementById('tab-' + id);
    if (panel) panel.classList.add('active');
    btn.classList.add('active');
  };

  // ── Mobile pane switcher ──────────────────────────────────────
  // On ≤960px, inject a sticky "Notes | Quiz" pill bar above the
  // page-split so users can toggle between the two panes.

  function injectPaneSwitcher() {
    var split = document.querySelector('.page-split');
    if (!split) return;
    if (document.querySelector('.pane-switcher')) return; // already injected

    var bar = document.createElement('div');
    bar.className = 'pane-switcher';
    bar.setAttribute('role', 'tablist');
    bar.setAttribute('aria-label', 'Switch between notes and quiz');

    var btnNotes = document.createElement('button');
    btnNotes.type = 'button';
    btnNotes.className = 'pane-switch-btn active';
    btnNotes.textContent = '📖 Notes';
    btnNotes.setAttribute('role', 'tab');
    btnNotes.setAttribute('aria-selected', 'true');

    var btnQuiz = document.createElement('button');
    btnQuiz.type = 'button';
    btnQuiz.className = 'pane-switch-btn';
    btnQuiz.textContent = '✏️ Quiz';
    btnQuiz.setAttribute('role', 'tab');
    btnQuiz.setAttribute('aria-selected', 'false');

    bar.appendChild(btnNotes);
    bar.appendChild(btnQuiz);

    // Insert before the split container
    split.parentNode.insertBefore(bar, split);

    // Set initial mobile active state
    split.classList.add('mobile-notes-active');

    btnNotes.addEventListener('click', function () {
      split.classList.remove('mobile-quiz-active');
      split.classList.add('mobile-notes-active');
      btnNotes.classList.add('active');
      btnNotes.setAttribute('aria-selected', 'true');
      btnQuiz.classList.remove('active');
      btnQuiz.setAttribute('aria-selected', 'false');
      // Scroll to top of notes pane
      var notesPaneEl = split.querySelector('.notes-pane');
      if (notesPaneEl) notesPaneEl.scrollTop = 0;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    btnQuiz.addEventListener('click', function () {
      split.classList.remove('mobile-notes-active');
      split.classList.add('mobile-quiz-active');
      btnQuiz.classList.add('active');
      btnQuiz.setAttribute('aria-selected', 'true');
      btnNotes.classList.remove('active');
      btnNotes.setAttribute('aria-selected', 'false');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  function handleResponsiveLayout() {
    var bar = document.querySelector('.pane-switcher');
    var split = document.querySelector('.page-split');
    if (window.innerWidth <= 960) {
      if (!bar) injectPaneSwitcher();
      // Make sure one pane-active class is set
      if (split && !split.classList.contains('mobile-notes-active') && !split.classList.contains('mobile-quiz-active')) {
        split.classList.add('mobile-notes-active');
      }
    } else {
      // Desktop: remove mobile hide classes so both panes show
      if (split) {
        split.classList.remove('mobile-notes-active', 'mobile-quiz-active');
      }
    }
  }

  function init() {
    handleResponsiveLayout();
    var debounceTimer;
    window.addEventListener('resize', function () {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(handleResponsiveLayout, 120);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
