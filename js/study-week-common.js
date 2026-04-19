(function () {
  if (/(?:^|[?&])embed=1(?:&|$)/.test(location.search)) {
    document.documentElement.classList.add('embed-mode');
  }


  var THEME_VARS = {
    dark: {
      '--bg':'#0f172a','--surface':'#111827','--surface2':'#1f2937','--border':'#334155','--border2':'#334155',
      '--text':'#e5e7eb','--text2':'#cbd5e1','--muted':'#94a3b8','--tag-bg':'#243244','--accent':'#60a5fa',
      '--accent-light':'#0f2747','--accent2':'#f59e0b','--accent2-light':'#3a2a08','--blue':'#93c5fd','--blue-light':'#10233f',
      '--red':'#fca5a5','--red-light':'#3b1218','--green':'#34d399','--green-light':'#052e25',
      '--correct-bg':'#052e1d','--correct-text':'#bbf7d0','--wrong-bg':'#3f1115','--wrong-text':'#fecaca','--reveal-bg':'#132d52','--reveal-text':'#bfdbfe'
    }
  };

  function syncStudyTheme(theme) {
    var t = theme === 'dark' ? 'dark' : 'light';
    var root = document.documentElement;
    root.setAttribute('data-theme', t);
    if (document.body) document.body.setAttribute('data-theme', t);
    Object.keys(THEME_VARS.dark).forEach(function(name){
      if (t === 'dark') root.style.setProperty(name, THEME_VARS.dark[name]);
      else root.style.removeProperty(name);
    });
    document.dispatchEvent(new CustomEvent('study-theme-applied', { detail: { theme: t } }));
  }
  window.syncStudyTheme = syncStudyTheme;
  var savedTheme = null;
  try { savedTheme = localStorage.getItem('studyTheme'); } catch (e) {}
  if (savedTheme === 'dark' || savedTheme === 'light') syncStudyTheme(savedTheme);
  window.addEventListener('study-theme-change', function (ev) { syncStudyTheme(ev && ev.detail ? ev.detail.theme : 'light'); });
  window.addEventListener('storage', function (ev) { if (ev.key === 'studyTheme' && (ev.newValue === 'dark' || ev.newValue === 'light')) syncStudyTheme(ev.newValue); });

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
})();
