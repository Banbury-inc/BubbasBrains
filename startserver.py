## Python Script to run the dev server

import os

## Navigate to api folder

os.chdir("Scripts/api/projectname")

## Run the command gunicorn -c gunicorn_config_dev.py app:app

os.system("python3 manage.py runserver 192.168.1.51:4001")
