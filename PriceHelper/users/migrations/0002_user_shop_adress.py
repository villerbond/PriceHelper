# Generated by Django 3.2.13 on 2023-12-20 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_shop',
            name='adress',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]