# Django Toko Online

An online shop app build with Django and Bootstrap 5

## Features

### Admin Panel

    - Manage accounts
    - CRUD category
    - CRUD product
    - CRUD variations
    - Manage cart and items

### Authentication

    - Register
    - Login
    - Logout
    - User activation using email
    - Forgot password

### User Functionality

    - Index page
    - Product page
    - Search
    - Product details
    - Manage Cart (Add to cart, increase quantity, decrease quantity, remove an item)
    - Filter by category

## Installation

#### Create virtual environment and activate the virtual environment

```bash
  python -m venv env
  source env/Scripts/activate
```

#### Install libraries

```bash
  pip install django==3.2
  pip install pillow
  pip install django-decouple
```

#### Copy and paste .env-example and rename it to .env

#### Generate Secret key and put it into .env file

```bash
  python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
```

#### Migrate database

```bash
  python manage.py migrate
```

#### Run server

```bash
  python manage.py runserver
```
