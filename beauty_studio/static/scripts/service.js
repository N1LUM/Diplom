
const closeButton = document.getElementById('closeButton');
const cardOfService = document.getElementById('carOfService');
const overlayService = document.getElementById('overlayService');
closeButton.addEventListener('click', (e) => {
    // Получаем родительский элемент изображений
    var imageContainer = document.querySelector('.cardOfService_content__images');

    // Удаляем все дочерние элементы (изображения)
    while (imageContainer.firstChild) {
        imageContainer.removeChild(imageContainer.firstChild);
    }

    // Скрываем блок с данными о сервисе
    cardOfService.style.display = 'none';
    overlayService.style.display = 'none';
});

document.querySelectorAll('.cardOfServices_services__service').forEach(function(serviceCard) {
    serviceCard.addEventListener('click', function() {
        const serviceTitle = document.getElementById('serviceTitle');
        const serviceDescription = document.getElementById('serviceDescription');
        const serviceVideo = document.getElementById('serviceVideo');
        const serviceVideoSource = document.getElementById('serviceVideoSource');
        const serviceHours = document.getElementById('serviceHours');
        const serviceMinutes = document.getElementById('serviceMinutes');
        const serviceCost = document.getElementById('serviceCost');
        const cardOfService = document.getElementById('carOfService');
        const screenWidth = window.innerWidth;

        // Обработка данных перед парсингом JSON
        let serviceDataString = this.dataset.service.replace(/(?:\r\n|\r|\n)/g, " ");

        // Пытаемся распарсить JSON
        try {
            console.log(serviceDataString)

            const serviceData = JSON.parse(serviceDataString);

             console.log(serviceData)

            // Устанавливаем текстовое содержимое для каждого элемента
            serviceTitle.textContent = serviceData.title;
            serviceDescription.textContent = serviceData.description;

            serviceVideoSource.src = serviceData.video;
            serviceVideo.load();

            serviceHours.textContent = serviceData.hours + "ч";
            serviceMinutes.textContent = serviceData.minute + "мин";
            serviceCost.textContent = serviceData.cost + "руб";

            if (screenWidth > 1024) {
                serviceData.images.forEach(function(image) {
                    // Создание нового элемента <img>
                    var newImage = document.createElement('img');

                    // Установка класса для нового изображения
                    newImage.className = 'content_images__image';

                    // Установка атрибута src для нового изображения
                    newImage.src = image.url;

                    // Установка атрибута alt для нового изображения
                    newImage.alt = ' ';

                    // Добавление нового изображения в элемент с классом "cardOfService_content__images"
                    document.querySelector('.cardOfService_content__images').appendChild(newImage);
                });
            } else {
                serviceData.images.forEach(function(image, index) {
                    if (index === 0) {
                        // Создание нового элемента <img>
                        var newImage = document.createElement('img');

                        // Установка класса для нового изображения
                        newImage.className = 'content_images__image';

                        // Установка атрибута src для нового изображения
                        newImage.src = image.url;

                        // Установка атрибута alt для нового изображения
                        newImage.alt = ' ';

                        // Добавление нового изображения в элемент с классом "cardOfService_content__images"
                        document.querySelector('.cardOfService_content__images').appendChild(newImage);
                    }
                });
            }

            // Показываем блок с данными о сервисе
            cardOfService.style.display = 'flex';
            overlayService.style.display = 'block';
        } catch (error) {
            console.error("Ошибка при парсинге JSON:", error);
        }
    });
});

document.querySelectorAll('.cardOfServices_services__service').forEach(function(serviceCard) {
    serviceCard.addEventListener('click', function() {
        // Проверяем ширину экрана
        if (window.innerWidth <= 1024) {
            // Находим элемент .cardOfService_title внутри текущего .cardOfServices_services__service
            const titleElement = document.getElementById('serviceTitle');

            // Проверяем, что элемент найден
            if (titleElement) {
                // Получаем координаты элемента
                const titleElementRect = titleElement.getBoundingClientRect();
                // Прокручиваем страницу к текущему .cardOfService_title с учетом смещения вверх на 1024 пикселя
                window.scrollTo({
                    top: window.scrollY + titleElementRect.top - 1024,
                    behavior: 'smooth'
                });
            }
        }
    });
});
