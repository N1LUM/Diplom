# Generated by Django 5.0.4 on 2024-05-10 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_type_service_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='images',
            field=models.ManyToManyField(null=True, related_name='images', to='base.image'),
        ),
        migrations.AlterField(
            model_name='service',
            name='videos',
            field=models.ManyToManyField(null=True, related_name='videos', to='base.video'),
        ),
    ]
