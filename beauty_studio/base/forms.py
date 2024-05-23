from django import forms
from .models import Order, MessageForDirector
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

# Получение ключа шифрования из переменных окружения
key = os.getenv('FERNET_KEY')
if not key:
    raise ValueError("No Fernet key found in environment variables. Please set FERNET_KEY in your .env file.")
cipher_suite = Fernet(key)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # Указываем только те поля, которые должны быть включены в форму
        fields = ['name', 'lastname', 'number']
        labels = {
            'name': 'Имя',
            'lastname': 'Фамилия',
            'number': 'Номер',
        }

    def __init__(self, *args, **kwargs):
        chosen_services_ids = kwargs.pop('chosen_services_ids', [])
        super(OrderForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)

        print("Данные перед шифрованием:")
        print("Имя:", self.cleaned_data['name'])
        print("Фамилия:", self.cleaned_data['lastname'])
        print("Номер:", self.cleaned_data['number'])

        # Шифрование данных и преобразование в строку
        instance.name = cipher_suite.encrypt(self.cleaned_data['name'].encode('utf-8')).decode('utf-8')
        instance.lastname = cipher_suite.encrypt(self.cleaned_data['lastname'].encode('utf-8')).decode('utf-8')
        instance.number = cipher_suite.encrypt(self.cleaned_data['number'].encode('utf-8')).decode('utf-8')

        print("Данные после шифрования:")
        print("Имя:", instance.name)
        print("Фамилия:", instance.lastname)
        print("Номер:", instance.number)

        if commit:
            instance.save()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        number = cleaned_data.get("number")
        if number:
            number_str = str(number)
            # Учитываем символы заполнителя в маске
            if len(number_str.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('_', '')) < 12:
                self.add_error('number', 'Пожалуйста, введите полный российский номер телефона.')
        return cleaned_data


class MessageForDirectorForm(forms.ModelForm):
    class Meta:
        model = MessageForDirector
        fields = ['name', 'lastname', 'number', 'text']
        labels = {
            'name': 'Имя',
            'lastname': 'Фамилия',
            'number': 'Номер',
            'text': 'Текст сообщения',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        print("Данные перед шифрованием:")
        print("Имя:", self.cleaned_data['name'])
        print("Фамилия:", self.cleaned_data['lastname'])
        print("Номер:", self.cleaned_data['number'])

        instance.name = cipher_suite.encrypt(self.cleaned_data['name'].encode('utf-8')).decode('utf-8')
        instance.lastname = cipher_suite.encrypt(self.cleaned_data['lastname'].encode('utf-8')).decode('utf-8')
        instance.number = cipher_suite.encrypt(self.cleaned_data['number'].encode('utf-8')).decode('utf-8')

        print("Данные после шифрования:")
        print("Имя:", instance.name)
        print("Фамилия:", instance.lastname)
        print("Номер:", instance.number)

        if commit:
            instance.save()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        number = cleaned_data.get("number")
        if number:
            number_str = str(number)
            # Учитываем символы заполнителя в маске
            if len(number_str.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('_', '')) < 12:
                self.add_error('number', 'Пожалуйста, введите полный российский номер телефона.')
        return cleaned_data