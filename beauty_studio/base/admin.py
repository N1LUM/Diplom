from django.contrib import admin
from .models import Service, Video, Image, Type, Gallery, Order, MessageForDirector, ConditionOfOrder

class ServiceAdmin(admin.ModelAdmin):
    filter_horizontal = ['images']
    list_display = ('title', 'hours', 'minute', 'cost', 'description',  'type', 'updated', 'created')

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video', 'updated', 'created')

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'updated', 'created')

class TypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated', 'created')

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'updated', 'created')

class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ['services']
    list_display = ('decrypt_name', 'decrypt_lastname', 'decrypt_number', 'confirmed', 'updated', 'created')

class MessageForDirectorAdmin(admin.ModelAdmin):
    list_display = ('decrypt_name', 'decrypt_lastname', 'decrypt_number', 'text', 'updated', 'created')

class ConditionOfOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated', 'created')

admin.site.register(Service, ServiceAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(MessageForDirector, MessageForDirectorAdmin)
admin.site.register(ConditionOfOrder, ConditionOfOrderAdmin)