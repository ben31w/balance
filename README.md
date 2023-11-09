# Summary

For people who are serious about transforming their body, 
logging exercises and calories is essential. For people starting 
their fitness journey, it is critical that they learn good exercise 
and diet practices in order to create an enjoyable routine. No matter
your background, Balance can help anyone create a sustainable fitness 
routine and achieve Fitness-Life Balance.

Balance will be a web app that can be accessed from any browser on any
device. Balance will provide intuitive tools for tracking your exercises 
and calories, with charts to visualize your progressive overload, 
calorie intake, and body weight over time. Balance will also provide
an algorithm that can generate a workout routine tailored to any 
individual needs and goals. Balance is here to make the process of 
fitness fun and easy.

# Project Structure
Balance is built using Django, a Python web development framework. 
A Django project is composed of apps that serve a specific function.

Root directory folders:
- `balance`: contains settings and URL configurations for the entire project
- `commons`: app containing resources that are shared throughout all the 
other apps, like a base.html for other pages to inherit from
- `users`: app containing user authentication files
- `workout_log`: files for the Workout Log app
- `nutrition_log`: files for the Nutrition Log app

Root directory files:
- `manage.py`: created by Django for development use
- `requirements.txt`: list of pip packages required for this project
