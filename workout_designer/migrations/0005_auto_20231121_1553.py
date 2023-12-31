# Generated by Django 4.2.5 on 2023-11-21 15:53
#  This script creates some initial data for the Workout Designer.

# Once this script is migrated, modifications won't be saved 
#  (even after running migrate again)!! :/

from django.db import migrations

from workout_designer.models import DayType
import workout_log.constants as constants


def create_initial_data(apps, schema_editor):
    # Create day types
    day_types = apps.get_model('workout_designer', 'DayType').objects
    day_types.create(name=DayType.PUSH)
    day_types.create(name=DayType.PULL)
    day_types.create(name=DayType.LEGS)
    day_types.create(name=DayType.UPPER)
    day_types.create(name=DayType.LOWER)
    day_types.create(name=DayType.CHEST)
    day_types.create(name=DayType.BACK)
    day_types.create(name=DayType.SHOULDERS)
    day_types.create(name=DayType.ARMS)
    day_types.create(name=DayType.BC)
    day_types.create(name=DayType.SA)
    day_types.create(name=DayType.REST)

    # Create focii. Seems a little unbalanced. Lots of muscles for pull and upper. 
    # Might need to adjust later.
    focii = apps.get_model('workout_designer', 'Focus').objects
    muscles = apps.get_model('workout_log', 'Muscle').objects
    focii.create(day_type=day_types.get(name=DayType.PUSH), muscle=muscles.get(name=constants.UPPER_CHEST))
    focii.create(day_type=day_types.get(name=DayType.PUSH), muscle=muscles.get(name=constants.LOWER_CHEST))
    focii.create(day_type=day_types.get(name=DayType.PUSH), muscle=muscles.get(name=constants.TRICEPS))
    focii.create(day_type=day_types.get(name=DayType.PUSH), muscle=muscles.get(name=constants.FRONT_DELTS))
    focii.create(day_type=day_types.get(name=DayType.PUSH), muscle=muscles.get(name=constants.LATERAL_DELTS))
    focii.create(day_type=day_types.get(name=DayType.PULL), muscle=muscles.get(name=constants.UPPER_TRAPS))
    focii.create(day_type=day_types.get(name=DayType.PULL), muscle=muscles.get(name=constants.LOWER_TRAPS))
    focii.create(day_type=day_types.get(name=DayType.PULL), muscle=muscles.get(name=constants.LATS))
    focii.create(day_type=day_types.get(name=DayType.PULL), muscle=muscles.get(name=constants.SPINAL_ERECTORS))
    focii.create(day_type=day_types.get(name=DayType.PULL), muscle=muscles.get(name=constants.REAR_DELTS))
    focii.create(day_type=day_types.get(name=DayType.PULL), muscle=muscles.get(name=constants.BICEPS))
    focii.create(day_type=day_types.get(name=DayType.PULL), muscle=muscles.get(name=constants.FOREARMS))
    focii.create(day_type=day_types.get(name=DayType.LEGS), muscle=muscles.get(name=constants.QUADRICEPS))
    focii.create(day_type=day_types.get(name=DayType.LEGS), muscle=muscles.get(name=constants.HAMSTRINGS))
    focii.create(day_type=day_types.get(name=DayType.LEGS), muscle=muscles.get(name=constants.GLUTES))
    focii.create(day_type=day_types.get(name=DayType.LEGS), muscle=muscles.get(name=constants.CALVES))
    focii.create(day_type=day_types.get(name=DayType.LEGS), muscle=muscles.get(name=constants.ABS))
    focii.create(day_type=day_types.get(name=DayType.UPPER), muscle=muscles.get(name=constants.UPPER_CHEST))
    focii.create(day_type=day_types.get(name=DayType.UPPER), muscle=muscles.get(name=constants.LOWER_CHEST))
    focii.create(day_type=day_types.get(name=DayType.UPPER), muscle=muscles.get(name=constants.TRICEPS))
    focii.create(day_type=day_types.get(name=DayType.UPPER), muscle=muscles.get(name=constants.FRONT_DELTS))
    focii.create(day_type=day_types.get(name=DayType.UPPER), muscle=muscles.get(name=constants.LATERAL_DELTS))
    focii.create(day_type=day_types.get(name=DayType.UPPER), muscle=muscles.get(name=constants.UPPER_TRAPS))
    focii.create(day_type=day_types.get(name=DayType.UPPER), muscle=muscles.get(name=constants.LOWER_TRAPS))
    focii.create(day_type=day_types.get(name=DayType.UPPER), muscle=muscles.get(name=constants.LATS))
    focii.create(day_type=day_types.get(name=DayType.UPPER), muscle=muscles.get(name=constants.REAR_DELTS))
    focii.create(day_type=day_types.get(name=DayType.UPPER), muscle=muscles.get(name=constants.BICEPS))
    focii.create(day_type=day_types.get(name=DayType.UPPER), muscle=muscles.get(name=constants.FOREARMS))
    focii.create(day_type=day_types.get(name=DayType.LOWER), muscle=muscles.get(name=constants.QUADRICEPS))
    focii.create(day_type=day_types.get(name=DayType.LOWER), muscle=muscles.get(name=constants.HAMSTRINGS))
    focii.create(day_type=day_types.get(name=DayType.LOWER), muscle=muscles.get(name=constants.GLUTES))
    focii.create(day_type=day_types.get(name=DayType.LOWER), muscle=muscles.get(name=constants.CALVES))
    focii.create(day_type=day_types.get(name=DayType.LOWER), muscle=muscles.get(name=constants.ABS))
    focii.create(day_type=day_types.get(name=DayType.LOWER), muscle=muscles.get(name=constants.SPINAL_ERECTORS))
    focii.create(day_type=day_types.get(name=DayType.CHEST), muscle=muscles.get(name=constants.UPPER_CHEST))
    focii.create(day_type=day_types.get(name=DayType.CHEST), muscle=muscles.get(name=constants.LOWER_CHEST))
    focii.create(day_type=day_types.get(name=DayType.BACK), muscle=muscles.get(name=constants.UPPER_TRAPS))
    focii.create(day_type=day_types.get(name=DayType.BACK), muscle=muscles.get(name=constants.LOWER_TRAPS))
    focii.create(day_type=day_types.get(name=DayType.BACK), muscle=muscles.get(name=constants.SPINAL_ERECTORS))
    focii.create(day_type=day_types.get(name=DayType.BACK), muscle=muscles.get(name=constants.LATS))
    focii.create(day_type=day_types.get(name=DayType.SHOULDERS), muscle=muscles.get(name=constants.FRONT_DELTS))
    focii.create(day_type=day_types.get(name=DayType.SHOULDERS), muscle=muscles.get(name=constants.LATERAL_DELTS))
    focii.create(day_type=day_types.get(name=DayType.SHOULDERS), muscle=muscles.get(name=constants.REAR_DELTS))
    focii.create(day_type=day_types.get(name=DayType.ARMS), muscle=muscles.get(name=constants.FOREARMS))
    focii.create(day_type=day_types.get(name=DayType.ARMS), muscle=muscles.get(name=constants.BICEPS))
    focii.create(day_type=day_types.get(name=DayType.ARMS), muscle=muscles.get(name=constants.TRICEPS))
    focii.create(day_type=day_types.get(name=DayType.BC), muscle=muscles.get(name=constants.UPPER_CHEST))
    focii.create(day_type=day_types.get(name=DayType.BC), muscle=muscles.get(name=constants.LOWER_CHEST))
    focii.create(day_type=day_types.get(name=DayType.BC), muscle=muscles.get(name=constants.UPPER_TRAPS))
    focii.create(day_type=day_types.get(name=DayType.BC), muscle=muscles.get(name=constants.LOWER_TRAPS))
    focii.create(day_type=day_types.get(name=DayType.BC), muscle=muscles.get(name=constants.SPINAL_ERECTORS))
    focii.create(day_type=day_types.get(name=DayType.BC), muscle=muscles.get(name=constants.LATS))
    focii.create(day_type=day_types.get(name=DayType.SA), muscle=muscles.get(name=constants.FRONT_DELTS))
    focii.create(day_type=day_types.get(name=DayType.SA), muscle=muscles.get(name=constants.LATERAL_DELTS))
    focii.create(day_type=day_types.get(name=DayType.SA), muscle=muscles.get(name=constants.REAR_DELTS))
    focii.create(day_type=day_types.get(name=DayType.SA), muscle=muscles.get(name=constants.FOREARMS))
    focii.create(day_type=day_types.get(name=DayType.SA), muscle=muscles.get(name=constants.BICEPS))
    focii.create(day_type=day_types.get(name=DayType.SA), muscle=muscles.get(name=constants.TRICEPS))
    

class Migration(migrations.Migration):

    dependencies = [
        ('workout_designer', '0004_alter_day_day_type'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
