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


# How to run the project

Balance is a locally hosted web app. 
You need to launch the web server from a command line interface to use the app. 

<b>Steps for running the first time:</b>

1. Clone the project to your computer using 

`git clone https://student-gitlab.pcs.cnu.edu/benjamin.wright.20-cpsc498-f23/balance.git`

2. Make and activate a virtual environment in a directory of your choice.

`python -m venv path/to/virtual-env`

`source path/to/virtual-env/bin/activate`

3. With the virtual environment activated, navigate to the project's root directory (`cd wherever/you/cloned/it/balance`) and install the project's dependencies with

`pip install -r requirements.txt`

4. In the root directoy, populate the database with initial data using 

`python manage.py migrate`

5. In the root directory, launch the web server using 

`python manage.py runserver`


<b>Steps for running subsequent times:</b>

1. Activate the virtual environment you created for this project.

`source path/to/virtual-env/bin/activate`

2. With the virtual environment activated, navigate to the project's root directory (`cd wherever/you/cloned/it/balance`) and launch the web server using 

`python manage.py runserver`
