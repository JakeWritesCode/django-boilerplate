# Django-boilerplate
A general use boilerplate with all the standard stuff you're probably going to need 
for that next side-project of yours. 

I've been fairly opinionated here and used bootstrap and crispy forms for the front-end.

## Features:

This project has the following features implemented:
 - Basic PostgreSQL setup.
 - A really basic front end using bootstrap and django-crispy-forms.
 - An extended user model, with email in place of username.
 - Log-in, log-out, password reset by email.
 - Black, flake8 and isort configured with all code formatted.
 - Split out settings files for production and development.
 - Split out requirements files for production and dev.
 - A basic CircleCI config.


## Notes:
 - Keys and secrets in the settings file are stored in environment variables from the get
go.

## Environment Variables
To run this project you'll need to set the following environment variables:
- `DJANGO_SECRET_KEY` - Django secret key.
- `DEBUG` - Django debug mode (defaults to on for development and off for production).
- Postgres settings:
  - `POSTGRES_DB_NAME` - Database name.
  - `POSTGRES_DB_USER` - Database user.
  - `POSTGRES_DB_PASSWORD` - Database password.
  - `POSTGRES_DB_HOST` - Database server host IP.
  - `POSTGRES_DB_PORT` - Database server port.
- Email settings:
  - I've gone out on a limb here and assumed you'll use gmail. If not, change the email host 
and port to suit.
  - `OUTGOING_GMAIL_ADDRESS` - yourmum@gmail.com
  - `OUTGOING_GMAIL_APP_PASSWORD` - The app password for your account. *You need an app 
password, not your normal password!*

