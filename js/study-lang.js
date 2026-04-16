/**
 * Site language: Chinese (zh) vs English (en). Pages live under zh/ and en/.
 * Persists in localStorage on index (default English on first open); path decides language on week pages.
 */
(function () {
  var STORAGE_KEY = 'cs427-study-lang';

  function normPath() {
    return ((typeof location !== 'undefined' && location.pathname) || '').replace(/\\/g, '/');
  }

  function inferLangFromPath() {
    var path = normPath();
    if (path.indexOf('/en/') !== -1) return 'en';
    if (path.indexOf('/zh/') !== -1) return 'zh';
    return 'zh';
  }

  function isIndexPage() {
    var p = normPath();
    return /\/index\.html$/i.test(p) || /\/$/i.test(p) || p === '' || p === '/';
  }

  function insideLangFolder() {
    var p = normPath();
    return /\/(zh|en)\/[^/]+\.html$/i.test(p);
  }

  window.getStudyLang = function () {
    if (!isIndexPage()) {
      return inferLangFromPath();
    }
    try {
      var s = localStorage.getItem(STORAGE_KEY);
      if (s === 'en' || s === 'zh') return s;
    } catch (e) {}
    return 'en';
  };

  window.setStudyLang = function (lang) {
    if (lang !== 'en' && lang !== 'zh') return;
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {}
    try {
      window.dispatchEvent(new CustomEvent('study-lang-change', { detail: { lang: lang } }));
    } catch (e2) {}
  };

  /** Path from site root, e.g. zh/week_1_....html — for index iframe src */
  window.getWeekFile = function (week) {
    if (!week || !week.file) return '';
    var lang = window.getStudyLang();
    var folder = lang === 'en' ? 'en' : 'zh';
    return folder + '/' + week.file;
  };

  /**
   * Nav href: from index, use zh/... or en/...; from inside zh/ or en/, use sibling filename only.
   */
  window.getWeekNavHref = function (week) {
    if (!week || !week.file) return '';
    if (insideLangFolder()) {
      return week.file;
    }
    return window.getWeekFile(week);
  };

  window.switchStudyPageLang = function (targetLang) {
    if (!window.STUDY_WEEKS) return;
    var currentId = document.body && document.body.getAttribute('data-study-week');
    if (!currentId) return;
    var week = null;
    for (var i = 0; i < window.STUDY_WEEKS.length; i++) {
      if (window.STUDY_WEEKS[i].id === currentId) {
        week = window.STUDY_WEEKS[i];
        break;
      }
    }
    if (!week || !week.file) return;
    window.setStudyLang(targetLang);
    var folder = targetLang === 'en' ? 'en' : 'zh';
    var file = folder + '/' + week.file;
    if (insideLangFolder()) {
      file = '../' + folder + '/' + week.file;
    }
    var qs = location.search || '';
    if (qs.indexOf('embed=1') !== -1) {
      file += (file.indexOf('?') >= 0 ? '&' : '?') + 'embed=1';
    }
    location.href = file;
  };

  window.mountStudyLangSwitch = function (container, opts) {
    opts = opts || {};
    var inIndex = !!opts.inIndex;
    if (!container) return;

    var wrap = document.createElement('div');
    wrap.className = 'study-lang-switch';
    wrap.setAttribute('role', 'group');
    wrap.setAttribute('aria-label', 'Language');

    function btn(label, lang, active) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'study-lang-btn' + (active ? ' active' : '');
      b.textContent = label;
      b.setAttribute('aria-pressed', active ? 'true' : 'false');
      b.addEventListener('click', function () {
        if (inIndex) {
          if (lang === window.getStudyLang()) return;
          window.setStudyLang(lang);
          return;
        }
        if (lang === window.getStudyLang()) return;
        window.switchStudyPageLang(lang);
      });
      return b;
    }

    function refresh() {
      var lang = window.getStudyLang();
      wrap.innerHTML = '';
      wrap.appendChild(btn('中文', 'zh', lang === 'zh'));
      wrap.appendChild(btn('English', 'en', lang === 'en'));
    }

    refresh();
    window.addEventListener('study-lang-change', refresh);
    container.appendChild(wrap);
  };

  if (!isIndexPage()) {
    try {
      localStorage.setItem(STORAGE_KEY, inferLangFromPath());
    } catch (e) {}
  }
})();
