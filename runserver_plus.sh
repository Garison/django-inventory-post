#!/bin/sh
if [ -n "$1" ]; then
	./manage.py runserver_plus $1 --adminmedia ./django-inventory-site_media/admin_media/
else
	./manage.py runserver_plus --adminmedia ./django-inventory-site_media/admin_media/
fi
