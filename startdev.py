## Python Script to run the dev server

import os

## Navigate to api folder

os.chdir("Scripts/api")

## Run the command gunicorn -c gunicorn_config_dev.py app:app

os.system("gunicorn -c gunicorn_config_dev.py app:app")
