#!/bin/sh
python manage.py makemigrations LotDividerAPI
python manage.py migrate LotDividerAPI
python manage.py runserver