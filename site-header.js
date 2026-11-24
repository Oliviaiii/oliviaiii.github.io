(function () {
  var header = document.querySelector('[data-site-header]');
  if (!header) return;

  var current = header.getAttribute('data-current');
  var links = [
    { key: 'home', href: 'index.html', label: '首頁', mobileLabel: '首頁', icon: '<path d="M3 10.5 12 3l9 7.5v9a1.5 1.5 0 0 1-1.5 1.5h-4.75v-6.5h-5.5V21H4.5A1.5 1.5 0 0 1 3 19.5z"/>' },
    { key: 'experience', href: 'index.html#experience', label: '經歷', mobileLabel: '經歷', icon: '<path d="M8 5V3.75A1.75 1.75 0 0 1 9.75 2h4.5A1.75 1.75 0 0 1 16 3.75V5m-13 5.5h18M4.5 5h15A1.5 1.5 0 0 1 21 6.5v13A1.5 1.5 0 0 1 19.5 21h-15A1.5 1.5 0 0 1 3 19.5v-13A1.5 1.5 0 0 1 4.5 5Z"/>' },
    { key: 'work', href: 'work.html', label: '案例', mobileLabel: '案例', icon: '<path d="M3.5 5.5h6l1.75 2H20.5V20H3.5zM3.5 11h17"/>' },
    { key: 'ai', href: 'ai-workflow.html', label: 'AI 工作方式', mobileLabel: 'AI 工作', icon: '<path d="m12 2 1.35 4.15L17.5 7.5l-4.15 1.35L12 13l-1.35-4.15L6.5 7.5l4.15-1.35zm6.25 10.5.9 2.85 2.85.9-2.85.9-.9 2.85-.9-2.85-2.85-.9 2.85-.9zM6 14l1.05 3.2L10.25 18l-3.2 1.05L6 22.25l-1.05-3.2L1.75 18l3.2-1.05z"/>' },
    { key: 'contact', href: 'index.html#connect', label: '聯絡', mobileLabel: '聯絡', icon: '<path d="M3 5.5h18v13H3zM4 7l8 6 8-6"/>' }
  ];

  var navLinks = links.map(function (link) {
    var currentAttribute = link.key === current ? ' aria-current="page"' : '';
    return '<a href="' + link.href + '"' + currentAttribute + '>' + link.label + '</a>';
  }).join('');

  header.innerHTML =
    '<div class="site-header-inner">' +
      '<a class="site-brand" href="index.html">林芷筠 <small>Olivia Lin · Product Builder</small></a>' +
      '<nav class="site-nav" aria-label="主導覽">' +
        navLinks +
        '<a class="site-mobile-resume" href="林芷筠中文履歷.pdf?v=20261124-2" download>PDF 履歷</a>' +
      '</nav>' +
      '<a class="site-header-cta" href="林芷筠中文履歷.pdf?v=20261124-2" download>PDF 履歷</a>' +
    '</div>';

  var mobileLinks = links.map(function (link) {
    var currentAttribute = link.key === current ? ' aria-current="page"' : '';
    return '<a data-mobile-key="' + link.key + '" href="' + link.href + '"' + currentAttribute + '>' +
      '<svg viewBox="0 0 24 24" aria-hidden="true">' + link.icon + '</svg>' +
      '<span>' + link.mobileLabel + '</span>' +
    '</a>';
  }).join('');

  header.insertAdjacentHTML(
    'afterend',
    '<nav class="mobile-bottom-nav" aria-label="手機主導覽">' +
      mobileLinks +
      '<a data-mobile-key="resume" href="林芷筠中文履歷.pdf?v=20261124-2" download>' +
        '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 2.75h8l4 4V21.25H6zM14 2.75v4h4M9 12h6M9 16h6"/></svg>' +
        '<span>PDF</span>' +
      '</a>' +
    '</nav>'
  );

  var mobileNav = document.querySelector('.mobile-bottom-nav');
  if (!mobileNav) return;

  function setMobileCurrent(key) {
    Array.prototype.forEach.call(mobileNav.querySelectorAll('a[data-mobile-key]'), function (link) {
      if (link.getAttribute('data-mobile-key') === key) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
  }

  if (current === 'home') {
    var experience = document.getElementById('experience');
    var contact = document.getElementById('connect');
    var updateMobileCurrent = function () {
      var marker = window.scrollY + window.innerHeight * 0.35;
      if (contact && marker >= contact.offsetTop) setMobileCurrent('contact');
      else if (experience && marker >= experience.offsetTop) setMobileCurrent('experience');
      else setMobileCurrent('home');
    };
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        updateMobileCurrent();
        ticking = false;
      });
    }, { passive: true });
    window.addEventListener('hashchange', updateMobileCurrent);
    updateMobileCurrent();
  }
}());
