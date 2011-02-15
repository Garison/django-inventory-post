from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _
from django.views.generic.create_update import create_object, update_object

from generic_views.views import generic_assign_remove, \
                                generic_delete, \
                                generic_detail, generic_list

from photos.views import generic_photos

from models import ItemTemplate, InventoryTransaction, \
                   Inventory, Log, Location, SubLocation, Supplier
                   
from forms import InventoryTransactionForm, InventoryForm, \
                  ItemTemplateForm, ItemTemplateForm_view, LogForm, \
                  SupplierForm, LocationForm_view, SubLocationForm_view

from conf import settings as inventory_settings
                                

urlpatterns = patterns('inventory.views',
    url(r'^template/list/$', generic_list, dict({'queryset':ItemTemplate.objects.all()}, extra_context=dict(title=_(u'item template'))), 'template_list'),
    url(r'^template/create/$', create_object, {'form_class':ItemTemplateForm, 'template_name':'generic_form.html', 'extra_context':{'object_name':_(u'item template')}}, 'template_create'),
    url(r'^template/(?P<object_id>\d+)/update/$', update_object, {'form_class':ItemTemplateForm, 'template_name':'generic_form.html', 'extra_context':{'object_name':_(u'item template')}}, 'template_update' ),
    url(r'^template/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':ItemTemplate}, post_delete_redirect="template_list", extra_context=dict(object_name=_(u'item template'), _message=_(u"Will be deleted from any user that may have it assigned and from any item group."))), 'template_delete' ),
    url(r'^template/orphans/$', generic_list, dict({'queryset':ItemTemplate.objects.filter(item=None)}, extra_context=dict(title=_('orphan templates'))), 'template_orphans_list'),
    url(r'^template/(?P<object_id>\d+)/photos/$', generic_photos, {'model':ItemTemplate, 'max_photos':inventory_settings.MAX_TEMPLATE_PHOTOS}, 'template_photos'), 
    url(r'^template/(?P<object_id>\d+)/$', generic_detail, dict(form_class=ItemTemplateForm_view, queryset=ItemTemplate.objects.all(), extra_context={'object_name':_(u'item template'), 'sidebar_subtemplates':['generic_photos_subtemplate.html']}), 'template_view'),
    url(r'^template/(?P<object_id>\d+)/items/$', 'template_items', (), 'template_items_list'),
    url(r'^template/(?P<object_id>\d+)/assign/supplies$', 'template_assign_remove_supply', (), name='template_assign_supply'),
    url(r'^template/(?P<object_id>\d+)/assign/suppliers/$', 'template_assign_remove_suppliers', (), name='template_assign_suppliers'),

    url(r'^inventory/list/$', generic_list, dict({'queryset':Inventory.objects.all()}, extra_context=dict(title=_(u'inventories'), extra_columns=[{'name':_(u'location'), 'attribute':'location'}])), 'inventory_list'),
    url(r'^inventory/create/$', create_object, {'model':Inventory, 'template_name':'generic_form.html', 'extra_context':{'object_name':_(u'inventory')}}, 'inventory_create'),
    url(r'^inventory/(?P<object_id>\d+)/$', 'inventory_view', (),'inventory_view'),
    url(r'^inventory/(?P<object_id>\d+)/update/$', update_object, {'form_class':InventoryForm, 'template_name':'generic_form.html', 'extra_context':{'object_name':_(u'inventory')}}, 'inventory_update'),
    url(r'^inventory/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':Inventory}, post_delete_redirect="inventory_list", extra_context=dict(object_name=_(u'inventory'))), 'inventory_delete'),
    url(r'^inventory/(?P<object_id>\d+)/current/$', 'inventory_current', (), 'inventory_current'),
    url(r'^inventory/(?P<object_id>\d+)/transaction/create/$', 'inventory_create_transaction', (), 'inventory_create_transaction'),

    url(r'^transaction/list/$', generic_list, dict({'queryset':InventoryTransaction.objects.all()}, extra_context=dict(title=_(u'transactions'))), 'inventory_transaction_list'),
    url(r'^transaction/create/$', create_object, {'model':InventoryTransaction, 'template_name':'generic_form.html', 'extra_context':{'object_name':_(u'transaction')}}, 'inventory_transaction_create'),
    url(r'^transaction/(?P<object_id>\d+)/$', generic_detail, dict(form_class=InventoryTransactionForm, queryset=InventoryTransaction.objects.all(), extra_context={'object_name':_(u'transaction')}), 'inventory_transaction_view'),
    url(r'^transaction/(?P<object_id>\d+)/update/$', update_object, {'model':InventoryTransaction, 'template_name':'generic_form.html', 'extra_context':{'object_name':_(u'transaction')}}, 'inventory_transaction_update'),
    url(r'^transaction/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':InventoryTransaction}, post_delete_redirect="inventory_transaction_list", extra_context=dict(object_name=_(u'inventory transaction'))), 'inventory_transaction_delete'),

    url(r'^location/list/$', generic_list, dict({'queryset':Location.objects.all()}, extra_context=dict(title =_(u'locations'))), 'location_list'),
    url(r'^location/create/$', create_object, {'model':Location, 'template_name':'generic_form.html'}, 'location_create'),
    url(r'^location/(?P<object_id>\d+)/update/$', update_object, {'model':Location, 'template_name':'generic_form.html'}, 'location_update'),
    url(r'^location/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':Location}, post_delete_redirect="location_list", extra_context=dict(object_name=_(u'locations'))), 'location_delete'),
    url(r'^location/(?P<object_id>\d+)/$', generic_detail, dict(form_class=LocationForm_view, queryset=Location.objects.all()), 'location_view'),
   
  url(r'^sublocation/list/$', generic_list, dict({'queryset':SubLocation.objects.all()}, extra_context=dict(title =_(u'sublocations'))), 'sublocation_list'),
    url(r'^sublocation/create/$', create_object, {'model':SubLocation, 'template_name':'generic_form.html'}, 'sublocation_create'),
    url(r'^sublocation/(?P<object_id>\d+)/update/$', update_object, {'model':SubLocation, 'template_name':'generic_form.html'}, 'sublocation_update'),
