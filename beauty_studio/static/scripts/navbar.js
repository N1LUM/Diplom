const overlay = document.getElementById('overlay');
const sidebar = document.getElementById('sidebar');
const openSidebarButton = document.getElementById('open-sidebar');
const closeSidebarButton = document.getElementById('close-sidebar');

openSidebarButton.addEventListener('click', (e) => {
    if (overlay != null) {
        overlay.style.width = 'calc(100vw - 320px)';
    }
    sidebar.style.right = '0%';
});

closeSidebarButton.addEventListener('click', (e) => {
    if (overlay != null) {
        overlay.style.width = '100%';
    }

    sidebar.style.right = '-320px';
});
