# Generated by Django 4.2.5 on 2025-01-17 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='portefeuille',
            name='gain',
            field=models.FloatField(default=0.0),
        ),
    ]
