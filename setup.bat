
@echo off
cd /d D:\AbroadProject

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install django djangorestframework

echo Creating Django project...
if not exist manage.py (
    django-admin startproject abroad_Project .
) else (
    echo Django project already exists, skipping creation...
)

echo Creating Django app...
if not exist abroad_app (
    django-admin startapp abroad_app
) else (
    echo Django app 'abroad_app' already exists, skipping creation...
)

echo Running migrations...
if exist manage.py (
    python manage.py migrate
) else (
    echo Error: manage.py not found in D:\AbroadProject
    exit /b 1
)

echo Creating superuser (default: abroad_admin/tomsaji123)...
echo Creating superuser...
set DJANGO_SUPERUSER_USERNAME=abroad_admin
set DJANGO_SUPERUSER_EMAIL=tomsaji20@gmail.com
set DJANGO_SUPERUSER_PASSWORD=tomsaji123
python manage.py createsuperuser --noinput


echo Starting Django server...
python manage.py runserver
