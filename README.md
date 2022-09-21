#How to run the program
Resource: https://flask.palletsprojects.com/en/2.2.x/tutorial/

#Setup Environment
pip install Flask
pip install pytest coverage

#Account
id: ryantj
pass: asdf1234

#How to run the app:
flask --app flaskr run

#How to initialize the db:
flask --app flaskr init-db

#Install our project as an app:
pip install yourproject.whl

#Install project in virtual environment
This tells pip to find setup.py in the current directory and install it in editable or development mode. Editable mode means that as you make changes to your local code, you’ll only need to re-install if you change the metadata about the project, such as its dependencies.
pip install -e .