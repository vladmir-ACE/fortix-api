# Generated by Django 4.2.5 on 2024-11-26 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pronostic', '0002_remove_pronostic_numbers_pronostic_banka_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pronostic',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
