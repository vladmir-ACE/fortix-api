# Generated by Django 4.2.5 on 2024-11-14 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pronostic', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pronostic',
            name='numbers',
        ),
        migrations.AddField(
            model_name='pronostic',
            name='banka',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='pronostic',
            name='perm',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='pronostic',
            name='two',
            field=models.CharField(max_length=255, null=True),
        ),
    ]