from django.contrib import admin

from inventory.models import ItemTemplate, Log, \
                             Inventory, Location, SubLocation, Supplier


class ItemTemplateAdmin(admin.ModelAdmin):
    filter_horizontal = ('supplies', 'suppliers')

#class SubmissionLocationAdmin(admin.ModelAdmin):
    #list_display = ('location')
    #list_display = ('completename')
 #    search_fields = ('location')
 #    def name(obj):
  #      return obj.Location.__unicode__()


admin.site.register(Location)
admin.site.register(Log)
admin.site.register(ItemTemplate, ItemTemplateAdmin)
admin.site.register(Inventory)
admin.site.register(Supplier)
admin.site.register(SubLocation)

