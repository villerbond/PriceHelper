# Generated by Django 3.2.13 on 2023-12-20 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='adress',
        ),
        migrations.AddField(
            model_name='price',
            name='date_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
