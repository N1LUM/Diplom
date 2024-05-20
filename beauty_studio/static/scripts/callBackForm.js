document.addEventListener("DOMContentLoaded", () => {
    const callBackForm = document.getElementById('callBackForm');
    const closeCallBackForm = document.getElementById('closeCallBackForm');
    const overlayCallBackForm = document.getElementById('overlayCallBackForm');
    const openCallBackFormNavbar = document.getElementById('openCallBackFormNavbar');
    const openCallBackFormFooter = document.getElementById('openCallBackFormFooter');

    if (openCallBackFormFooter) {
        openCallBackFormFooter.addEventListener('click', (e) => {
            callBackForm.style.display = 'flex';
            overlayCallBackForm.style.display = 'block';
        });
    }

    if (openCallBackFormNavbar) {
        openCallBackFormNavbar.addEventListener('click', (e) => {
            callBackForm.style.display = 'flex';
            overlayCallBackForm.style.display = 'block';
        });
    }

    if (closeCallBackForm) {
        closeCallBackForm.addEventListener('click', (e) => {
            callBackForm.style.display = 'none';
            overlayCallBackForm.style.display = 'none';
        });
    }
});