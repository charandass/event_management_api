# Event Management application APIs.

These APIs are able to create an event , list all the events, update an event by super admin, and user can register himself, user can book event ticket, user can view his ticket, admin can see all events summary.



## Clone this repo to use this project.


## To Start configration this application you need to make virtual environment.

`virtualenv env_name`

## Activate virtual environment

```bash
# for linux
Source env/bin/activate
```

```bash
# for windows
env\Scripts\activate
```

## Install all the Required packages.

```bash
pip install -r requirements.txt
```

## Change the DATABASE connection in project folder settings.py
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_project_name',
        'USER': 'your_postgres_username',
        'PASSWORD': 'your_postgres_password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

## Run all the migrations and migrate the changes

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run the app
```bash
python manage.py runserver
```

## If you want to run the test
```bash
python manage.py test
```

## you can find all the apis json payload in this repo as well.


## JWT Authentication is implemented in this project.

## Quick Note:-
 you can register and login the user and get refresh token and access token and  with same login by using admin credentials you can get admin access token.

## You can create superadmin using this command
```bash
python manage.py createsuperuser
```


## You can run the project using docker

## Build the Docker image using the following command:
```bash
    docker build -t event_management_app .

```

## Start a PostgreSQL container:
```bash
docker run -d --name event_management_db -p 5432:5432 -e POSTGRES_DB=mydatabase -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword postgres
```

# Run the docker image
```bash
docker run -d -p 8000:8000 --name event_management_container --link event_management_db:postgres event_management_app

```
