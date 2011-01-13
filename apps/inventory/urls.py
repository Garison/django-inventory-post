from django.conf.urls.defaults import *
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.views.generic.create_update import create_object, update_object

from photos.views import generic_photos

from inventory import person_links, \
                      template_record_links, inventory_links, \
                      item_record_links, state_links, \
                      inventory_transaction_links, \
                      group_links, location_filter, location_links, \
                      suppliers_record_links


from models import ItemTemplate, InventoryTransaction, \
                   Inventory, Settings, Item, ItemGroup, Person, \
                   Log, Location, State, Supplier
                   
from forms import InventoryTransactionForm, InventoryForm, \
                  ItemTemplateForm, ItemTemplateForm_view, ItemForm, \
                  ItemForm_view, ItemGroupForm, PersonForm, \
                  LogForm, SupplierForm, PersonForm_view, LocationForm_view

from generic_views.views import generic_assign_remove, \
                                generic_delete, \
                                generic_detail, generic_list
                                

urlpatterns = patterns('inventory.views',
    url(r'^person/(?P<object_id>\d+)/photos/$', generic_photos, {'model':Person, 'max_photos':Settings.objects.get(pk=1).max_person_photos}, 'person_photos'), 
    url(r'^person/(?P<object_id>\d+)/$', generic_detail, {'form_class':PersonForm_view, 'queryset':Person.objects.all(), 'create_view':'person_create', 'record_links':person_links, 'extra_context':{'subtemplates':['generic_photos_subtemplate.html']}}, 'person_view'),
    url(r'^person/list/$', generic_list, {'queryset':Person.objects.all(), 'list_filter':location_filter, 'extra_context':{'title':_(u'people'), 'create_view':"person_create", 'record_links':person_links}}, 'person_list'),
    url(r'^person/create/$', create_object, {'form_class':PersonForm, 'template_name':'generic_form.html'}, 'person_create'),
    url(r'^person/(?P<object_id>\d+)/update/$', update_object, {'form_class':PersonForm, 'template_name':'generic_form.html'}, 'person_update'),
    url(r'^person/(?P<object_id>\d+)/delete/$', generic_delete, {'model':Person, 'post_delete_redirect':'person_list', 'extra_context':{'title':_(u'person')}}, 'person_delete'),
    url(r'^person/(?P<object_id>\d+)/assign/$', 'person_assign_remove_item', (), 'person_assign_item'),

    url(r'^template/list/$', generic_list, dict({'queryset':ItemTemplate.objects.all()}, extra_context=dict(title=_(u'item template'), create_view="template_create", record_links=template_record_links)), 'template_list'),
    url(r'^template/create/$', create_object, {'form_class':ItemTemplateForm, 'template_name':'generic_form.html'}, 'template_create'),
    url(r'^template/(?P<object_id>\d+)/update/$', update_object, {'form_class':ItemTemplateForm, 'template_name':'generic_form.html'}, 'template_update' ),
    url(r'^template/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':ItemTemplate}, post_delete_redirect="template_list", extra_context=dict(title=_(u'item template'), _message=_(u"Will be deleted from any user that may have it assigned and from any item group."))), 'template_delete' ),
    url(r'^template/orphans/$', generic_list, dict({'queryset':ItemTemplate.objects.filter(item=None)}, extra_context=dict(title=_('orphan templates'), create_view='template_create', record_links=template_record_links)), 'template_orphans_list'),
    url(r'^template/(?P<object_id>\d+)/photos/$', generic_photos, {'model':ItemTemplate, 'max_photos':Settings.objects.get(pk=1).max_template_photos }, 'template_photos'), 
    url(r'^template/(?P<object_id>\d+)/$', generic_detail, dict(form_class=ItemTemplateForm_view, queryset=ItemTemplate.objects.all(), create_view='template_create', record_links=template_record_links, extra_context={'subtemplates':['generic_photos_subtemplate.html']}), 'template_view'),
    url(r'^template/(?P<object_id>\d+)/items/$', 'template_items', (), 'template_items_list'),
    url(r'^template/(?P<object_id>\d+)/assign/supplies$', 'template_assign_remove_supply', (), name='template_assign_supply'),
    url(r'^template/(?P<object_id>\d+)/assign/suppliers/$', 'template_assign_remove_suppliers', (), name='template_assign_suppliers'),

    url(r'^asset/create/$', create_object, {'form_class':ItemForm, 'template_name':'generic_form.html'}, 'item_create'),
    url(r'^asset/(?P<object_id>\d+)/update/$', update_object, {'form_class':ItemForm, 'template_name':'generic_form.html'}, 'item_update'),
    url(r'^asset/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':Item}, post_delete_redirect="item_list", extra_context=dict(title=_(u'asset'))), 'item_delete'),
    url(r'^asset/(?P<object_id>\d+)/assign/$', 'item_assign_remove_person', (), name='item_assign_person'),
    url(r'^asset/orphans/$', generic_list, dict({'queryset':Item.objects.filter(person=None)}, list_filter=location_filter, extra_context=dict(title=_(u'orphan assets'), create_view='item_create', record_links=item_record_links)), 'item_orphans_list'),
    url(r'^asset/list/$', generic_list, dict({'queryset':Item.objects.all()}, list_filter=location_filter, extra_context=dict(title=_(u'assets'), create_view='item_create', record_links=item_record_links)), 'item_list'),
    url(r'^asset/(?P<object_id>\d+)/$', generic_detail, dict(form_class=ItemForm_view, queryset=Item.objects.all(), create_view='item_create', record_links=item_record_links, extra_context={'subtemplates':['generic_photos_subtemplate.html', 'state_subtemplate.html']}, extra_fields=[{'field':'get_owners', 'label':_(u'Assigned to users:')}]), 'item_view'),
    url(r'^asset/(?P<object_id>\d+)/photos/$', generic_photos, dict(model=Item, max_photos=Settings.objects.get(pk=1).max_item_photos), 'item_photos'), 
    url(r'^asset/(?P<object_id>\d+)/state/(?P<state_id>\d+)/set/$', 'item_setstate', (), 'item_setstate'),
    url(r'^asset/(?P<object_id>\d+)/state/(?P<state_id>\d+)/unset$', 'item_remove_state', (), 'item_remove_state'),
    url(r'^asset/state/init/$', 'item_state_list_init', (), 'item_state_list_init'),
    url(r'^asset/state/(?P<state_id>\d+)/list/$', 'item_state_list', (), 'item_state_list'),

    url(r'^group/list/$', generic_list, dict({'queryset':ItemGroup.objects.all()}, extra_context=dict(title=_(u'item groups'), create_view='group_create', record_links=group_links)), 'group_list'),
    url(r'^group/create/$', create_object, {'form_class':ItemGroupForm, 'template_name':'generic_form.html'}, 'group_create'),
    url(r'^group/(?P<object_id>\d+)/$', generic_detail, dict(form_class=ItemGroupForm, queryset=ItemGroup.objects.all(), create_view='group_create', record_links=group_links), 'group_view'),
    url(r'^group/(?P<object_id>\d+)/update/$', 'group_assign_remove_item', (), name='group_update'),
    url(r'^group/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':ItemGroup}, post_delete_redirect="group_list", extra_context=dict(title=_(u'item group'))), 'group_delete'),

    url(r'^inventory/list/$', generic_list, dict({'queryset':Inventory.objects.all()}, extra_context=dict(title=_(u'inventories'), create_view='inventory_create', record_links=inventory_links)), 'inventory_list'),
    url(r'^inventory/create/$', create_object, {'model':Inventory, 'template_name':'generic_form.html'}, 'inventory_create'),
    url(r'^inventory/(?P<object_id>\d+)/$', generic_detail, dict(form_class=InventoryForm, queryset=Inventory.objects.all(), create_view='inventory_create', record_links=inventory_links), 'inventory_view'),
    url(r'^inventory/(?P<object_id>\d+)/update/$', update_object, {'form_class':InventoryForm, 'template_name':'generic_form.html'}, 'inventory_update'),
    url(r'^inventory/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':Inventory}, post_delete_redirect="inventory_list", extra_context=dict(title=_(u'inventory'))), 'inventory_delete'),
    url(r'^inventory/(?P<object_id>\d+)/current/$', 'inventory_current', (), 'inventory_current'),

    url(r'^transaction/list/$', generic_list, dict({'queryset':InventoryTransaction.objects.all()}, extra_context=dict(title=_(u'transactions'), create_view='inventory_transaction_create', record_links=inventory_transaction_links)), 'inventory_transaction_list'),
    url(r'^transaction/create/$', create_object, {'model':InventoryTransaction, 'template_name':'generic_form.html'}, 'inventory_transaction_create'),
    url(r'^transaction/(?P<object_id>\d+)/$', generic_detail, dict(form_class=InventoryTransactionForm, queryset=InventoryTransaction.objects.all(), title=_(u'Transaction details'), create_view='inventory_transaction_create', record_links=inventory_transaction_links), 'inventory_transaction_view'),
    url(r'^transaction/(?P<object_id>\d+)/update/$', update_object, {'model':InventoryTransaction, 'template_name':'generic_form.html'}, 'inventory_transaction_update'),
    url(r'^transaction/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':InventoryTransaction}, post_delete_redirect="inventory_transaction_list"), 'inventory_transaction_delete'),

    url(r'^location/list/$', generic_list, dict({'queryset':Location.objects.all()}, extra_context=dict(title =_(u'locations'), create_view='location_create', record_links=location_links)), 'location_list'),
    url(r'^location/create/$', create_object, {'model':Location, 'template_name':'generic_form.html'}, 'location_create'),
    url(r'^location/(?P<object_id>\d+)/update/$', update_object, {'model':Location, 'template_name':'generic_form.html'}, 'location_update'),
    url(r'^location/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':Location}, post_delete_redirect="location_list", extra_context=dict(title=_(u'locations'))), 'location_delete'),
    url(r'^location/(?P<object_id>\d+)/$', generic_detail, dict(form_class=LocationForm_view, queryset=Location.objects.all(), create_view='location_create', record_links=location_links), 'location_view'),

    url(r'^state/list/$', generic_list, dict({'queryset':State.objects.all()}, extra_context=dict(title =_(u'states'), create_view='state_create', record_links=state_links)), 'state_list'),
    url(r'^state/create/$', create_object, {'model':State, 'template_name':'generic_form.html'}, 'state_create'),
    url(r'^state/(?P<object_id>\d+)/update/$', update_object, {'model':State, 'template_name':'generic_form.html'}, 'state_update'),
    url(r'^state/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':State}, post_delete_redirect="state_list", extra_context=dict(title=_(u'states'))), 'state_delete'),

    url(r'^supplier/(?P<object_id>\d+)/$', generic_detail, dict(form_class=SupplierForm, queryset=Supplier.objects.all(), create_view='supplier_create', record_links=suppliers_record_links), 'supplier_view'),
    url(r'^supplier/list/$', generic_list, dict({'queryset':Supplier.objects.all()}, extra_context=dict(title=_(u'suppliers'), create_view="supplier_create", record_links=suppliers_record_links)), 'supplier_list'),
    url(r'^supplier/create/$', create_object, {'form_class':SupplierForm, 'template_name':'generic_form.html'}, 'supplier_create'),
    url(r'^supplier/(?P<object_id>\d+)/update/$', update_object, {'form_class':SupplierForm, 'template_name':'generic_form.html'}, 'supplier_update'),
    url(r'^supplier/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':Supplier}, post_delete_redirect="supplier_list", extra_context=dict(title=_(u'supplier'))), 'supplier_delete'),
    url(r'^supplier/(?P<object_id>\d+)/assign/itemtemplates/$', 'supplier_assign_remove_itemtemplates', (), 'supplier_assign_itemtemplates'),

    url(r'^search/$', 'search', (), 'search'),

    url(r'^settings/$', update_object, {'model':Settings, 'template_name':'generic_form.html', 'object_id':1}, 'settings'),

#    url(r'^reports/items_per_person/(?P<object_id>\d+)/$', 'report_items_per_person', (), 'report_items_per_person'),
)
    

