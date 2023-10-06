## Python Script to run the dev server

import os

## Navigate to api folder

os.chdir("Scripts/api/projectname")

## Run the command gunicorn -c gunicorn_config_dev.py app:app

os.system("python manage.py runserver")