from django.contrib import admin

from inventory.models import State, ItemState, \
                             ItemTemplate, Item, \
                             ItemGroup, Log, \
                             Person, Inventory, Location, Supplier


class ItemTemplateAdmin(admin.ModelAdmin):
    filter_horizontal = ('supplies', 'suppliers')


admin.site.register(Location)
admin.site.register(Log)
admin.site.register(ItemTemplate, ItemTemplateAdmin)
admin.site.register(Item)
admin.site.register(ItemGroup)
admin.site.register(Person)
admin.site.register(Inventory)
admin.site.register(State)
admin.site.register(ItemState)
admin.site.register(Supplier)


