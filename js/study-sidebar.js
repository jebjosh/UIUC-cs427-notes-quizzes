/**
 * 注入合并页侧栏（#study-sidebar-root），或为 index 填充 #study-nav-list。
 * 依赖：先加载 study-weeks-config.js
 */
(function () {
  function findWeekById(id) {
    var weeks = window.STUDY_WEEKS || [];
    for (var i = 0; i < weeks.length; i++) {
      if (weeks[i] && weeks[i].id === id) return weeks[i];
    }
    return null;
  }

  function syncNotesTitleWithSidebar(currentId) {
    if (!currentId || !window.formatWeekLabel) return;
    var week = findWeekById(currentId);
    if (!week) return;
    var titleEl = document.querySelector('.notes-pane header h1');
    if (!titleEl) return;
    titleEl.textContent = window.formatWeekLabel(week);
  }

  function renderStudyNavList(navEl, opts) {
    opts = opts || {};
    var currentId = opts.currentId || '';
    var useHash = !!opts.useHash;
    var onWeekClick = opts.onWeekClick;
    var weeks = window.STUDY_WEEKS;
    var fmt = window.formatWeekLabel;
    if (!navEl || !weeks || !fmt) return;

    navEl.innerHTML = '';
    weeks.forEach(function (w) {
      if (w.children && w.children.length) {
        var group = document.createElement('div');
        group.className = 'study-nav-group';
        group.setAttribute('role', 'group');
        group.setAttribute('aria-label', fmt(w));
        var label = document.createElement('div');
        label.className = 'study-nav-group-label';
        label.textContent = fmt(w);
        group.appendChild(label);
        w.children.forEach(function (ch) {
          var sub = document.createElement('span');
          sub.className = 'study-nav-sub study-nav-soon';
          sub.textContent = fmt(ch);
          group.appendChild(sub);
        });
        navEl.appendChild(group);
        return;
      }
      if (w.soon || !w.file) {
        var span = document.createElement('span');
        span.className = 'study-nav-soon';
        span.textContent = fmt(w);
        navEl.appendChild(span);
        return;
      }
      var a = document.createElement('a');
      a.setAttribute('data-week-id', w.id);
      a.textContent = fmt(w);
      var hrefFile = window.getWeekNavHref ? window.getWeekNavHref(w) : (window.getWeekFile ? window.getWeekFile(w) : w.file);
      if (useHash) {
        a.href = '#' + w.id;
        if (onWeekClick) {
          a.addEventListener('click', function (e) {
            e.preventDefault();
            onWeekClick(w);
          });
        }
      } else {
        a.href = hrefFile;
      }
      if (w.id === currentId) {
        a.classList.add('current');
        a.setAttribute('aria-current', 'page');
      }
      navEl.appendChild(a);
    });
  }

  function setSidebarCollapsed(collapsed) {
    document.body.classList.toggle('study-sidebar-collapsed', !!collapsed);
    try { localStorage.setItem('studySidebarCollapsed', collapsed ? '1' : '0'); } catch (e) {}
    var btn = document.querySelector('.study-nav-toggle');
    if (btn) {
      btn.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
      btn.setAttribute('title', collapsed ? 'Show weeks' : 'Hide weeks');
    }
  }

  function getPreferredCollapsed() {
    try {
      var saved = localStorage.getItem('studySidebarCollapsed');
      if (saved === '1') return true;
      if (saved === '0') return false;
    } catch (e) {}
    return window.innerWidth <= 960;
  }

  function enhanceSidebarToggle(scope) {
    var aside = scope || document.querySelector('.study-nav');
    if (!aside) return;
    var header = aside.querySelector('.study-nav-header');
    if (!header) return;
    var existing = header.querySelector('.study-nav-toggle');
    if (!existing) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'study-nav-toggle';
      btn.setAttribute('aria-label', 'Toggle week menu');
      btn.innerHTML = '<span></span><span></span><span></span>';
      header.appendChild(btn);
      btn.addEventListener('click', function () {
        setSidebarCollapsed(!document.body.classList.contains('study-sidebar-collapsed'));
      });
    }
    setSidebarCollapsed(getPreferredCollapsed());

    aside.querySelectorAll('.study-nav-list a').forEach(function (link) {
      if (link.dataset.sidebarAutoBound === '1') return;
      link.dataset.sidebarAutoBound = '1';
      link.addEventListener('click', function () {
        if (window.innerWidth <= 960) {
          setSidebarCollapsed(true);
        }
      });
    });
  }

  function mountStudySidebar() {
    if (document.documentElement.classList.contains('embed-mode')) return;
    if (/(?:^|[?&])embed=1(?:&|$)/.test(location.search)) return;
    var root = document.getElementById('study-sidebar-root');
    if (!root || !window.STUDY_WEEKS) return;
    var currentId = document.body.getAttribute('data-study-week') || '';
    root.innerHTML = '';
    var aside = document.createElement('aside');
    aside.className = 'study-nav';
    aside.setAttribute('aria-label', 'Course weeks');
    var header = document.createElement('div');
    header.className = 'study-nav-header';
    var title = document.createElement('div');
    title.className = 'study-nav-title';
    title.textContent = 'CS 427: Software Engineering';
    header.appendChild(title);
    var nav = document.createElement('nav');
    nav.className = 'study-nav-list';
    aside.appendChild(header);
    aside.appendChild(nav);
    var langRoot = document.createElement('div');
    langRoot.className = 'study-lang-switch-root';
    langRoot.setAttribute('aria-label', 'Language');
    aside.appendChild(langRoot);
    root.appendChild(aside);
    if (typeof window.mountStudyLangSwitch === 'function') {
      window.mountStudyLangSwitch(langRoot, { inIndex: false });
    }
    renderStudyNavList(nav, { currentId: currentId, useHash: false });
    enhanceSidebarToggle(aside);
    syncNotesTitleWithSidebar(currentId);
  }

  window.renderStudyNavList = renderStudyNavList;
  window.mountStudySidebar = mountStudySidebar;
  window.enhanceSidebarToggle = enhanceSidebarToggle;

  function boot() {
    var currentId = document.body.getAttribute('data-study-week') || '';
    syncNotesTitleWithSidebar(currentId);
    if (document.getElementById('study-sidebar-root')) {
      mountStudySidebar();
    } else {
      enhanceSidebarToggle(document.querySelector('.study-nav'));
    }

    window.addEventListener('resize', function () {
      if (window.innerWidth > 960) {
        setSidebarCollapsed(false);
      }
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
