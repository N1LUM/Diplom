from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='./static/filesForService/')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='./static/filesForService/')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

class Type(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Тип услуг'

class Service(models.Model):
    title = models.CharField(max_length=100)
    hours = models.IntegerField(blank=False, null=False, default=0)
    minute = models.IntegerField(blank=False, null=False, default=0)
    cost = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    videos = models.OneToOneField(Video, related_name='videos', on_delete=models.SET_NULL, null=True, blank=True)
    images = models.ManyToManyField(Image, related_name='images', blank=True)
    type = models.ForeignKey(Type, related_name='type', on_delete=models.SET_NULL, null=True, unique=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.title}"

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Gallery(models.Model):
    title = models.CharField(max_length=100, default="Произведение")
    image = models.ImageField(upload_to='./static/filesForService/gallery/', null=False, default="")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Галлерея'
        verbose_name_plural = 'Галлереи'

class Order(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Имя')
    lastname = models.CharField(max_length=100, blank=False, null=False, verbose_name='Фамилия')
    number = models.CharField(max_length=100, blank=False, null=False, verbose_name='Номер')
    services = models.ManyToManyField(Service, related_name='chosenServices', null=False, verbose_name='Услуги')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.lastname} {self.number}"

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-created']

class MessageForDirector(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Имя')
    lastname = models.CharField(max_length=100, blank=False, null=False, verbose_name='Фамилия')
    number = models.CharField(max_length=100, blank=False, null=False, verbose_name='Номер')
    text = models.TextField(blank=False,null=True, verbose_name='Текст сообщения')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.lastname} {self.number}"

    class Meta:
        verbose_name = 'Сообщение обратной связи'
        verbose_name_plural = 'Сообщения обратной связи'
        ordering = ['-created']