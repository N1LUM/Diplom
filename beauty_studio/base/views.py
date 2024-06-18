from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Service, Type, Gallery, Order, ConditionOfOrder
from .forms import OrderForm, MessageForDirectorForm
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from django.shortcuts import get_object_or_404
import os
import asyncio
import json

load_dotenv()

# Получение ключа шифрования из переменных окружения
key = os.getenv('FERNET_KEY')
if not key:
    raise ValueError("No Fernet key found in environment variables. Please set FERNET_KEY in your .env file.")
cipher_suite = Fernet(key)


def home(request):
    formCallBack = MessageForDirectorForm(request.POST or None)
    if request.method == 'POST':
        formCallBack = MessageForDirectorForm(request.POST)
        if formCallBack.is_valid():
            form_instance = formCallBack.save()
            form_instance.save()
            sendNotificationAboutCallBackFormToTelegram(form_instance)
            return redirect('completeForm')
        else:
            return render(request, 'home.html', {'formCallBack': formCallBack})

    context = {
        'formCallBack': formCallBack
    }
    return render(request, 'home.html', context)

def services(request):
    if request.method == 'POST':
        formCallBack = MessageForDirectorForm(request.POST)
        if formCallBack.is_valid():
            form_instance = formCallBack.save()
            form_instance.save()
            sendNotificationAboutCallBackFormToTelegram(form_instance)
            return redirect('completeForm')
        else:
            return render(request, 'services.html', {'formCallBack': formCallBack})
    else:
        formCallBack = MessageForDirectorForm()

    types = Type.objects.all()
    services = Service.objects.all()
    context = {
        "services": services,
        "types": types,
        "formCallBack": formCallBack
    }
    return render(request, 'services.html', context)

def order(request):
    if 'chosenServices' not in request.session:
        request.session['chosenServices'] = []

    form = OrderForm(chosen_services_ids=request.session.get('chosenServices', []))
    formCallBack = MessageForDirectorForm()

    if request.method == 'POST':
        if 'order_form_submit' in request.POST:
            form = OrderForm(request.POST, chosen_services_ids=request.session.get('chosenServices', []))
            if form.is_valid():
                order_instance = form.save(commit=False)
                chosen_service_ids = request.session.get('chosenServices', [])
                chosen_services = Service.objects.filter(pk__in=chosen_service_ids)
                order_instance.save()
                order_instance.services.set(chosen_services)
                del request.session['chosenServices']
                sendNotificationAboutOrderToTelegram(order_instance)
                return redirect('completeForm')
        elif 'callback_form_submit' in request.POST:
            formCallBack = MessageForDirectorForm(request.POST)
            if formCallBack.is_valid():
                form_instance = formCallBack.save()
                form_instance.save()
                sendNotificationAboutCallBackFormToTelegram(form_instance)
                return redirect('completeForm')
            else:
                return render(request, 'order.html', {'formCallBack': formCallBack})

    types = Type.objects.all()
    services = Service.objects.all()

    # Получаем список идентификаторов услуг из сессии
    chosen_service_ids = request.session.get('chosenServices', [])

    # Получаем объекты Service из базы данных по их идентификаторам
    chosenServices = Service.objects.filter(pk__in=chosen_service_ids)

    cost = 0
    hours = 0
    minutes = 0

    for service in chosenServices:
        cost += service.cost
        hours += service.hours
        minutes += service.minute

    if minutes >= 60:
        hours += 1
        minutes -= 60
    elif minutes >= 120:
        hours += 2
        minutes -= 120
    elif minutes >= 180:
        hours += 3
        minutes -= 180
    elif minutes >= 240:
        hours += 4
        minutes -= 240
    elif minutes >= 270:
        hours += 5
        minutes -= 270

    total = {
        "cost": cost,
        "hours": hours,
        "minutes": minutes,
    }

    context = {
        "form": form,
        "formCallBack": formCallBack,
        "services": services,
        "types": types,
        "chosenServices": chosenServices,
        "chosen_service_ids": chosen_service_ids,
        "total": total
    }
    return render(request, 'order.html', context)

