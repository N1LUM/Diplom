from django import forms
from .models import Order, MessageForDirector

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'lastname', 'number']
        labels = {
            'name': 'Имя',
            'lastname': 'Фамилия',
            'number': 'Номер',
        }
    def __init__(self, *args, **kwargs):
        chosen_services_ids = kwargs.pop('chosen_services_ids', [])
        super(OrderForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        number = cleaned_data.get("number")
        if number:
            number_str = str(number)
            # Учитываем символы заполнителя в маске
            if len(number_str.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('_', '')) < 10:
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
    def clean(self):
        cleaned_data = super().clean()
        number = cleaned_data.get("number")
        if number:
            number_str = str(number)
            # Учитываем символы заполнителя в маске
            if len(number_str.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('_', '')) < 10:
                self.add_error('number', 'Пожалуйста, введите полный российский номер телефона.')
        return cleaned_data