from django.utils.translation import ugettext_lazy as _

from models import Location
import assets


inventory_list = {'text':_('view all inventories'), 'view':'inventory_list', 'famfam':'package_go'}
inventory_create = {'text':_('create new inventory'), 'view':'inventory_create', 'famfam':'package_add'}
inventory_balances = {'text':_(u'current balances'), 'view':'inventory_current', 'args':'object.id', 'famfam':'book_addresses'}
inventory_update = {'text':_(u'edit'), 'view':'inventory_update', 'args':'object.id', 'famfam':'package_green'}
inventory_delete = {'text':_(u'delete'), 'view':'inventory_delete', 'args':'object.id', 'famfam':'package_delete'}

inventory_transaction_list = {'text':_('view all transactions'), 'view':'inventory_transaction_list', 'famfam':'book_go'}
inventory_transaction_create = {'text':_('create new transaction'), 'view':'inventory_transaction_create', 'famfam':'book_add'}
inventory_transaction_update = {'text':_(u'edit'), 'view':'inventory_transaction_update', 'args':'object.id', 'famfam':'book_add'}
inventory_transaction_delete = {'text':_(u'delete'), 'view':'inventory_transaction_delete', 'args':'object.id', 'famfam':'book_delete'}

location_list = {'text':_('locations'), 'view':'location_list', 'famfam':'map'}
location_update = {'text':_(u'edit'), 'view':'location_update', 'args':'object.id', 'famfam':'map_edit'}
location_delete = {'text':_(u'delete'), 'view':'location_delete', 'args':'object.id', 'famfam':'map_delete'}

supplier_create = {'text':_('create new supplier'), 'view':'supplier_create'}
supplier_list = {'text':_('suppliers'), 'view':'supplier_list', 'famfam':'lorry'}
supplier_delete = {'text':_('delete'), 'view':'supplier_delete', 'args':'object.id', 'famfam':'lorry_delete'}
supplier_update = {'text':_('edit'), 'view':'supplier_update', 'args':'object.id', 'famfam':'lorry'}
supplier_assign_itemtemplate = {'text':_(u'assign templates'), 'view':'supplier_assign_itemtemplates', 'args':'object.id', 'famfam':'page_go'}

template_list = {'text':_('view all'), 'view':'template_list', 'famfam':'page_go'}
template_create = {'text':_('create new'), 'view':'template_create', 'famfam':'page_add'}
template_orphan_list = {'text':_('orphans'), 'view':'template_orphans_list'}
template_update = {'text':_(u'edit'), 'view':'template_update', 'args':'object.id', 'famfam':'page_edit'}
template_delete = {'text':_(u'delete'), 'view':'template_delete', 'args':'object.id', 'famfam':'page_delete'}
template_photos = {'text':_(u'photos'), 'view':'template_photos', 'args':'object.id', 'famfam':'picture_go'}
template_assets = {'text':_(u'related assets'), 'view':'template_items_list', 'args':'object.id', 'famfam':'computer_go'}
template_assign_supplies = {'text':_(u'assign supplies'), 'view':'template_assign_supply', 'args':'object.id', 'famfam':'monitor'}
template_assign_suppliers = {'text':_(u'assign suppliers'), 'view':'template_assign_suppliers', 'args':'object.id', 'famfam':'lorry_go'}


template_menu_links = [template_list, template_create, template_orphan_list]

#template_record_links = [template_edit, template_delete, template_photos,
#    template_assets, template_assign_supplies, template_assign_suppliers]

inventory_menu_links = [
    inventory_list, inventory_create, inventory_transaction_list, inventory_transaction_create
]

#inventory_links = [inventory_balances, inventory_edit, inventory_delete]

#inventory_transaction_links = [inventory_transaction_edit, inventory_transaction_delete]

location_filter = {'name':'location', 'queryset':Location.objects.all(), 'destination':'location'}

#location_links = [location_edit, location_delete]

#suppliers_record_links = [
#    supplier_delete, supplier_update, supplier_assign_itemtemplate
#]
