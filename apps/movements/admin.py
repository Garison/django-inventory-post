from django.contrib import admin

from models import PurchaseRequestStatus, PurchaseRequest, \
        PurchaseRequestItem, PurchaseOrderStatus, PurchaseOrderItemStatus, \
        PurchaseOrder, PurchaseOrderItem

class PurchaseRequestItemInline(admin.StackedInline):
    model = PurchaseRequestItem
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class PurchaseRequestAdmin(admin.ModelAdmin):
    inlines = [PurchaseRequestItemInline,]


class PurchaseOrderItemInline(admin.StackedInline):
    model = PurchaseOrderItem
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class PurchaseOrderAdmin(admin.ModelAdmin):
    inlines = [PurchaseOrderItemInline,]


admin.site.register(PurchaseRequestStatus)
admin.site.register(PurchaseRequest, PurchaseRequestAdmin)
admin.site.register(PurchaseRequestItem)
admin.site.register(PurchaseOrderStatus)
admin.site.register(PurchaseOrderItemStatus)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderItem)
