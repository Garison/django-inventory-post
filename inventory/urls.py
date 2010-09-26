#-*- coding: UTF-8 -*-
from django.conf.urls.defaults import *
from models import *
from forms import *
from settings import MEDIA_URL
from views import item_retire, retireditem_unretire, item_sendtorepairs, inrepairsitem_unrepair
from django.utils.translation import ugettext_lazy as _

template_orphan_dict = dict(
	queryset = ItemTemplate.objects.filter(item=None)
)

regional_filter = {
		'regional' : { 'queryset': RegionalOffice.objects.all(), 'destination': 'regional_office'},
		}

template_record_links = [
		{ 'text' : _(u'Editar'), 'view' : 'template_update', 'icon' : MEDIA_URL+'images/accessories-text-editor.png' },
		{ 'text' : _(u'Borrar'), 'view' : 'template_delete', 'icon' : MEDIA_URL+'images/emblem-unreadable.png' },
		{ 'text' : _(u'Fotos'), 'view' : 'template_photos', 'icon': MEDIA_URL + 'images/camera-photo.png' },
		{ 'text' : _(u'Equipos que usan esta plantilla'), 'view' : 'template_items_list', 'icon': MEDIA_URL + 'images/folder-saved-search.png' },
		{ 'text' : _(u'Asignar/Remover artículos'), 'view' : 'template_assign_supply', 'icon': MEDIA_URL + 'images/edit-redo.png'},
	]
	
item_record_links = [
		{ 'text' : _(u'Editar'), 'view' : 'item_update', 'icon' : MEDIA_URL+'images/accessories-text-editor.png'},
		{ 'text' : _(u'Borrar'), 'view' : 'item_delete', 'icon' : MEDIA_URL+'images/emblem-unreadable.png'},
		{ 'text' : _(u'Fotos'), 'view' : 'item_photos', 'icon': MEDIA_URL + 'images/camera-photo.png' },
		{ 'text' : _(u'Asignar/Remover'), 'view' : 'item_assign_person', 'icon': MEDIA_URL + 'images/item-plus-user.png' },
		{ 'text' : _(u'Decomisar'), 'view' : 'item_retire', 'icon': MEDIA_URL + 'images/user-trash.png' },
		{ 'text' : _(u'Reparar'), 'view' : 'item_sendtorepairs', 'icon': MEDIA_URL + 'images/broken-computer.png' },
		{ 'text' : _(u'Plantilla'), 'view' : 'template_view', 'icon' : MEDIA_URL+'images/font-x-generic.png', 'args': 'object.item_template.id'},
	]
	
retireditem_links = [
		{ 'text' : _(u'Reactivar'), 'view' : 'retireditem_unretire' }
	]

person_links = [
		{ 'text' : _(u'Editar'), 'view' : 'person_update', 'icon' : MEDIA_URL+'images/accessories-text-editor.png'},
		{ 'text' : _(u'Borrar'), 'view' : 'person_delete', 'icon' : MEDIA_URL+'images/emblem-unreadable.png'},
		{ 'text' : _(u'Editar fotos'), 'view' : 'person_photos', 'icon': MEDIA_URL + 'images/camera-photo.png' },
		{ 'text' : _(u'Asignar/Remover equipo'), 'view' : 'person_assign_item', 'icon': MEDIA_URL + 'images/item-plus-user.png'},
	 ]

#TODO: autodetect update or delete
group_links = [
		{ 'text' : _(u'Editar'), 'view' : 'group_update', 'icon' : MEDIA_URL+'images/accessories-text-editor.png'},
		{ 'text' : _(u'Borrar'), 'view' : 'group_delete', 'icon' : MEDIA_URL+'images/emblem-unreadable.png'},
	]

regional_links = [
		{ 'text' : _(u'Editar'), 'view' : 'regional_update', 'icon' : MEDIA_URL+'images/accessories-text-editor.png'},
		{ 'text' : _(u'Borrar'), 'view' : 'regional_delete', 'icon' : MEDIA_URL+'images/emblem-unreadable.png'},
	]

department_links = [
		{ 'text' : _(u'Editar'), 'view' : 'department_update', 'icon' : MEDIA_URL+'images/accessories-text-editor.png'},
		{ 'text' : _(u'Borrar'), 'view' : 'department_delete', 'icon' : MEDIA_URL+'images/emblem-unreadable.png'},
	]

inrepairsitem_links = [ { 'text' :  _(u'Reparado'), 'view' : 'inrepairsitem_unrepair' }]

