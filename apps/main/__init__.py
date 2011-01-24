from django.utils.translation import ugettext as _

import assets
import inventory
import movements

from assets.models import Item, Person, ItemGroup, State
from inventory.models import ItemTemplate, Inventory, InventoryTransaction, Supplier, Location

#object_navigation = {
#    Item:[assets.asset_edit, assets.asset_delete, assets.asset_photos, assets.asset_assign_person, assets.asset_template],
#    Person:[assets.person_update, assets.person_delete, assets.person_photos, assets.person_assign_item],
#    ItemGroup:[assets.group_update, assets.group_delete],
#    State:[assets.state_edit, assets.state_delete],
#    ItemTemplate:[inventory.template_update, inventory.template_delete, inventory.template_photos, inventory.template_assets, inventory.template_assign_supplies, inventory.template_assign_suppliers],
#    Supplier:[inventory.supplier_update, inventory.supplier_delete, inventory.supplier_assign_itemtemplate],
#    Inventory:[inventory.inventory_balances, inventory.inventory_update, inventory.inventory_delete],
#    InventoryTransaction:[inventory.inventory_transaction_update, inventory.inventory_transaction_delete],
#    Location:[inventory.location_update, inventory.location_delete],
#}

    
menu_navigation = [
    {'text':_('home'), 'view':'home', 'famfam':'house'},
    {'text':_('templates'), 'view':'template_list', 'links':inventory.template_menu_links, 'famfam':'page'},
    {'text':_('assets'), 'view':'item_list', 'links':[
        assets.asset_list, assets.asset_create, assets.asset_orphan_list, assets.group_list, assets.group_create, assets.person_list, assets.person_create 
    ], 'famfam':'computer'},
    {'text':_('inventories'), 'view':'inventory_list', 'links':inventory.inventory_menu_links,'famfam':'package_go'},
    {'text':_('tools'), 'view':'location_list', 'links': [
        inventory.location_list, assets.state_list, inventory.supplier_list, movements.purchase_request_state_list,
        {'text':_('import'), 'view':'import_wizard', 'famfam':'lightning_add'}
    ],'famfam':'wrench'},
    {'text':_('search'), 'view':'search', 'famfam':'zoom'},
    {'text':_('about'), 'view':'about'},
]
