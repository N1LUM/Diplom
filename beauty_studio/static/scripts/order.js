document.querySelectorAll('.order_listOfServices__service').forEach(function(serviceCard) {
    serviceCard.addEventListener('click', function() {
        const service_id = this.getAttribute('data-id');
        const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        fetch('/add_to_chosen_services/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ service_id: service_id }),
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Ошибка при добавлении сервиса в корзину chosenServices');
            }
        })
        .then(data => {
             console.log('Сервис успешно добавлен в корзину chosenServices:', data);
            const newService = data.service; // Получаем данные нового сервиса

            // Проверяем, существует ли уже элемент с таким ID
            const existingService = document.getElementById(newService.id);

            // Если элемент с таким ID уже существует, не добавляем его снова
            if (existingService) {
                console.log('Услуга с ID', newService.id, 'уже в корзине.');
            } else {
                updateTotalCostAndTime(newService.cost, newService.hours, newService.minute)

                // Создаем новый элемент на основе данных о новом сервисе
                const newServiceElement = document.createElement('div');
                newServiceElement.classList.add('cart_items__service');
                newServiceElement.setAttribute('id', newService.id);
                newServiceElement.setAttribute('data-id', newService.id); // Добавляем атрибут data-id
                newServiceElement.innerHTML = `
                    <div class="items_service__nameAndCross">
                        <p class="service_nameAndCross__title">${newService.title}</p>
                        <img src="/static/images/orderImages/cross.svg" alt="" class="service_nameAndCross__img">
                    </div>
                    <div class="items_service__info">
                        <div class="service_info__time">
                            <p class="info_time__hours">${newService.hours}ч</p>
                            <p class="info_time__minutes">${newService.minute}мин</p>
                        </div>
                        <p class="service_info__cost">${newService.cost}руб</p>
                    </div>
                </div>
                `;

                // Добавляем новый элемент в контейнер с услугами
                const listOfServicesContainer = document.querySelector('.order_cart__items');
                listOfServicesContainer.appendChild(newServiceElement);

                // Добавляем обработчик события клика на новый элемент
                newServiceElement.querySelector('.service_nameAndCross__img').addEventListener('click', function(event) {
                    event.stopPropagation(); // Чтобы событие не всплывало к родительскому элементу
                    const service_id = newServiceElement.getAttribute('data-id');
                    const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

                    fetch('/delete_from_chosen_services/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': csrftoken,
                        },
                        body: JSON.stringify({ service_id: service_id }),
                    })
                    .then(response => {
                        if (response.ok) {
                            return response.json();
                        } else {
                            throw new Error('Ошибка при удалении сервиса из корзины chosenServices');
                        }
                    })
                    .then(data => {
                        console.log('Сервис успешно удален из корзины chosenServices:', data);
                        const deletedService = data.service

                        updateTotalCostAndTime(-newService.cost, -newService.hours, -newService.minute)

                        const serviceToRemove = document.getElementById(deletedService.id);
                        if (serviceToRemove) {
                            serviceToRemove.remove();
                            console.log('Элемент с ID', deletedService.id, 'удален из корзины.');
                        } else {
                            console.log('Элемент с ID', deletedService.id, 'не найден в корзине.');
                        }
                    })
                    .catch(error => {
                        console.error('Ошибка:', error);
                    });
                });
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    });
});

function updateTotalCostAndTime(costChange, hoursChange, minutesChange) {
    const totalCostElement = document.querySelector('.cart_resultCost__cost');
    const totalTimeElement = document.querySelector('.cart_resultCost__time');

    // Парсим текущие значения стоимости и времени
    const currentCost =  parseInt(totalCostElement.innerText.replace(/\D/g, ''));
    const totalTimeParts = totalTimeElement.innerText.split(' '); // Разделяем на составляющие по пробелам

    // Парсим значения часов и минут, учитывая возможные пробелы
    const currentHours = parseInt(totalTimeParts[1].replace(/\D/g, ''));
    const currentMinutes = parseInt(totalTimeParts[2].replace(/\D/g, ''));

    const updatedCost = currentCost + costChange;
    let updatedHours = currentHours + hoursChange;
    let updatedMinutes = currentMinutes + minutesChange;

    if (updatedMinutes >= 60) {
        updatedHours += Math.floor(updatedMinutes / 60); // Добавляем целое количество часов
        updatedMinutes %= 60; // Оставляем только оставшиеся минуты
    }

    // Обновляем текст в элементах общей стоимости и времени
    totalCostElement.innerText = `Цена: ${updatedCost}руб`;
    totalTimeElement.innerText = `Время: ${updatedHours}ч ${updatedMinutes}мин`;
}


document.querySelector('.order_cart__items').addEventListener('click', function(event) {
    if (event.target && event.target.matches('.service_nameAndCross__img')) {
        const service_id = event.target.closest('.cart_items__service').getAttribute('data-id');
        const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        fetch('/delete_from_chosen_services/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ service_id: service_id }),
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Ошибка при удалении сервиса из корзины chosenServices');
            }
        })
        .then(data => {
            console.log('Сервис успешно удален из корзины chosenServices:', data);
            console.log(data)
            const serviceID = data.service.id

            const serviceToRemove = document.getElementById(serviceID);
            if (serviceToRemove) {
                serviceToRemove.remove();
                console.log('Элемент с ID', serviceID, 'удален из корзины.');
            } else {
                console.log('Элемент с ID', serviceID, 'не найден в корзине.');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    }
});