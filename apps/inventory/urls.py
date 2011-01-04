from django.conf.urls.defaults import *
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from inventory import person_links, regional_links, department_links
#from views import item_retire, retireditem_unretire, item_sendtorepairs#, inrepairsitem_unrepair
from views import generic_photos

from models import ItemTemplate, RegionalOffice, InventoryTransaction, \
                   Inventory, Supply, Settings, Item, ItemGroup, Person, \
                   RetiredItem, InRepairsItem, Department, Log
from forms import InventoryTransactionForm, InventoryForm, SupplyForm, \
                  ItemTemplateForm, ItemForm, ItemGroupForm, PersonForm, \
                  LogForm

#template_orphan_dict = dict(
#    queryset = ItemTemplate.objects.filter(item=None)
#)

regional_filter = {
    'regional' : { 'queryset': RegionalOffice.objects.all(), 'destination': 'regional_office'},
}


urlpatterns = patterns('inventory.views',
#    url(r'^transaction/list/$', 'generic_list', dict({ 'queryset' : InventoryTransaction.objects.all() }, extra_context = dict( title = _(u'transactions'), create_view = 'inventory_transaction_create', record_links=inventory_transaction_links) ), 'inventory_transaction_list'),
#    url(r'^transaction/create/$', 'generic_create', dict({ 'model' : InventoryTransaction }), 'inventory_transaction_create'),
#    url(r'^transaction/(?P<object_id>\d+)/$', 'generic_detail', dict(form_class = InventoryTransactionForm, model=InventoryTransaction, title=_(u'transaction'), create_view = 'inventory_transaction_create', record_links=inventory_transaction_links), 'inventory_transaction_view'),
#    url(r'^transaction/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'model' : InventoryTransaction }), 'inventory_transaction_update' ),
#    url(r'^transaction/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : InventoryTransaction }, post_delete_redirect = "inventory_transaction_list"), 'inventory_transaction_delete'),

#    url(r'^inventory/list/$', 'generic_list', dict({ 'queryset' : Inventory.objects.all() }, extra_context = dict( title = _('inventory'), create_view = 'inventory_create', record_links=inventory_links) ), 'inventory_list'),
#    url(r'^inventory/create/$', 'generic_create', dict({ 'model' : Inventory }, extra_context={ 'title': _('inventory') }), 'inventory_create'),
#    url(r'^inventory/(?P<object_id>\d+)/$', 'generic_detail', dict(form_class = InventoryForm, model=Inventory, title=_('inventory'), create_view = 'inventory_create', record_links=inventory_links), 'inventory_view'),
#    url(r'^inventory/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'form_class' : InventoryForm }, extra_context={ 'title': _(u'inventory') }), 'inventory_update' ),
#    url(r'^inventory/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : Inventory }, post_delete_redirect = "inventory_list", extra_context = dict ( title = _(u'inventory'))), 'inventory_delete'),
#    url(r'^inventory/(?P<object_id>\d+)/current/$', 'inventory_current', (), 'inventory_current'),

#    url(r'^supply/create/$', 'generic_create', dict({ 'form_class' : SupplyForm }, extra_context={ 'title': _(u'supply') }), 'supply_create' ),
#    url(r'^supply/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'form_class' : SupplyForm }, extra_context={ 'title': _(u'supply') }), 'supply_update' ),
#    url(r'^supply/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : Supply }, post_delete_redirect = "supply_list", extra_context=dict(title = _(u'supply'))), 'supply_delete' ),
#    url(r'^supply/list/$', 'generic_list', dict({ 'queryset' : Supply.objects.all() }, extra_context = dict(title = _(u'supply'), create_view = 'supply_create', record_links=supply_record_links) ), 'supply_list'),
#    url(r'^supply/(?P<object_id>\d+)/$', 'supply_detail', (), 'supply_view'),
#    url(r'^supply/(?P<object_id>\d+)/photos/$', generic_photos, dict(model = Supply, max_photos = 5), 'supply_photos'), 
#    url(r'^supply/(?P<object_id>\d+)/templates/$', 'supply_templates', (), 'supply_templates_list'),
#    url(r'^supply/orphans/$', 'generic_list', dict({ 'queryset' : Supply.objects.filter(itemtemplate=None)}, extra_context = dict(title = _(u'orphan supplies'), create_view = 'supply_create', record_links=supply_record_links)), 'supply_orphans_list'),
#    url(r'^supply/(?P<object_id>\d+)/assign/$', 'generic_assign_remove', dict(title = _(u"supplies to template"), object = Supply.objects.all(), left_list_qryset='object.get_nonowners()',right_list_qryset='object.get_owners()',add_method='object.add_owner',remove_method='object.remove_owner',left_list_title = _(u'Unassigned templates'),right_list_title = _(u'Assigned templates'), item_name=_("templates")), name='supply_assign_template'),

#    url(r'^template/list/$', 'generic_list', dict({ 'queryset' : ItemTemplate.objects.all() }, extra_context = dict( title = _('item template'), create_view = "template_create", record_links=template_record_links ) ), 'template_list'),
#    url(r'^template/create/$', 'generic_create', dict({ 'form_class' : ItemTemplateForm }, extra_context = dict( title = _('item template'))), 'template_create' ),
#    url(r'^template/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'form_class' : ItemTemplateForm }, extra_context = dict( title = _('item template'))), 'template_update' ),
#    url(r'^template/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : ItemTemplate }, post_delete_redirect = "template_list", extra_context=dict(title=_('item template'), _message=_("Sera borrado de los usuarios que lo tengan asignado y de cualquier grupo de equipo al que pertenezca."))), 'template_delete' ),
#    url(r'^template/orphans/$', 'generic_list', dict({ 'queryset' : ItemTemplate.objects.filter(item=None)}, extra_context = dict( title = _('plantillas sin usar'), create_view = 'template_create', update_view = 'template_update', delete_view = 'template_delete', extra_record_links={ 'Editar fotos' : { 'view' : 'template_photos', 'icon': MEDIA_URL + 'images/camera-photo.png' }}) ), 'template_orphans_list'),
#    url(r'^template/(?P<object_id>\d+)/photos/$', generic_photos, { 'model' : ItemTemplate, 'max_photos' : Settings.objects.get(pk=1).max_template_photos }, 'template_photos'), 
#    url(r'^template/(?P<object_id>\d+)/$', 'template_detail', (), 'template_view'),
#    url(r'^template/(?P<object_id>\d+)/items/$', 'template_items', (), 'template_items_list'),
#    url(r'^template/(?P<object_id>\d+)/assign/$', 'generic_assign_remove', dict(title = _(u"template supplies"), object = ItemTemplate.objects.all(), left_list_qryset='Supply.objects.exclude(itemtemplate=object)',right_list_qryset='object.supplies.all()',add_method='object.supplies.add',remove_method="object.supplies.remove",left_list_title = _(u'Unassigned supplies'),right_list_title = _(u'Assigned supplies'), item_name=_(u"Supplies")  ), name='template_assign_supply'),

#    url(r'^item/create/$', 'generic_create', dict({ 'form_class' : ItemForm }, extra_context={ 'title': _(u'item') }), 'item_create' ),
#    url(r'^item/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'form_class' : ItemForm }, extra_context={ 'title': _(u'item') }), 'item_update' ),
#    url(r'^item/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : Item }, post_delete_redirect = "item_list", extra_context=dict(title = _(u'item'))), 'item_delete' ),
#    url(r'^item/(?P<object_id>\d+)/assign/$', 'generic_assign_remove', dict(title = _("to users of the item"), object = Item.objects.all(), left_list_qryset='object.get_nonowners()',right_list_qryset='object.get_owners()',add_method='object.add_owner',remove_method='object.remove_owner',left_list_title = _('Usuarios que no poseen el equipo'),right_list_title = _('Usuarios que poseen el equipo'), item_name=_("usuarios"), list_filter=regional_filter), name='item_assign_person'),
#    url(r'^item/(?P<object_id>\d+)/retire/$', 'generic_confirm', dict(_view=item_retire, _title=_("retire item"), _model=Item, _object_id="object_id", _message=_("Sera borrado de los usuarios que lo tengan asignado y de cualquier grupo de equipo al que pertenezca.")), 'item_retire'),
#    url(r'^item/(?P<object_id>\d+)/sendtorepairs/$', 'generic_confirm', dict(_view=item_sendtorepairs, _title=_("send item to repairs"), _model=Item, _object_id="object_id"), 'item_sendtorepairs'),
#    url(r'^item/orphans/$', 'generic_list', dict({ 'queryset' : Item.objects.filter(person=None)}, extra_context = dict(title = _('orphan items'), create_view = 'item_create', record_links=item_record_links)), 'item_orphans_list'),
#    url(r'^item/list/$', 'generic_list', dict({ 'queryset' : Item.objects.all() }, list_filter=regional_filter, extra_context = dict(title = _('items'), create_view = 'item_create', record_links=item_record_links) ), 'item_list'),
#    url(r'^item/(?P<object_id>\d+)/$', 'item_detail', (), 'item_view'),
#    url(r'^item/(?P<object_id>\d+)/photos/$', generic_photos, dict(model = Item, max_photos = Settings.objects.get(pk=1).max_item_photos), 'item_photos'), 
#    url(r'^item/(?P<object_id>\d+)/log/$', 'item_log_list', () , 'item_log_list'),

#    url(r'^group/list/$', 'generic_list', dict({ 'queryset' : ItemGroup.objects.all() }, extra_context = dict( title = _(u'item group'), create_view = 'group_create', record_links=group_links) ), 'group_list'),
#    url(r'^group/create/$', 'generic_create', dict({ 'form_class' : ItemGroupForm }, extra_context={ 'title': _(u'item group') }), 'group_create'),
#    url(r'^group/(?P<object_id>\d+)/$', 'generic_detail', dict(form_class=ItemGroupForm, model=ItemGroup, title=_(u'item group'), create_view = 'group_create', record_links=group_links), 'group_view'),
#    url(r'^group/(?P<object_id>\d+)/update/$', 'generic_assign_remove', dict(title = _(u"item group"), object = ItemGroup.objects.all(), left_list_qryset='Item.objects.exclude(itemgroup=object)',right_list_qryset='object.items.all()',add_method='object.items.add',remove_method="object.items.remove",left_list_title = _('Equipos no asignados'),right_list_title = _('Equipos asignados'), item_name=_("equipos")  ), name='group_update'),
#    url(r'^group/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : ItemGroup }, post_delete_redirect = "group_list", extra_context = dict ( title = _(u'item group'))), 'group_delete'),

    url(r'^person/(?P<object_id>\d+)/photos/$', generic_photos, {'model':Person, 'max_photos':Settings.objects.get(pk=1).max_person_photos}, 'person_photos'), 
    url(r'^person/(?P<object_id>\d+)/$', 'person_detail', (), 'person_view'),
    url(r'^person/list/$', 'generic_list', dict({'queryset':Person.objects.all()}, list_filter=regional_filter, extra_context=dict(title=_(u'users'), create_view="person_create", record_links=person_links)), 'person_list'),
    url(r'^person/create/$', 'generic_create', dict({'form_class':PersonForm}, extra_context={'title':_(u'user')}), 'person_create'),
    url(r'^person/(?P<object_id>\d+)/update/$', 'generic_update', dict({'form_class':PersonForm}, extra_context={'title':_(u'user')}), 'person_update'),
    url(r'^person/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({'model':Person}, post_delete_redirect="person_list", extra_context=dict(title=_(u'user'))), 'person_delete'),
    url(r'^person/(?P<object_id>\d+)/assign/$', 'generic_assign_remove', dict(title=_(u"item to user"), object=Person.objects.all(), left_list_qryset='Item.objects.exclude(person=object)', right_list_qryset='object.inventory.all()', add_method='object.inventory.add', remove_method="object.inventory.remove", left_list_title=_(u'Unassigned items'), right_list_title=_(u'Assigned items'), item_name=_(u"items"), list_filter=regional_filter), name='person_assign_item'),

#    url(r'^retireditem/list/$', 'generic_list', dict({ 'queryset' : RetiredItem.objects.all() }, list_filter=retireditem_filter, extra_context = dict(title = _('retired items'),  record_links=retireditem_links)), 'retireditem_list'),
#    url(r'^retireditem/(?P<object_id>\d+)/$', 'retireditem_detail', (), 'retireditem_view'),
#    url(r'^retireditem/(?P<object_id>\d+)/unretire/$', 'generic_confirm', dict(_view=retireditem_unretire, _title=_("reactivate item"), _model=RetiredItem, _object_id="object_id"), 'retireditem_unretire'),

#    url(r'^inrepairsitem/list/$', 'generic_list', dict({ 'queryset' : InRepairsItem.objects.all() }, list_filter=retireditem_filter, extra_context = dict(title = _(u"items in repairs"), record_links=inrepairsitem_links)), 'inrepairsitem_list'),
#    url(r'^inrepairsitem/(?P<object_id>\d+)/$', 'inrepairsitem_detail', (), 'inrepairsitem_view'),
#    url(r'^inrepairsitem/(?P<object_id>\d+)/unrepair/$', 'generic_confirm', dict(_view=inrepairsitem_unrepair, _title=_(u"mark item as repaired"), _model=InRepairsItem, _object_id="object_id"), 'inrepairsitem_unrepair'),
    
    url(r'^regional/list/$', 'generic_list', dict({'queryset':RegionalOffice.objects.all()}, extra_context=dict(title =_(u'regionals'), create_view='regional_create', record_links=regional_links)), 'regional_list'),
    url(r'^regional/create/$', 'generic_create', dict({'model':RegionalOffice}, extra_context={'title':_(u'regionals')}), 'regional_create'),
    url(r'^regional/(?P<object_id>\d+)/update/$', 'generic_update', dict({'model':RegionalOffice}, extra_context={'title':_(u'regionals')}), 'regional_update'),
    url(r'^regional/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({'model':RegionalOffice}, post_delete_redirect="regional_list", extra_context=dict (title=_(u'regional'))), 'regional_delete'),

    url(r'^department/create/$', 'generic_create', dict({'model':Department }, extra_context={'title':_(u'department/section/area')}), 'department_create'),
    url(r'^department/(?P<object_id>\d+)/update/$', 'generic_update', dict({'model':Department}, extra_context={'title':_(u'department/section/area')}) , 'department_update'),
    url(r'^department/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({'model':Department}, post_delete_redirect="department_list", extra_context=dict(title=_(u'departments/sections/areas'))), 'department_delete'),
    url(r'^department/list/$', 'generic_list', dict({'queryset':Department.objects.all()}, list_filter=regional_filter, extra_context=dict(title=_(u'departments/sections/areas'), create_view='department_create', record_links=department_links)), 'department_list'),

#    url(r'^log/list/$', 'generic_list', dict(queryset=Log.objects.all(), extra_context={'title' : _(u'log')}), 'log_list'),
#    url(r'^log/(?P<object_id>\d+)/$', 'generic_detail', dict(form_class=LogForm, model=Log, title=_(u'log')), 'log_view'),
    url(r'^search/$', 'search', (), 'search'),

#    url(r'^settings/$', 'generic_update', dict({ 'model' : Settings, 'object_id' : 1 }), 'settings' ),

#    url(r'^reports/items_per_person/(?P<object_id>\d+)/$', 'report_items_per_person', (), 'report_items_per_person'),
  
#    url(r'^assign_remove/$', 'generic_assign_remove', (), 'generic_assign_remove'),
    
#	url(r'^user/list/$', 'generic_list', dict({ 'queryset' : CustomUser.objects.all() }, extra_context = dict( title = 'usuarios', record_links=user_links) ), 'user_list'),
#	url(r'^user/(?P<object_id>\d+)/$', 'generic_detail', dict(form_class=CustomUserForm, model=CustomUser, title='usuario', create_view = 'user_create', record_links=user_links), 'user_view'),
#	url(r'^user/create/$', 'generic_create', dict({ 'model' : CustomUser }, extra_context={ 'title': 'usuario' }), 'user_create'),
#	url(r'^user/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'model' : CustomUser }, extra_context={ 'title': 'usuario' }) , 'user_update'),
#	url(r'^user/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : CustomUser }, post_delete_redirect = "/user/list", extra_context={ 'title': 'el usuario' }) , 'user_delete'),
#	url(r'^user/(?P<user_id>\d+)/permission/list$', 'generic_list', dict({ 'queryset' : Permission.objects.all() }, queryset_filter={ 'field' : 'user', 'source' : 'user_id'}, extra_context = dict( title = 'privilegios', create_view = 'permission_create', record_links=permission_links)), 'permission_list'),
#	url(r'^permission/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'model' : Permission }, extra_context = dict( title = 'privilegio') ), 'permission_update'),
#	url(r'^permission/create/$', 'generic_create', dict({ 'model' : Permission }, extra_context={ 'title': 'privilegio' }), 'permission_create'),
#	url(r'^permission/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : Permission }, post_delete_redirect = "/user/list", extra_context={ 'title': 'el privilegio' }) , 'permission_delete'),
)
    

