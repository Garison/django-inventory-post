from django.contrib import admin

from models import PurchaseRequestStatus, PurchaseRequest, PurchaseRequestItem

class PurchaseRequestItemInline(admin.StackedInline):
    model = PurchaseRequestItem
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class PurchaseRequestAdmin(admin.ModelAdmin):
    inlines = [PurchaseRequestItemInline,]



admin.site.register(PurchaseRequestStatus)
admin.site.register(PurchaseRequest, PurchaseRequestAdmin)
admin.site.register(PurchaseRequestItem)
