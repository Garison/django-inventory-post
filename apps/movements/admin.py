from django.contrib import admin

from models import PurchaseRequestStatus, PurchaseRequest


admin.site.register(PurchaseRequestStatus)
admin.site.register(PurchaseRequest)
