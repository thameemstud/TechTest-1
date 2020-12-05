# TechTest

## Run Directory App
1. Goto the directory where requirements.txt file located run the below commands to install dependancies.

    pip install -r requirements.txt

2. Navigate to directory folder where manage.py file located run the beloww commands.

    python manage.py makemigrations

    python manage.py migrate

3. Create default user (admin:admin1234).

    python manage.py createuser

4. Run application.

    python manage.py runserver
