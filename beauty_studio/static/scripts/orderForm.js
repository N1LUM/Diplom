document.addEventListener('DOMContentLoaded', function() {
    // Применяем маску ввода к полю номера телефона формы заказа
    var inputMask = new Inputmask('+7 (999) 999-99-99').mask(document.querySelector('#orderForm #id_number'));

    // Обработчик отправки формы заказа
    document.querySelector('#orderForm').addEventListener('submit', function(event) {
        // Получаем значение поля номера телефона
        var number = document.querySelector('#orderForm #id_number').value;
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