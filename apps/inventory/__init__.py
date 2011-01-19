from django.utils.translation import ugettext_lazy as _

from models import Location
import assets


inventory_list = {'text':_('View all inventories'), 'view':'inventory_list'}
inventory_create = {'text':_('Create new inventory'), 'view':'inventory_create'}

inventory_transaction_list = {'text':_('View all transactions'), 'view':'inventory_transaction_list'}
inventory_transaction_create = {'text':_('Create new transaction'), 'view':'inventory_transaction_create'}

location_list = {'text':_('Locations'), 'view':'location_list'}
settings = {'text':_('Settings'), 'view':'settings'}

supplier_create = {'text':_('Create new supplier'), 'view':'supplier_create'}
supplier_list = {'text':_('Suppliers'), 'view':'supplier_list'}
supplier_delete = {'text':_('Delete'), 'view':'supplier_delete'}
supplier_update = {'text':_('Edit'), 'view':'supplier_update'}
supplier_assign_itemtemplate = {'text':_(u'Assign/Remove templates'), 'view':'supplier_assign_itemtemplates'}

template_assign_suppliers = {'text':_(u'Assign/Remove suppliers'), 'view':'template_assign_suppliers'}



template_menu_links = [
    {'text':_('View all'), 'view':'template_list'},
    {'text':_('Create new'), 'view':'template_create'},
    {'text':_('Orphans'), 'view':'template_orphans_list'},
]

template_record_links = [
    {'text':_(u'Edit'), 'view':'template_update'},
    {'text':_(u'Delete'), 'view':'template_delete'},
    {'text':_(u'Photos'), 'view':'template_photos'},
    {'text':_(u'Assets that use this template'), 'view':'template_items_list'},
    {'text':_(u'Assign/Remove supplies'), 'view':'template_assign_supply'},
    template_assign_suppliers
]


inventory_menu_links = [
    inventory_list, inventory_create, inventory_transaction_list, inventory_transaction_create
]


inventory_links = [
    {'text':_(u'Current balances'), 'view':'inventory_current'},
    {'text':_(u'Edit'), 'view':'inventory_update'},
    {'text':_(u'Delete'), 'view':'inventory_delete'},
]


inventory_transaction_links = [
    {'text':_(u'Edit'), 'view':'inventory_transaction_update'},
    {'text':_(u'Delete'), 'view':'inventory_transaction_delete'},
]

navigation = [
    {'text':_('Home'), 'view':'home', 'famfam':'house'},
    {'text':_('People'), 'view':'person_list', 'famfam':'group', 'links':[
        assets.person_list, assets.person_create
    ]},
    {'text':_('Templates'), 'view':'template_list', 'links':template_menu_links, 'famfam':'page'},
    {'text':_('Assets'), 'view':'item_list', 'links':[
        assets.asset_list, assets.asset_create, assets.asset_orphan_list, assets.group_list, assets.group_create 
    ]},
    {'text':_('Asset states'), 'view':'item_state_list_init'},
    {'text':_('Inventories'), 'view':'inventory_list', 'links':inventory_menu_links,'famfam':'book'},
    {'text':_('Tools'), 'view':'location_list', 'links': [
        location_list, assets.state_list, supplier_list, settings
    ],'famfam':'wrench'},
    {'text':_('Search'), 'view':'search', 'famfam':'zoom'},
    {'text':_('About'), 'view':'about'},
]
"""
navigation = [
    {'text':_('Home'), 'view':'home', 'famfam':'house'},
    {'text':_('People'), 'view':'person_list', 'famfam':'group', 'links':[
        person_list, person_create
    ]},
    {'text':_('Templates'), 'view':'template_list', 'links':template_menu_links, 'famfam':'page'},
    {'text':_('Assets'), 'view':'item_list', 'links':[
        asset_list, asset_create, asset_orphan_list, group_list, group_create 
    ]},
    {'text':_('Asset states'), 'view':'item_state_list_init'},
    {'text':_('Inventories'), 'view':'inventory_list', 'links':inventory_menu_links,'famfam':'book'},
    {'text':_('Tools'), 'view':'location_list', 'links': [
        location_list, state_list, supplier_list, settings
    ],'famfam':'wrench'},
    {'text':_('Search'), 'view':'search', 'famfam':'zoom'},
    {'text':_('About'), 'view':'about'},
]
"""

location_filter = {
    'location':{'queryset':Location.objects.all(), 'destination':'location'},
}

location_links = [
    {'text':_(u'Edit'), 'view':'location_update'},
    {'text':_(u'Delete'), 'view':'location_delete'},
]


suppliers_record_links = [
    supplier_delete, supplier_update, supplier_assign_itemtemplate
]
