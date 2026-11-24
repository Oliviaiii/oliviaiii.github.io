(function () {
  var header = document.querySelector('[data-site-header]');
  if (!header) return;

  var current = header.getAttribute('data-current');
  var links = [
    { key: 'home', href: 'index.html', label: '首頁' },
    { key: 'experience', href: 'index.html#experience', label: '經歷' },
    { key: 'work', href: 'work.html', label: '案例' },
    { key: 'ai', href: 'ai-workflow.html', label: 'AI 工作方式' },
    { key: 'contact', href: 'index.html#connect', label: '聯絡' }
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
}());
