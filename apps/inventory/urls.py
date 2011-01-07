from django.conf.urls.defaults import *
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from photos.views import generic_photos

from inventory import person_links, \
                      template_record_links, inventory_links, \
                      item_record_links, \
                      inventory_transaction_links, \
                      group_links, location_filter, location_links


from models import ItemTemplate, InventoryTransaction, \
                   Inventory, Settings, Item, ItemGroup, Person, \
                   Log, Location
                   
from forms import InventoryTransactionForm, InventoryForm, \
                  ItemTemplateForm, ItemForm, ItemGroupForm, PersonForm, \
                  LogForm

from generic_views.views import generic_assign_remove, \
                                generic_create, generic_delete, \
                                generic_detail, generic_list, \
                                generic_update

#template_orphan_dict = dict(
#    queryset = ItemTemplate.objects.filter(item=None)
#)

urlpatterns = patterns('inventory.views',
    url(r'^transaction/list/$', generic_list, dict({'queryset':InventoryTransaction.objects.all()}, extra_context=dict(title=_(u'transactions'), create_view='inventory_transaction_create', record_links=inventory_transaction_links)), 'inventory_transaction_list'),
    url(r'^transaction/create/$', generic_create, dict({'model':InventoryTransaction}), 'inventory_transaction_create'),
    url(r'^transaction/(?P<object_id>\d+)/$', generic_detail, dict(form_class=InventoryTransactionForm, model=InventoryTransaction, title=_(u'transaction'), create_view='inventory_transaction_create', record_links=inventory_transaction_links), 'inventory_transaction_view'),
    url(r'^transaction/(?P<object_id>\d+)/update/$', generic_update, dict({'model':InventoryTransaction}), 'inventory_transaction_update'),
    url(r'^transaction/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':InventoryTransaction}, post_delete_redirect="inventory_transaction_list"), 'inventory_transaction_delete'),

    url(r'^inventory/list/$', generic_list, dict({'queryset':Inventory.objects.all()}, extra_context=dict(title=_(u'inventories'), create_view='inventory_create', record_links=inventory_links)), 'inventory_list'),
    url(r'^inventory/create/$', generic_create, dict({'model':Inventory}, extra_context={'title':_(u'inventory')}), 'inventory_create'),
    url(r'^inventory/(?P<object_id>\d+)/$', generic_detail, dict(form_class=InventoryForm, model=Inventory, title=_(u'inventory'), create_view='inventory_create', record_links=inventory_links), 'inventory_view'),
    url(r'^inventory/(?P<object_id>\d+)/update/$', generic_update, dict({'form_class':InventoryForm}, extra_context={'title':_(u'inventory')}), 'inventory_update'),
    url(r'^inventory/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':Inventory}, post_delete_redirect="inventory_list", extra_context=dict(title=_(u'inventory'))), 'inventory_delete'),
    url(r'^inventory/(?P<object_id>\d+)/current/$', 'inventory_current', (), 'inventory_current'),

    url(r'^template/list/$', generic_list, dict({'queryset':ItemTemplate.objects.all()}, extra_context=dict(title=_(u'item template'), create_view="template_create", record_links=template_record_links)), 'template_list'),
    url(r'^template/create/$', generic_create, dict({'form_class':ItemTemplateForm}, extra_context=dict(title=_(u'item template'))), 'template_create'),
    url(r'^template/(?P<object_id>\d+)/update/$', generic_update, dict({'form_class':ItemTemplateForm}, extra_context=dict(title=_(u'item template'))), 'template_update' ),
    url(r'^template/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':ItemTemplate}, post_delete_redirect="template_list", extra_context=dict(title=_(u'item template'), _message=_(u"Will be deleted from any user that may have it assigned and from any item group."))), 'template_delete' ),
    url(r'^template/orphans/$', generic_list, dict({'queryset':ItemTemplate.objects.filter(item=None)}, extra_context=dict(title=_('orphan templates'), create_view='template_create', update_view='template_update', delete_view='template_delete', extra_record_links={'Edit photos':{'view':'template_photos', 'icon':settings.MEDIA_URL+'images/camera-photo.png'}})), 'template_orphans_list'),
    url(r'^template/(?P<object_id>\d+)/photos/$', generic_photos, {'model':ItemTemplate, 'max_photos':Settings.objects.get(pk=1).max_template_photos }, 'template_photos'), 
    url(r'^template/(?P<object_id>\d+)/$', 'template_detail', (), 'template_view'),
    url(r'^template/(?P<object_id>\d+)/items/$', 'template_items', (), 'template_items_list'),
    url(r'^template/(?P<object_id>\d+)/assign/$', 'template_assign_remove_supply', (), name='template_assign_supply'),

    url(r'^asset/create/$', generic_create, dict({'form_class':ItemForm}, extra_context={'title':_(u'asset')}), 'item_create'),
    url(r'^asset/(?P<object_id>\d+)/update/$', generic_update, dict({'form_class':ItemForm}, extra_context={'title':_(u'asset')}), 'item_update'),
    url(r'^asset/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':Item}, post_delete_redirect="item_list", extra_context=dict(title=_(u'asset'))), 'item_delete'),
    url(r'^asset/(?P<object_id>\d+)/assign/$', 'item_assign_remove_person', (), name='item_assign_person'),
