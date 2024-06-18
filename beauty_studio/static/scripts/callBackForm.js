document.addEventListener('DOMContentLoaded', function() {
    // Применяем маску ввода к полю номера телефона формы обратной связи
    var inputMask = new Inputmask('+7 (999) 999-99-99').mask(document.querySelector('#callBackForm #id_number'));

    // Обработчик отправки формы
    document.querySelector('#callBackForm').addEventListener('submit', function(event) {
        // Получаем значение поля номера телефона
        var number = document.querySelector('#callBackForm #id_number').value;
        // Удаляем пробелы, тире, скобки и подчеркивания из номера
        var numberStripped = number.replace(/[\s-()_]/g, '');
        // Проверяем длину номера
        if (numberStripped.length < 12) {
            // Если номер слишком короткий, показываем сообщение об ошибке
            alert('Пожалуйста, введите полный номер телефона');
            // Останавливаем отправку формы
            event.preventDefault();
        }
    });
});
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