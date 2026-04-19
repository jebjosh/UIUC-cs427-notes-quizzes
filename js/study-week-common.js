(function () {
  if (/(?:^|[?&])embed=1(?:&|$)/.test(location.search)) {
    document.documentElement.classList.add('embed-mode');
  }

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
