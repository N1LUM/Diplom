const sidebar = document.getElementById('sidebar');
const openSidebarButton = document.getElementById('open-sidebar');
const closeSidebarButton = document.getElementById('close-sidebar');

openSidebarButton.addEventListener('click', (e) => {
    sidebar.style.right = '0%';
});

closeSidebarButton.addEventListener('click', (e) => {
    sidebar.style.right = '-320px';
});
