# Generated by Django 5.0.6 on 2024-05-21 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_rename_text_messagefordirector_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=models.ImageField(default='', upload_to='./static/filesForGallery/'),
        ),
    ]
