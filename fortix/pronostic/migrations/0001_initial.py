# Generated by Django 4.2.5 on 2024-11-05 21:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jeux',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('heure', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Jour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pronostic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('numbers', models.CharField(max_length=255)),
                ('forcasseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.forcasseur')),
                ('jeu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pronostic.jeux')),
            ],
        ),
        migrations.AddField(
            model_name='jeux',
            name='jour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pronostic.jour'),
        ),
        migrations.AddField(
            model_name='jeux',
            name='pays',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.country'),
        ),
    ]