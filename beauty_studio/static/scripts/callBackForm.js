document.addEventListener("DOMContentLoaded", () => {
    const callBackForm = document.getElementById('callBackForm');
    const closeCallBackForm = document.getElementById('closeCallBackForm');
    const overlayCallBackForm = document.getElementById('overlayCallBackForm');
    const openCallBackFormNavbar = document.getElementById('openCallBackFormNavbar');
    const openCallBackFormFooter = document.getElementById('openCallBackFormFooter');
    const openCallBackFormPartnership = document.getElementById('openCallBackFormPartnership');

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

    if (openCallBackFormPartnership) {
        openCallBackFormPartnership.addEventListener('click', (e) => {
            callBackForm.style.display = 'flex';
            overlayCallBackForm.style.display = 'block';
        });
    }

    if (overlayCallBackForm) {
        overlayCallBackForm.addEventListener('click', (e) => {
            callBackForm.style.display = 'none';
            overlayCallBackForm.style.display = 'none';
        });
    }

    if (closeCallBackForm) {
        closeCallBackForm.addEventListener('click', (e) => {
            callBackForm.style.display = 'none';
            overlayCallBackForm.style.display = 'none';
        });
    }
});