from inventory.models import *
from django.contrib import admin

mysite = admin.AdminSite()
mysite.register(CustomUser)
mysite.register(Permission)


