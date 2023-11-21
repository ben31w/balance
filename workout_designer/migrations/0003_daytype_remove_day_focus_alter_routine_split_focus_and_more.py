# Generated by Django 4.2.5 on 2023-11-21 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workout_log', '0005_auto_20231121_1500'),
        ('workout_designer', '0002_alter_day_focus'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('PUSH', 'Push'), ('PULL', 'Pull'), ('LEGS', 'Legs'), ('UPPER', 'Upper'), ('LOWER', 'Lower'), ('CHEST', 'Chest'), ('BACK', 'Back'), ('SHOULDERS', 'Shoulders'), ('ARMS', 'Arms'), ('BC', 'Back-Chest'), ('SA', 'Shoulders-Arms'), ('REST', 'Rest')], max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='day',
            name='focus',
        ),
        migrations.AlterField(
            model_name='routine',
            name='split',
            field=models.CharField(choices=[('ARN', 'Arnold'), ('BRO', 'Bro'), ('PPL', 'Push-Pull-Legs'), ('UL', 'Upper-Lower')], max_length=3),
        ),
        migrations.CreateModel(
            name='Focus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='workout_designer.daytype')),
                ('muscle', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='workout_log.muscle')),
            ],
            options={
                'verbose_name_plural': 'focii',
            },
        ),
        migrations.AddField(
            model_name='day',
            name='day_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='workout_designer.daytype'),
            preserve_default=False,
        ),
    ]
