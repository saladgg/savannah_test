# DJANGO API SERVICE WITH UNITTEST, INTEGRATION TEST & CI/CD TO HEROKU

## Order API service

---

### Main External Libraries

    - Django
    - Django Rest Framework
    - Simple JWT
    - Gunicorn

## Installed apps

**customers app**

- Customer model - overrides django user model and is also the default auth model - UserAccessGroup - model for user authentication. Connects user to auth groups.

**orders app**

- Item model - this models the items that can be ordered by the registered customers - Order model - is the model for recording,listing and fetching customer orders

## Authentication and Authorization

    **access_control folder**
    - Authentication  - the custom_token.py contains a token based authentication logic. Overriding
        simplejwt classes to achieve the desired token pair.
    - Authorization - authenticated users are checked for predefined access implemented in user_permissions file.

## Installation

- clone the project
- navigate to the project directory and run;
- python -m venv venv to install virtual environment
- activate the venv by running source venv/bin/activate
- install the requirequirements by running pip install -r requirements.txt
- start the prj by running ./manage.py runserver

## Usage