def sendNotificationAboutOrderToTelegram(order):
    order_id = order.id
    decrypted_name = cipher_suite.decrypt(bytes(order.name.encode('utf-8'))).decode('utf-8')
    decrypted_lastname = cipher_suite.decrypt(bytes(order.lastname.encode('utf-8'))).decode('utf-8')
    decrypted_number = cipher_suite.decrypt(bytes(order.number.encode('utf-8'))).decode('utf-8')
    date_of_creating = order.created.strftime('%Y-%m-%d %H:%M:%S')

    bot_token = '7431207165:AAGEnZqak6p6J09Fx5nzOwcO29TaBlyuvak'
    chat_id = '1866798571'

    bot = Bot(token=bot_token)

    # Предполагаем, что у order есть поле services, которое является списком или QuerySet объектов Service
    service_titles = [service.title for service in order.services.all()]  # .all() если это QuerySet
    services_string = ', '.join(service_titles)

    message = (f"Запись от клиента \n\n"
               f"Идентификатор записи: {order_id}\n\n"
               f"Имя: {decrypted_name}\n\n"
               f"Фамилия: {decrypted_lastname}\n\n"
               f"Номер телефона: {decrypted_number}\n\n"
               f"Услуги: {services_string}\n\n"
               f"Дата записи: {date_of_creating}")

    # Определение асинхронной функции для отправки сообщения
    async def send_message_async():
        # Создаем кнопки
        keyboard = [
            [
                InlineKeyboardButton("Подтвердить", callback_data='confirm'),
                InlineKeyboardButton("Отменить", callback_data='cancel')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем сообщение с кнопками
        await bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    # Запуск асинхронной функции в блоке asyncio
    asyncio.run(send_message_async())

def sendNotificationAboutCallBackFormToTelegram(form):
    order_id = form.id
    decrypted_name = cipher_suite.decrypt(bytes(form.name.encode('utf-8'))).decode('utf-8')
    decrypted_lastname = cipher_suite.decrypt(bytes(form.lastname.encode('utf-8'))).decode('utf-8')
    decrypted_number = cipher_suite.decrypt(bytes(form.number.encode('utf-8'))).decode('utf-8')
    text = form.text
    date_of_creating = form.created.strftime('%Y-%m-%d %H:%M:%S')

    bot_token = '7431207165:AAGEnZqak6p6J09Fx5nzOwcO29TaBlyuvak'
    chat_id = '1866798571'

    bot = Bot(token=bot_token)

    message = (f"Обращение от пользователя\n\n"
               f"Идентификатор записи: {order_id}\n\n"
               f"Имя: {decrypted_name}\n\n"
               f"Фамилия: {decrypted_lastname}\n\n"
               f"Номер телефона: {decrypted_number}\n\n"
               f"Текст обращения: {text}\n\n"
               f"Дата обращения: {date_of_creating}")

    # Определение асинхронной функции для отправки сообщения
    async def send_message_async():
        await bot.send_message(chat_id=chat_id, text=message)

    # Запуск асинхронной функции в блоке asyncio
    asyncio.run(send_message_async())



def sendAllNotConfirmedOrdersToTelegram(request):
    orders = Order.objects.filter(confirmed__name="Не подтверждена")
    bot_token = '7431207165:AAGEnZqak6p6J09Fx5nzOwcO29TaBlyuvak'
    chat_id = '1866798571'

    bot = Bot(token=bot_token)

    async def send_message_async():
        # Создаем кнопки
        keyboard = [
            [
                InlineKeyboardButton("Подтвердить", callback_data='confirm'),
                InlineKeyboardButton("Отменить", callback_data='cancel')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем сообщение с кнопками
        await bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    for order in orders:
        order_id = order.id
        decrypted_name = cipher_suite.decrypt(bytes(order.name.encode('utf-8'))).decode('utf-8')
        decrypted_lastname = cipher_suite.decrypt(bytes(order.lastname.encode('utf-8'))).decode('utf-8')
        decrypted_number = cipher_suite.decrypt(bytes(order.number.encode('utf-8'))).decode('utf-8')
        date_of_creating = order.created.strftime('%Y-%m-%d %H:%M:%S')

        service_titles = [service.title for service in order.services.all()]
        services_string = ', '.join(service_titles)

        message = (f"Запись от клиента\n\n"
                   f"Идентификатор записи: {order_id}\n\n"
                   f"Имя: {decrypted_name}\n\n"
                   f"Фамилия: {decrypted_lastname}\n\n"
                   f"Номер телефона: {decrypted_number}\n\n"
                   f"Услуги: {services_string}\n\n"
                   f"Дата записи: {date_of_creating}")

        loop.run_until_complete(send_message_async())

    loop.close()

    return JsonResponse({'status': 'ok'})

def confirmOrder(request, order_id):
    order_instance = get_object_or_404(Order, pk=order_id)

    # Найти объект ConditionOfOrder с id=2 (предположим, что у вас есть такой объект)
    confirmed_condition = ConditionOfOrder.objects.get(pk=2)

    # Установить новое значение confirmed_id
    order_instance.confirmed_id = confirmed_condition.id
    order_instance.save()
    return JsonResponse({'status': 'ok'})
def cancelOrder(request, order_id):
    order_instance = get_object_or_404(Order, pk=order_id)

    # Найти объект ConditionOfOrder с id=2 (предположим, что у вас есть такой объект)
    confirmed_condition = ConditionOfOrder.objects.get(pk=3)

    # Установить новое значение confirmed_id
    order_instance.confirmed_id = confirmed_condition.id
    order_instance.save()
    return JsonResponse({'status': 'ok'})

def gallery(request):
    if request.method == 'POST':
        formCallBack = MessageForDirectorForm(request.POST)
        if formCallBack.is_valid():
            form_instance = formCallBack.save()
            form_instance.save()
            sendNotificationAboutCallBackFormToTelegram(form_instance)
            return redirect('completeForm')
        else:
            return render(request, 'gallery.html', {'formCallBack': formCallBack})
    else:
        formCallBack = MessageForDirectorForm()

    gallery = Gallery.objects.all()
    context = {"gallery": gallery, "formCallBack": formCallBack}
    return render(request, 'gallery.html', context)

def partnership(request):
    if request.method == 'POST':
        formCallBack = MessageForDirectorForm(request.POST)
        if formCallBack.is_valid():
            form_instance = formCallBack.save()
            form_instance.save()
            sendNotificationAboutCallBackFormToTelegram(form_instance)
            return redirect('completeForm')
        else:
            return render(request, 'partnership.html', {'formCallBack': formCallBack})
    else:
        formCallBack = MessageForDirectorForm()

    context = {"formCallBack": formCallBack}

    return render(request, 'partnership.html', context)


def privacy(request):
    if request.method == 'POST':
        formCallBack = MessageForDirectorForm(request.POST)
        if formCallBack.is_valid():
            form_instance = formCallBack.save()
            form_instance.save()
            sendNotificationAboutCallBackFormToTelegram(form_instance)
            return redirect('completeForm')
        else:
            return render(request, 'partnership.html', {'formCallBack': formCallBack})
    else:
        formCallBack = MessageForDirectorForm()

    context = {"formCallBack": formCallBack}

    return render(request, 'privacy.html', context)
def completeForm(request):
    formCallBack = MessageForDirectorForm(request.POST or None)
    if request.method == 'POST':
        formCallBack = MessageForDirectorForm(request.POST)
        if formCallBack.is_valid():
            form_instance = formCallBack.save()
            form_instance.save()
            sendNotificationAboutCallBackFormToTelegram(form_instance)
            return redirect('completeForm')
        else:
            return render(request, 'completeForm.html', {'formCallBack': formCallBack})

    context = {
        'formCallBack': formCallBack
    }
    return render(request, 'completeForm.html', context)

def add_to_chosen_services(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        service_id = data.get('service_id')
        try:
            service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            return JsonResponse({'error': f'Услуга с указанным ID {service_id} не найдена'}, status=404)

        # Сохраняем только идентификатор услуги в сессии
        chosen_services = request.session.get('chosenServices', [])
        chosen_services.insert(0, service_id)
        chosen_services = list(set(chosen_services))
        request.session['chosenServices'] = chosen_services

        # Возвращаем JSON-ответ с данными об объекте добавленной услуги
        serialized_service = {
            'id': service.id,
            'title': service.title,
            'hours': service.hours,
            'minute': service.minute,
            'cost': service.cost,
            'description': service.description,
            # Добавьте остальные поля, если необходимо
        }

        return JsonResponse({
            'service': serialized_service,
        })
    else:
        return JsonResponse({'error': 'Метод не поддерживается или запрос не AJAX'}, status=400)

def delete_from_chosen_services(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        service_id = data.get('service_id')

        # Сохраняем только идентификатор услуги в сессии
        chosen_services = request.session.get('chosenServices', [])
        chosen_services.remove(service_id)
        request.session['chosenServices'] = chosen_services

        # Возвращаем JSON-ответ с данными об объекте добавленной услуги
        serialized_service = {
            'success': True,
            'id': service_id,
        }

        return JsonResponse({
            'service': serialized_service,
        })
    else:
        return JsonResponse({'error': 'Метод не поддерживается или запрос не AJAX'}, status=400)