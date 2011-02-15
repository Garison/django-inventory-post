from django.utils.translation import ugettext_lazy as _

import assets
import inventory
import movements

from common.api import register_menu

from assets.models import Item, Person, ItemGroup, State
from inventory.models import ItemTemplate, Inventory, InventoryTransaction, Supplier, Location, SubLocation
    
register_menu([
    {'text':_(u'home'), 'view':'home', 'famfam':'house', 'position':0},

    {'text':_(u'tools'), 'view':'location_list', 'links': [
        inventory.location_list, inventory.sublocation_list, assets.state_list, 
        inventory.supplier_list,
        movements.purchase_request_state_list, 
        movements.purchase_order_state_list,
        movements.purchase_order_item_state_list,
        {'text':_(u'import'), 'view':'import_wizard', 'famfam':'lightning_add'},
    ],'famfam':'wrench', 'name':'tools','position':5},
    
    {'text':_(u'about'), 'view':'about', 'position':7},
])
