# Summary

Balance is a web app that provides tools for tracking your exercises 
and calories, and generating workout routines. By providing intuitive 
tools and data visualzations, Balance can help anyone create a sustainable fitness 
routine and achieve Fitness-Life Balance.

# Components & Features
- Workout Log
  - Log your sets at the gym on any day.
  - See your volume for each muscle over any timeframe. This is useful for identifying weak spots 
     and preventing muscle imbalance
  - See your progress for any exercise over time via line charts. This is useful for ensuring progressive
     overload is reached, which is critical for building muscle.
- Nutrition Log
  - Log your weight and calories for any day
  - See your average weight and calories over any timeframe
  - See your weight and calorie progress over time via line charts. This helps you stay on top of your 
     body goals.
- Workout Designer
  - Inputs your preferred workout schedule, time willing to commit to a workout, and desired split
     (Push-Pull-Legs, Upper-Lower)
  - Outputs a custom routine tailored to your needs


# Project Structure
Root directory folders:
- `balance`: contains project-wide settings and URL configurations
- `commons`: resources that are shared among various apps
- `nutrition_log`: files for the Nutrition Log app
- `users`: files for user authentication
- `workout_designer`: files for the Workout Designer app
- `workout_log`: files for the Workout Log app

Root directory files:
- `manage.py`: a script used to run the project and issue development/administrative commands
- `requirements.txt`: list of pip packages required for this project
