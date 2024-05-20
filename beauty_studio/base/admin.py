from django.contrib import admin
from .models import Service, Video, Image, Type, Gallery, Order, MessageForDirector

class ServiceAdmin(admin.ModelAdmin):
    filter_horizontal = ['images']

class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ['services']

admin.site.register(Service, ServiceAdmin)
admin.site.register(Video)
admin.site.register(Image)
admin.site.register(Type)
admin.site.register(Gallery)
admin.site.register(Order, OrderAdmin)
admin.site.register(MessageForDirector)