from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Service, Type, Gallery
from .forms import OrderForm, MessageForDirectorForm
import json
from django.core import serializers


def home(request):
    formCallBack = MessageForDirectorForm(request.POST or None)
    if request.method == 'POST':
        formCallBack = MessageForDirectorForm(request.POST)
        if formCallBack.is_valid():
            formCallBack.save()
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
            formCallBack.save()
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
                return redirect('completeForm')
        elif 'callback_form_submit' in request.POST:
            formCallBack = MessageForDirectorForm(request.POST)
            if formCallBack.is_valid():
                formCallBack.save()
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
        "formCallBack":formCallBack,
        "services": services,
        "types": types,
        "chosenServices": chosenServices,
        "chosen_service_ids": chosen_service_ids,
        "total": total
    }
    return render(request, 'order.html', context)

def gallery(request):
    if request.method == 'POST':
        formCallBack = MessageForDirectorForm(request.POST)
        if formCallBack.is_valid():
            formCallBack.save()
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
            formCallBack.save()
            return redirect('completeForm')
        else:
            return render(request, 'partnership.html', {'formCallBack': formCallBack})
    else:
        formCallBack = MessageForDirectorForm()

    context = {"formCallBack": formCallBack}

    return render(request, 'partnership.html', context)

def completeForm(request):
    formCallBack = MessageForDirectorForm(request.POST or None)
    if request.method == 'POST':
        formCallBack = MessageForDirectorForm(request.POST)
        if formCallBack.is_valid():
            formCallBack.save()
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