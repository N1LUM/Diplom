from django.db import models
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

# Получение ключа шифрования из переменных окружения
key = os.getenv('FERNET_KEY')
if not key:
    raise ValueError("No Fernet key found in environment variables. Please set FERNET_KEY in your .env file.")
cipher_suite = Fernet(key)

# Create your models here.
class ConditionOfOrder(models.Model):
    name = models.CharField(max_length=120, verbose_name="Название состояния записи")
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлена в')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создана в')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Состояние записи'
        verbose_name_plural = 'Состояния записи'
class Video(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    video = models.FileField(upload_to='./static/filesForService/', verbose_name='Видео')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлена в')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создана в')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

class Image(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(upload_to='./static/filesForService/', verbose_name='Фото')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлена в')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создана в')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

class Type(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название типа услуги')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлена в')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создана в')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Тип услуг'

class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    hours = models.IntegerField(blank=False, null=False, default=0, verbose_name='Часов')
    minute = models.IntegerField(blank=False, null=False, default=0, verbose_name='Минут')
    cost = models.IntegerField(blank=True, null=True, verbose_name='Стоимость')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    videos = models.OneToOneField(Video, related_name='videos', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Видео')
    images = models.ManyToManyField(Image, related_name='images', blank=True, verbose_name='Фото')
    type = models.ForeignKey(Type, related_name='type', on_delete=models.SET_NULL, null=True, unique=False, verbose_name='Тип услуги')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлена в')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создана в')

    def __str__(self):
        return f"{self.id}: {self.title}"

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Gallery(models.Model):
    title = models.CharField(max_length=100, default="Произведение", verbose_name='Название')
    image = models.ImageField(upload_to='./static/filesForGallery/', null=False, default="", verbose_name='Фото')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлена в')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создана в')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Галлерея'
        verbose_name_plural = 'Галлереи'

class Order(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Имя')
    lastname = models.CharField(max_length=255, blank=False, null=False, verbose_name='Фамилия')
    number = models.CharField(max_length=255, blank=False, null=False, verbose_name='Номер')
    services = models.ManyToManyField('Service', related_name='chosenServices', verbose_name='Услуги')
    confirmed = models.ForeignKey(ConditionOfOrder, related_name='confirmed', on_delete=models.SET_NULL, null=True, unique=False, verbose_name='Запись подтверждена')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлена в')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создана в')

    def decrypt_name(self):
        try:
            decrypted_name = cipher_suite.decrypt(self.name.encode('utf-8')).decode('utf-8')
            return decrypted_name
        except Exception as e:
            print(f"Error decrypting name: {e}")
            return None

    def decrypt_lastname(self):
        try:
            decrypted_lastname = cipher_suite.decrypt(self.lastname.encode('utf-8')).decode('utf-8')
            return decrypted_lastname
        except Exception as e:
            print(f"Error decrypting lastname: {e}")
            return None

    def decrypt_number(self):
        try:
            decrypted_number = cipher_suite.decrypt(self.number.encode('utf-8')).decode('utf-8')
            return decrypted_number
        except Exception as e:
            print(f"Error decrypting number: {e}")
            return None

    def __str__(self):
        return f"{self.decrypt_name()} {self.decrypt_lastname()} {self.decrypt_number()}"

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-created']

class MessageForDirector(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Имя')
    lastname = models.CharField(max_length=255, blank=False, null=False, verbose_name='Фамилия')
    number = models.CharField(max_length=255, blank=False, null=False, verbose_name='Номер')
    text = models.TextField(blank=False, null=True, verbose_name='Текст сообщения')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлена в')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создана в')

    def decrypt_name(self):
        try:
            decrypted_name = cipher_suite.decrypt(self.name.encode('utf-8')).decode('utf-8')
            return decrypted_name
        except Exception as e:
            print(f"Error decrypting name: {e}")
            return None

    def decrypt_lastname(self):
        try:
            decrypted_lastname = cipher_suite.decrypt(self.lastname.encode('utf-8')).decode('utf-8')
            return decrypted_lastname
        except Exception as e:
            print(f"Error decrypting lastname: {e}")
            return None

    def decrypt_number(self):
        try:
            decrypted_number = cipher_suite.decrypt(self.number.encode('utf-8')).decode('utf-8')
            return decrypted_number
        except Exception as e:
            print(f"Error decrypting number: {e}")
            return None

    def __str__(self):
        return f"{self.decrypt_name()} {self.decrypt_lastname()} {self.decrypt_number()}"

    class Meta:
        verbose_name = 'Сообщение обратной связи'
        verbose_name_plural = 'Сообщения обратной связи'
        ordering = ['-created']