# Generated by Django 4.2.5 on 2023-11-16 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition_log', '0004_goals'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goals',
            old_name='targetCalories',
            new_name='target_calories',
        ),
    ]
