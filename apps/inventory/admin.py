from django.contrib import admin

from inventory.models import State, ItemState, \
                             ItemTemplate, Item, \
                             ItemGroup, Log, \
                             Person, Inventory, Location


admin.site.register(Location)
admin.site.register(Log)
admin.site.register(ItemTemplate)
admin.site.register(Item)
admin.site.register(ItemGroup)
admin.site.register(Person)
admin.site.register(Inventory)
admin.site.register(State)
admin.site.register(ItemState)


