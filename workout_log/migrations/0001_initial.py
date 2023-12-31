# Generated by Django 4.2.5 on 2023-10-13 01:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('isCompound', models.BooleanField()),
                ('equipment', models.CharField(choices=[('BB', 'Barbell'), ('DB', 'Dumbbells'), ('CB', 'Cables'), ('MC', 'Machine'), ('HB', 'Hexbar'), ('KB', 'Kettlebell'), ('RB', 'Resistance Band'), ('BW', 'Bodyweight')], max_length=2)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Muscle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('reps', models.IntegerField()),
                ('weight', models.FloatField()),
                ('index', models.IntegerField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='workout_log.exercise')),
                ('logged_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MuscleWorked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('directlyTargets', models.BooleanField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='workout_log.exercise')),
                ('muscle', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='workout_log.muscle')),
            ],
            options={
                'verbose_name_plural': 'muscles worked',
            },
        ),
    ]
