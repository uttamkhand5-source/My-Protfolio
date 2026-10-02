function toggleTheme(){document.body.classList.toggle('light');localStorage.theme=document.body.classList.contains('light')?'light':'dark'}if(localStorage.theme==='light')document.body.classList.add('light');
document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{const el=document.querySelector(a.getAttribute('href'));if(el){e.preventDefault();el.scrollIntoView({behavior:'smooth'})}}));
setTimeout(()=>document.querySelectorAll('.flash').forEach(x=>x.remove()),4000);