user_links = [
		{ 'text' : 	_(u'Editar'), 'view': 'user_update', 'icon' : MEDIA_URL+'images/accessories-text-editor.png' },
		{ 'text' : 	_(u'Borrar'), 'view' : 'user_delete', 'icon' : MEDIA_URL+'images/emblem-unreadable.png'},
		{ 'text' : 	_(u'Privilegios'), 'view': 'permission_list', 'icon' : '#'}
	]

permission_links = [
		{ 'text' : 	_(u'Editar'), 'view': 'permission_update', 'icon' : MEDIA_URL+'images/accessories-text-editor.png' },
		{ 'text' : 	_(u'Borrar'), 'view' : 'permission_delete', 'icon' : MEDIA_URL+'images/emblem-unreadable.png'},
	]

from inventory.views import generic_photos

retireditem_filter = {
	'regional' : { 'queryset': RegionalOffice.objects.all(), 'destination': 'item__regional_office'},
}

supply_record_links=[
		{ 'text' : _(u'Editar'), 'view' : 'supply_update', 'icon' : MEDIA_URL+'images/accessories-text-editor.png' },
		{ 'text' : _(u'Borrar'), 'view' : 'supply_delete', 'icon' : MEDIA_URL+'images/emblem-unreadable.png' },
		{ 'text' : _(u'Fotos'), 'view' : 'supply_photos', 'icon': MEDIA_URL + 'images/camera-photo.png' },
		{ 'text' : _(u'Plantillas que usan este artículo'), 'view' : 'supply_templates_list', 'icon': MEDIA_URL + 'images/folder-saved-search.png' },
		{ 'text' : _(u'Asignar/Remover plantillas'), 'view' : 'supply_assign_template', 'icon': MEDIA_URL + 'images/edit-redo.png' },
	]

inventory_links = [
		{ 'text' : 	_(u'Editar'), 'view': 'inventory_update', 'icon' : MEDIA_URL+'images/accessories-text-editor.png' },
		{ 'text' : 	_(u'Borrar'), 'view' : 'inventory_delete', 'icon' : MEDIA_URL+'images/emblem-unreadable.png'},
	]

inventory_transaction_links = [
		{ 'text' : 	_(u'Editar'), 'view': 'inventory_transaction_update', 'icon' : MEDIA_URL+'images/accessories-text-editor.png' },
		{ 'text' : 	_(u'Borrar'), 'view' : 'inventory_transaction_delete', 'icon' : MEDIA_URL+'images/emblem-unreadable.png'},
	]

