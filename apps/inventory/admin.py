from django.contrib import admin

from inventory.models import CustomUser, Permission, RegionalOffice, \
                             Department, Supply, ItemTemplate, Item, \
                             ItemGroup, RetiredItem, InRepairsItem, \
                             Person, Inventory


admin.site.register(CustomUser)
admin.site.register(Permission)
admin.site.register(RegionalOffice)
admin.site.register(Department)
admin.site.register(Supply)
admin.site.register(ItemTemplate)
admin.site.register(Item)
admin.site.register(ItemGroup)
admin.site.register(RetiredItem)
admin.site.register(InRepairsItem)
admin.site.register(Person)
admin.site.register(Inventory)