#    url(r'^asset/(?P<object_id>\d+)/retire/$', 'item_retire', (), 'item_retire'),
#    url(r'^asset/(?P<object_id>\d+)/sendtorepairs/$', 'item_sendtorepairs', (), 'item_sendtorepairs'),
    url(r'^asset/orphans/$', generic_list, dict({'queryset':Item.objects.filter(person=None)}, extra_context=dict(title=_(u'orphan assets'), create_view='item_create', record_links=item_record_links)), 'item_orphans_list'),
    url(r'^asset/list/$', generic_list, dict({'queryset':Item.objects.all()}, list_filter=location_filter, extra_context=dict(title=_(u'assets'), create_view='item_create', record_links=item_record_links)), 'item_list'),
    url(r'^asset/(?P<object_id>\d+)/$', 'item_detail', (), 'item_view'),
    url(r'^asset/(?P<object_id>\d+)/photos/$', generic_photos, dict(model=Item, max_photos=Settings.objects.get(pk=1).max_item_photos), 'item_photos'), 
    url(r'^asset/(?P<object_id>\d+)/log/$', 'item_log_list',() , 'item_log_list'),
    url(r'^asset/(?P<object_id>\d+)/setstate/(?P<state_id>\d+)/$', 'item_setstate', (), 'item_setstate'),
    url(r'^asset/state/(?P<state_id>\d+)/list/$', 'item_state_list', (), 'item_state_list'),


    url(r'^group/list/$', generic_list, dict({'queryset':ItemGroup.objects.all()}, extra_context=dict(title=_(u'item group'), create_view='group_create', record_links=group_links)), 'group_list'),
    url(r'^group/create/$', generic_create, dict({'form_class':ItemGroupForm}, extra_context={'title':_(u'item group')}), 'group_create'),
    url(r'^group/(?P<object_id>\d+)/$', generic_detail, dict(form_class=ItemGroupForm, model=ItemGroup, title=_(u'item group'), create_view='group_create', record_links=group_links), 'group_view'),
    #TODO: convert to new generic_assign_remove
    url(r'^group/(?P<object_id>\d+)/update/$', generic_assign_remove, dict(title=_(u"item group"), object=ItemGroup.objects.all(), left_list_qryset='Item.objects.exclude(itemgroup=object)', right_list_qryset='object.items.all()', add_method='object.items.add', remove_method="object.items.remove", left_list_title=_(u'Unassigned items'), right_list_title=_(u'Assigned items'), item_name=_(u"items")), name='group_update'),
    url(r'^group/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':ItemGroup}, post_delete_redirect="group_list", extra_context=dict(title=_(u'item group'))), 'group_delete'),

    url(r'^person/(?P<object_id>\d+)/photos/$', generic_photos, {'model':Person, 'max_photos':Settings.objects.get(pk=1).max_person_photos}, 'person_photos'), 
    url(r'^person/(?P<object_id>\d+)/$', 'person_detail', (), 'person_view'),
    url(r'^person/list/$', generic_list, dict({'queryset':Person.objects.all()}, list_filter=location_filter, extra_context=dict(title=_(u'users'), create_view="person_create", record_links=person_links)), 'person_list'),
    url(r'^person/create/$', generic_create, dict({'form_class':PersonForm}, extra_context={'title':_(u'user')}), 'person_create'),
    url(r'^person/(?P<object_id>\d+)/update/$', generic_update, dict({'form_class':PersonForm}, extra_context={'title':_(u'user')}), 'person_update'),
    url(r'^person/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':Person}, post_delete_redirect="person_list", extra_context=dict(title=_(u'user'))), 'person_delete'),
    url(r'^person/(?P<object_id>\d+)/assign/$', 'person_assign_remove_item', (), 'person_assign_item'),
    
