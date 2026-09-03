const languageButton = document.querySelector('.language-toggle');
const languageParts = languageButton.querySelectorAll('span');

function setLanguage(language) {
  const isEnglish = language === 'en';
  document.documentElement.lang = isEnglish ? 'en' : 'zh-Hant';
  document.querySelectorAll('[data-zh][data-en]').forEach((element) => {
    const value = element.dataset[language];
    if (value.includes('<br>') || value.includes('<em>')) {
      element.innerHTML = value;
    } else {
      element.textContent = value;
    }
  });
  document.querySelectorAll('[data-href-zh][data-href-en]').forEach((element) => {
    element.href = element.dataset[`href${isEnglish ? 'En' : 'Zh'}`];
  });
  languageButton.setAttribute('aria-pressed', String(isEnglish));
  languageParts[0].classList.toggle('active', !isEnglish);
  languageParts[2].classList.toggle('active', isEnglish);
  localStorage.setItem('portfolio-language', language);
}

languageButton.addEventListener('click', () => {
  setLanguage(document.documentElement.lang === 'en' ? 'zh' : 'en');
});

const savedLanguage = localStorage.getItem('portfolio-language');
if (savedLanguage === 'en') setLanguage('en');

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((element, index) => {
  element.style.transitionDelay = `${Math.min(index % 4, 3) * 70}ms`;
  observer.observe(element);
});

const header = document.querySelector('.site-header');
window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 12);
}, { passive: true });

document.getElementById('year').textContent = new Date().getFullYear();
