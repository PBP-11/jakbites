//buat navbar

const nav = document.getElementById("navBar");
    
window.addEventListener('scroll', () => {
    if (window.scrollY === 0) {
        nav.classList.remove('backdrop-filter', 'backdrop-blur-lg',  'border-b', 'border-gray-300');
    } else if (window.scrollY > 100) {
        nav.classList.add('backdrop-filter', 'backdrop-blur-lg',  'border-b', 'border-gray-300');
    }
});

const dropdownBtn = document.getElementById('dropdownBtn');
const dropdownMenu = document.getElementById('dropdownMenu');
const dropdownBar = document.getElementById('dropdownBar')


dropdownMenu.addEventListener('click', () => {
    dropdownBar.classList.toggle('hidden');
});
