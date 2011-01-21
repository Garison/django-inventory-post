from django.utils.translation import ugettext_lazy as _

from models import Location
import assets


inventory_list = {'text':_('view all inventories'), 'view':'inventory_list'}
inventory_create = {'text':_('create new inventory'), 'view':'inventory_create'}

inventory_transaction_list = {'text':_('view all transactions'), 'view':'inventory_transaction_list'}
inventory_transaction_create = {'text':_('create new transaction'), 'view':'inventory_transaction_create'}

location_list = {'text':_('locations'), 'view':'location_list', 'famfam':'map'}

supplier_create = {'text':_('create new supplier'), 'view':'supplier_create'}
supplier_list = {'text':_('suppliers'), 'view':'supplier_list', 'famfam':'lorry'}
supplier_delete = {'text':_('delete'), 'view':'supplier_delete'}
supplier_update = {'text':_('edit'), 'view':'supplier_update'}
supplier_assign_itemtemplate = {'text':_(u'assign/remove templates'), 'view':'supplier_assign_itemtemplates'}

template_assign_suppliers = {'text':_(u'assign/remove suppliers'), 'view':'template_assign_suppliers'}

template_menu_links = [
    {'text':_('view all'), 'view':'template_list'},
    {'text':_('create new'), 'view':'template_create'},
    {'text':_('orphans'), 'view':'template_orphans_list'},
]

template_record_links = [
    {'text':_(u'edit'), 'view':'template_update'},
    {'text':_(u'delete'), 'view':'template_delete'},
    {'text':_(u'photos'), 'view':'template_photos'},
    {'text':_(u'assets that use this template'), 'view':'template_items_list'},
    {'text':_(u'assign/remove supplies'), 'view':'template_assign_supply'},
    template_assign_suppliers
]


inventory_menu_links = [
    inventory_list, inventory_create, inventory_transaction_list, inventory_transaction_create
]


inventory_links = [
    {'text':_(u'current balances'), 'view':'inventory_current'},
    {'text':_(u'edit'), 'view':'inventory_update'},
    {'text':_(u'delete'), 'view':'inventory_delete'},
]


inventory_transaction_links = [
    {'text':_(u'edit'), 'view':'inventory_transaction_update'},
    {'text':_(u'delete'), 'view':'inventory_transaction_delete'},
]

navigation = [
    {'text':_('home'), 'view':'home', 'famfam':'house'},
    {'text':_('people'), 'view':'person_list', 'famfam':'group', 'links':[
        assets.person_list, assets.person_create
    ]},
    {'text':_('templates'), 'view':'template_list', 'links':template_menu_links, 'famfam':'page'},
    {'text':_('assets'), 'view':'item_list', 'links':[
        assets.asset_list, assets.asset_create, assets.asset_orphan_list, assets.group_list, assets.group_create 
    ], 'famfam':'computer'},
    {'text':_('asset states'), 'view':'item_state_list_init', 'famfam':'computer_error'},
    {'text':_('inventories'), 'view':'inventory_list', 'links':inventory_menu_links,'famfam':'book'},
    {'text':_('tools'), 'view':'location_list', 'links': [
        location_list, assets.state_list, supplier_list,
        {'text':_('import'), 'view':'import_wizard'}
    ],'famfam':'wrench'},
    {'text':_('search'), 'view':'search', 'famfam':'zoom'},
    {'text':_('about'), 'view':'about'},
]

location_filter = {
    'location':{'queryset':Location.objects.all(), 'destination':'location'},
}

location_links = [
    {'text':_(u'edit'), 'view':'location_update'},
    {'text':_(u'delete'), 'view':'location_delete'},
]


suppliers_record_links = [
    supplier_delete, supplier_update, supplier_assign_itemtemplate
]