urlpatterns = patterns('django-inventory.inventory.views',
	url(r'^transaction/list/$', 'generic_list', dict({ 'queryset' : InventoryTransaction.objects.all() }, extra_context = dict( title = _(u'transacciones'), create_view = 'inventory_transaction_create', record_links=inventory_transaction_links) ), 'inventory_transaction_list'),
	url(r'^transaction/create/$', 'generic_create', dict({ 'model' : InventoryTransaction }), 'inventory_transaction_create'),
	url(r'^transaction/(?P<object_id>\d+)/$', 'generic_detail', dict(form_class = InventoryTransactionForm, model=InventoryTransaction, title=_(u'transacción'), create_view = 'inventory_transaction_create', record_links=inventory_transaction_links), 'inventory_transaction_view'),
	url(r'^transaction/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'model' : InventoryTransaction }), 'inventory_transaction_update' ),
	url(r'^transaction/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : InventoryTransaction }, post_delete_redirect = "inventory_transaction_list"), 'inventory_transaction_delete'),

	url(r'^inventory/list/$', 'generic_list', dict({ 'queryset' : Inventory.objects.all() }, extra_context = dict( title = _('inventario'), create_view = 'inventory_create', record_links=inventory_links) ), 'inventory_list'),
	url(r'^inventory/create/$', 'generic_create', dict({ 'model' : Inventory }, extra_context={ 'title': _('inventario') }), 'inventory_create'),
	url(r'^inventory/(?P<object_id>\d+)/$', 'generic_detail', dict(form_class = InventoryForm, model=Inventory, title=_('inventario'), create_view = 'inventory_create', record_links=inventory_links), 'inventory_view'),
	url(r'^inventory/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'form_class' : InventoryForm }, extra_context={ 'title': _(u'inventario') }), 'inventory_update' ),
	url(r'^inventory/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : Inventory }, post_delete_redirect = "inventory_list", extra_context = dict ( title = _(u'inventario'))), 'inventory_delete'),
	url(r'^inventory/(?P<object_id>\d+)/current/$', 'inventory_current', (), 'inventory_current'),

	url(r'^supply/create/$', 'generic_create', dict({ 'form_class' : SupplyForm }, extra_context={ 'title': _(u'artículo') }), 'supply_create' ),
	url(r'^supply/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'form_class' : SupplyForm }, extra_context={ 'title': _(u'artículo') }), 'supply_update' ),
	url(r'^supply/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : Supply }, post_delete_redirect = "supply_list", extra_context=dict(title = _(u'artículo'))), 'supply_delete' ),
	url(r'^supply/list/$', 'generic_list', dict({ 'queryset' : Supply.objects.all() }, extra_context = dict(title = _(u'artículos'), create_view = 'supply_create', record_links=supply_record_links) ), 'supply_list'),
	url(r'^supply/(?P<object_id>\d+)/$', 'supply_detail', (), 'supply_view'),
	url(r'^supply/(?P<object_id>\d+)/photos/$', generic_photos, dict(model = Supply, max_photos = 5), 'supply_photos'), 
	url(r'^supply/(?P<object_id>\d+)/templates/$', 'supply_templates', (), 'supply_templates_list'),
	url(r'^supply/orphans/$', 'generic_list', dict({ 'queryset' : Supply.objects.filter(itemtemplate=None)}, extra_context = dict(title = _(u'artículos sin relacionar'), create_view = 'supply_create', record_links=supply_record_links)), 'supply_orphans_list'),
	url(r'^supply/(?P<object_id>\d+)/assign/$', 'generic_assign_remove', dict(title = _(u"a plantillas el artículo"), object = Supply.objects.all(), left_list_qryset='object.get_nonowners()',right_list_qryset='object.get_owners()',add_method='object.add_owner',remove_method='object.remove_owner',left_list_title = _(u'Plantillas que no estan relacionadas el artículo'),right_list_title = _(u'Plantillas relacionadas al artículo'), item_name=_("plantillas")), name='supply_assign_template'),

	url(r'^template/list/$', 'generic_list', dict({ 'queryset' : ItemTemplate.objects.all() }, extra_context = dict( title = _('plantillas de equipo'), create_view = "template_create", record_links=template_record_links ) ), 'template_list'),
	url(r'^template/create/$', 'generic_create', dict({ 'form_class' : ItemTemplateForm }, extra_context = dict( title = _('plantilla de equipo'))), 'template_create' ),
	url(r'^template/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'form_class' : ItemTemplateForm }, extra_context = dict( title = _('plantilla de equipo'))), 'template_update' ),
	url(r'^template/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : ItemTemplate }, post_delete_redirect = "template_list", extra_context=dict(title=_('plantilla de equipo'), _message=_("Sera borrado de los usuarios que lo tengan asignado y de cualquier grupo de equipo al que pertenezca."))), 'template_delete' ),
	url(r'^template/orphans/$', 'generic_list', dict({ 'queryset' : ItemTemplate.objects.filter(item=None)}, extra_context = dict( title = _('plantillas sin usar'), create_view = 'template_create', update_view = 'template_update', delete_view = 'template_delete', extra_record_links={ 'Editar fotos' : { 'view' : 'template_photos', 'icon': MEDIA_URL + 'images/camera-photo.png' }}) ), 'template_orphans_list'),
	url(r'^template/(?P<object_id>\d+)/photos/$', generic_photos, { 'model' : ItemTemplate, 'max_photos' : Settings.objects.get(pk=1).max_template_photos }, 'template_photos'), 
	url(r'^template/(?P<object_id>\d+)/$', 'template_detail', (), 'template_view'),
	url(r'^template/(?P<object_id>\d+)/items/$', 'template_items', (), 'template_items_list'),
	url(r'^template/(?P<object_id>\d+)/assign/$', 'generic_assign_remove', dict(title = _(u"artículos a la plantilla"), object = ItemTemplate.objects.all(), left_list_qryset='Supply.objects.exclude(itemtemplate=object)',right_list_qryset='object.supplies.all()',add_method='object.supplies.add',remove_method="object.supplies.remove",left_list_title = _(u'Artículos no relacionados'),right_list_title = _(u'Artículos relacionados'), item_name=_(u"Artículos")  ), name='template_assign_supply'),

	url(r'^item/create/$', 'generic_create', dict({ 'form_class' : ItemForm }, extra_context={ 'title': _('equipo') }), 'item_create' ),
	url(r'^item/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'form_class' : ItemForm }, extra_context={ 'title': _('equipo') }), 'item_update' ),
	url(r'^item/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : Item }, post_delete_redirect = "item_list", extra_context=dict(title = _('equipo'))), 'item_delete' ),
	url(r'^item/(?P<object_id>\d+)/assign/$', 'generic_assign_remove', dict(title = _("a usuarios el equipo"), object = Item.objects.all(), left_list_qryset='object.get_nonowners()',right_list_qryset='object.get_owners()',add_method='object.add_owner',remove_method='object.remove_owner',left_list_title = _('Usuarios que no poseen el equipo'),right_list_title = _('Usuarios que poseen el equipo'), item_name=_("usuarios"), list_filter=regional_filter), name='item_assign_person'),
	url(r'^item/(?P<object_id>\d+)/retire/$', 'generic_confirm', dict(_view=item_retire, _title=_("decomisar el equipo"), _model=Item, _object_id="object_id", _message=_("Sera borrado de los usuarios que lo tengan asignado y de cualquier grupo de equipo al que pertenezca.")), 'item_retire'),
	url(r'^item/(?P<object_id>\d+)/sendtorepairs/$', 'generic_confirm', dict(_view=item_sendtorepairs, _title=_("enviar a reparar el equipo"), _model=Item, _object_id="object_id"), 'item_sendtorepairs'),
	url(r'^item/orphans/$', 'generic_list', dict({ 'queryset' : Item.objects.filter(person=None)}, extra_context = dict(title = _('equipos sin asignar'), create_view = 'item_create', record_links=item_record_links)), 'item_orphans_list'),
	url(r'^item/list/$', 'generic_list', dict({ 'queryset' : Item.objects.all() }, list_filter=regional_filter, extra_context = dict(title = _('equipos'), create_view = 'item_create', record_links=item_record_links) ), 'item_list'),
	url(r'^item/(?P<object_id>\d+)/$', 'item_detail', (), 'item_view'),
	url(r'^item/(?P<object_id>\d+)/photos/$', generic_photos, dict(model = Item, max_photos = Settings.objects.get(pk=1).max_item_photos), 'item_photos'), 
	url(r'^item/(?P<object_id>\d+)/log/$', 'item_log_list', () , 'item_log_list'),

	url(r'^group/list/$', 'generic_list', dict({ 'queryset' : ItemGroup.objects.all() }, extra_context = dict( title = _('grupos de equipo'), create_view = 'group_create', record_links=group_links) ), 'group_list'),
	url(r'^group/create/$', 'generic_create', dict({ 'form_class' : ItemGroupForm }, extra_context={ 'title': _('grupo de equipos') }), 'group_create'),
	url(r'^group/(?P<object_id>\d+)/$', 'generic_detail', dict(form_class=ItemGroupForm, model=ItemGroup, title=_('grupo de equipo'), create_view = 'group_create', record_links=group_links), 'group_view'),
	url(r'^group/(?P<object_id>\d+)/update/$', 'generic_assign_remove', dict(title = _("equipos a el grupo"), object = ItemGroup.objects.all(), left_list_qryset='Item.objects.exclude(itemgroup=object)',right_list_qryset='object.items.all()',add_method='object.items.add',remove_method="object.items.remove",left_list_title = _('Equipos no asignados'),right_list_title = _('Equipos asignados'), item_name=_("equipos")  ), name='group_update'),
	url(r'^group/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : ItemGroup }, post_delete_redirect = "group_list", extra_context = dict ( title = _('grupo de equipos'))), 'group_delete'),

	url(r'^person/(?P<object_id>\d+)/photos/$', generic_photos, { 'model' : Person, 'max_photos' : Settings.objects.get(pk=1).max_person_photos }, 'person_photos'), 
	url(r'^person/(?P<object_id>\d+)/$', 'person_detail', (), 'person_view'),
	url(r'^person/list/$', 'generic_list', dict({ 'queryset' : Person.objects.all() }, list_filter=regional_filter, extra_context = dict(title = _('usuarios'), create_view = "person_create", record_links=person_links)), 'person_list'),
	url(r'^person/create/$', 'generic_create', dict({ 'form_class' : PersonForm }, extra_context={ 'title': _('usuario') }), 'person_create' ),
	url(r'^person/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'form_class' : PersonForm }, extra_context={  'title' : _('usuario') }), 'person_update' ),
	url(r'^person/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : Person }, post_delete_redirect = "person_list", extra_context=dict(title = _('usuario'))), 'person_delete' ),
	url(r'^person/(?P<object_id>\d+)/assign/$', 'generic_assign_remove', dict(title = _("equipos a el usuario"), object = Person.objects.all(), left_list_qryset='Item.objects.exclude(person=object)',right_list_qryset='object.inventory.all()',add_method='object.inventory.add',remove_method="object.inventory.remove",left_list_title = _('Equipos no asignados'),right_list_title = _('Equipos asignados'), item_name=_("equipos"), list_filter=regional_filter), name='person_assign_item'),

	url(r'^retireditem/list/$', 'generic_list', dict({ 'queryset' : RetiredItem.objects.all() }, list_filter=retireditem_filter, extra_context = dict(title = _('equipos decomisados'),  record_links=retireditem_links)), 'retireditem_list'),
	url(r'^retireditem/(?P<object_id>\d+)/$', 'retireditem_detail', (), 'retireditem_view'),
	url(r'^retireditem/(?P<object_id>\d+)/unretire/$', 'generic_confirm', dict(_view=retireditem_unretire, _title=_("reactivar el equipo"), _model=RetiredItem, _object_id="object_id"), 'retireditem_unretire'),

	url(r'^inrepairsitem/list/$', 'generic_list', dict({ 'queryset' : InRepairsItem.objects.all() }, list_filter=retireditem_filter, extra_context = dict(title = _(u"equipos en reparación"), record_links=inrepairsitem_links)), 'inrepairsitem_list'),
	url(r'^inrepairsitem/(?P<object_id>\d+)/$', 'inrepairsitem_detail', (), 'inrepairsitem_view'),
	url(r'^inrepairsitem/(?P<object_id>\d+)/unrepair/$', 'generic_confirm', dict(_view=inrepairsitem_unrepair, _title=_("marcar como reparado el equipo"), _model=InRepairsItem, _object_id="object_id"), 'inrepairsitem_unrepair'),
	
	url(r'^regional/list/$', 'generic_list', dict({ 'queryset' : RegionalOffice.objects.all() }, extra_context = dict( title = _('regionales'), create_view = 'regional_create', record_links=regional_links)), 'regional_list'),
	url(r'^regional/create/$', 'generic_create', dict({ 'model' : RegionalOffice }, extra_context={ 'title': _('regional') }), 'regional_create'),
	url(r'^regional/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'model' : RegionalOffice }, extra_context={ 'title': _('regional') }) , 'regional_update'),
	url(r'^regional/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : RegionalOffice }, post_delete_redirect = "regional_list", extra_context = dict ( title = _('regional'))), 'regional_delete'),

	url(r'^department/create/$', 'generic_create', dict({ 'model' : Department }, extra_context={ 'title': _('departamento/sección/area') }), 'department_create'),
	url(r'^department/(?P<object_id>\d+)/update/$', 'generic_update', dict({ 'model' : Department }, extra_context={ 'title': _('departamento/sección/area') }) , 'department_update'),
	url(r'^department/(?P<object_id>\d+)/delete/$', 'generic_delete', dict({ 'model' : Department }, post_delete_redirect = "department_list", extra_context = dict ( title = _('departamentos/Secciones/areas'))), 'department_delete'),
	url(r'^department/list/$', 'generic_list', dict({ 'queryset' : Department.objects.all() }, list_filter=regional_filter, extra_context = dict( title = _('departamentos/secciones/areas'), create_view='department_create', record_links=department_links) ), 'department_list'),

	url(r'^log/list/$', 'generic_list', dict(queryset=Log.objects.all(), extra_context={'title' : _('bitacora')}), 'log_list'),
	url(r'^log/(?P<object_id>\d+)/$', 'generic_detail', dict(form_class=LogForm, model=Log, title=_('bitacora')), 'log_view'),
	url(r'^search/$', 'search', (), 'search'),

	url(r'^settings/$', 'generic_update', dict({ 'model' : Settings, 'object_id' : 1 }), 'settings' ),

	url(r'^reports/items_per_person/(?P<object_id>\d+)/$', 'report_items_per_person', (), 'report_items_per_person'),
	
	url(r'^set_language/$', 'set_language', (), 'set_language'),
	
	url(r'^assign_remove/$', 'generic_assign_remove', (), 'generic_assign_remove'),
	
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
	
urlpatterns += patterns('django.views.generic.simple',
	(r'^$', 'direct_to_template', { 'template' : 'home.html', 'extra_context' : { 'person': Person.objects.all(), 'item': Item.objects.all(), 'template': ItemTemplate.objects.all(), 'retired' : RetiredItem.objects.all() }}, "home"),
)
