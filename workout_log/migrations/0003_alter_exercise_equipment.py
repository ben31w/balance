# Generated by Django 4.2.5 on 2023-11-21 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout_log', '0002_alter_exercise_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='equipment',
            field=models.CharField(choices=[('BB', 'Barbell'), ('DB', 'Dumbbells'), ('C', 'Cables'), ('M', 'Machine'), ('SM', 'Smith Machine'), ('HB', 'Hexbar'), ('KB', 'Kettlebell'), ('RB', 'Resistance Band'), ('BW', 'Bodyweight')], max_length=2),
        ),
    ]