url(r'^sublocation/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':SubLocation}, post_delete_redirect="Sublocation_list", extra_context=dict(object_name=_(u'sublocations'))), 'sublocation_delete'),
   
    url(r'^sublocation/(?P<object_id>\d+)/$', generic_detail, dict(form_class=SubLocationForm_view, queryset=SubLocation.objects.all()), 'sublocation_view'),


    url(r'^supplier/(?P<object_id>\d+)/$', generic_detail, dict(form_class=SupplierForm, queryset=Supplier.objects.all()), 'supplier_view'),
    url(r'^supplier/list/$', generic_list, dict({'queryset':Supplier.objects.all()}, extra_context=dict(title=_(u'suppliers'))), 'supplier_list'),
    url(r'^supplier/create/$', create_object, {'form_class':SupplierForm, 'template_name':'generic_form.html'}, 'supplier_create'),
    url(r'^supplier/(?P<object_id>\d+)/update/$', update_object, {'form_class':SupplierForm, 'template_name':'generic_form.html'}, 'supplier_update'),
    url(r'^supplier/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':Supplier}, post_delete_redirect="supplier_list", extra_context=dict(object_name=_(u'supplier'))), 'supplier_delete'),
    url(r'^supplier/(?P<object_id>\d+)/assign/itemtemplates/$', 'supplier_assign_remove_itemtemplates', (), 'supplier_assign_itemtemplates'),
    url(r'^supplier/(?P<object_id>\d+)/purchase/orders/$', 'supplier_purchase_orders', (), 'supplier_purchase_orders'),
    
#    url(r'^reports/items_per_person/(?P<object_id>\d+)/$', 'report_items_per_person', (), 'report_items_per_person'),
)
    

