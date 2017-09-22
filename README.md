# djangorest-elektron

Following DjangoRest Tutorial: http://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/
Integrating with Devices Class.
Integrating postgre.


# To auto install everything

./appconfig.sh

# pip reqs

pip install -r pip_reqs.txt
pip freeze > pip_reqs.txt

# To restart model

>rm -rf "*00*"
>rm -rf "*.pyc"

>su postgres

postgres> psql
psql> DROP DATABASE elektron;
psql> CREATE DATABASE elektron;
psql> CREATE USER elektron;
psql> CREATE USER elekron WITH PASSWORD 'elektron';


exit pqsl (ctrl + D)
exit user postgres (ctrl + D)

>python manage.py makemigrations
>python manage.py migrate
>python manage.py createsuperuser
