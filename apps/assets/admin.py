from django.contrib import admin

from assets.models import State, ItemState, Item, ItemGroup, Person

admin.site.register(State)
admin.site.register(ItemState)
admin.site.register(Item)
admin.site.register(ItemGroup)
admin.site.register(Person)