#    url(r'^retireditem/list/$', generic_list, dict({'queryset':RetiredItem.objects.all()}, list_filter=retireditem_filter, extra_context=dict(title=_(u'retired assets'), record_links=retireditem_links)), 'retireditem_list'),
#    url(r'^retireditem/(?P<object_id>\d+)/$', 'retireditem_detail', (), 'retireditem_view'),
#    url(r'^retireditem/(?P<object_id>\d+)/unretire/$', 'retireditem_unretire', (), 'retireditem_unretire'),

#    url(r'^inrepairsitem/list/$', generic_list, dict({'queryset':InRepairsItem.objects.all()}, list_filter=retireditem_filter, extra_context=dict(title=_(u"assets in repairs"), record_links=inrepairsitem_links)), 'inrepairsitem_list'),
#    url(r'^inrepairsitem/(?P<object_id>\d+)/$', 'inrepairsitem_detail', (), 'inrepairsitem_view'),
#    url(r'^inrepairsitem/(?P<object_id>\d+)/unrepair/$', 'inrepairsitem_unrepair', (), 'inrepairsitem_unrepair'),
    
    url(r'^location/list/$', generic_list, dict({'queryset':Location.objects.all()}, extra_context=dict(title =_(u'locations'), create_view='location_create', record_links=location_links)), 'location_list'),
    url(r'^location/create/$', generic_create, dict({'model':Location}, extra_context={'title':_(u'locations')}), 'location_create'),
    url(r'^location/(?P<object_id>\d+)/update/$', generic_update, dict({'model':Location}, extra_context={'title':_(u'locations')}), 'location_update'),
    url(r'^location/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':Location}, post_delete_redirect="location_list", extra_context=dict(title=_(u'locations'))), 'location_delete'),

#    url(r'^log/list/$', generic_list, dict(queryset=Log.objects.all(), extra_context={'title' : _(u'log')}), 'log_list'),
#    url(r'^log/(?P<object_id>\d+)/$', generic_detail, dict(form_class=LogForm, model=Log, title=_(u'log')), 'log_view'),
    url(r'^search/$', 'search', (), 'search'),

    url(r'^settings/$', generic_update, dict({'model':Settings, 'object_id':1}), 'settings'),

#    url(r'^reports/items_per_person/(?P<object_id>\d+)/$', 'report_items_per_person', (), 'report_items_per_person'),
  
#    url(r'^assign_remove/$', generic_assign_remove, (), generic_assign_remove),
    
#	url(r'^user/list/$', generic_list, dict({ 'queryset' : CustomUser.objects.all() }, extra_context = dict( title = 'usuarios', record_links=user_links) ), 'user_list'),
#	url(r'^user/(?P<object_id>\d+)/$', generic_detail, dict(form_class=CustomUserForm, model=CustomUser, title='usuario', create_view = 'user_create', record_links=user_links), 'user_view'),
#	url(r'^user/create/$', generic_create, dict({ 'model' : CustomUser }, extra_context={ 'title': 'usuario' }), 'user_create'),
#	url(r'^user/(?P<object_id>\d+)/update/$', generic_update, dict({ 'model' : CustomUser }, extra_context={ 'title': 'usuario' }) , 'user_update'),
#	url(r'^user/(?P<object_id>\d+)/delete/$', generic_delete, dict({ 'model' : CustomUser }, post_delete_redirect = "/user/list", extra_context={ 'title': 'el usuario' }) , 'user_delete'),
#	url(r'^user/(?P<user_id>\d+)/permission/list$', generic_list, dict({ 'queryset' : Permission.objects.all() }, queryset_filter={ 'field' : 'user', 'source' : 'user_id'}, extra_context = dict( title = 'privilegios', create_view = 'permission_create', record_links=permission_links)), 'permission_list'),
#	url(r'^permission/(?P<object_id>\d+)/update/$', generic_update, dict({ 'model' : Permission }, extra_context = dict( title = 'privilegio') ), 'permission_update'),
#	url(r'^permission/create/$', generic_create, dict({ 'model' : Permission }, extra_context={ 'title': 'privilegio' }), 'permission_create'),
#	url(r'^permission/(?P<object_id>\d+)/delete/$', generic_delete, dict({ 'model' : Permission }, post_delete_redirect = "/user/list", extra_context={ 'title': 'el privilegio' }) , 'permission_delete'),
)
    

