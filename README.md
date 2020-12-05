# TechTest

## Run Directory App
1. Goto the directory where requirements.txt file located run the below commands to install dependancies.

    conda create --name <env> --file requirements.txt
    

2. Navigate to directory folder where manage.py file located run the beloww commands.

    python manage.py makemigrations

    python manage.py migrate

3. Create default user (admin:admin1234).

    python manage.py createuser

4. Run application.

    python manage.py runserver
    
5. For bulk import upload csv file containing information about teacher and for images upload zip folder which contains the images. The csv format should be the same as the provided one with code.
