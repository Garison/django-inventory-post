from django.utils.translation import ugettext_lazy as _

from common.api import register_links, register_menu

from models import PurchaseRequestStatus, PurchaseRequest, \
                   PurchaseRequestItem, PurchaseOrderStatus, \
                   PurchaseOrderItemStatus, PurchaseOrder, \
                   PurchaseOrderItem

purchase_request_state_list = {'text':_('purchase request states'), 'view':'purchase_request_state_list', 'famfam':'pencil_go'}
purchase_request_state_create = {'text':_('create new purchase request state'), 'view':'purchase_request_state_create', 'famfam':'pencil_add'}
purchase_request_state_update = {'text':_('edit state'), 'view':'purchase_request_state_update', 'args':'object.id', 'famfam':'pencil'}
purchase_request_state_delete = {'text':_('delete state'), 'view':'purchase_request_state_delete', 'args':'object.id', 'famfam':'pencil_delete'}

purchase_request_list = {'text':_('purchase requests'), 'view':'purchase_request_list', 'famfam':'basket_go'}
purchase_request_create = {'text':_('create new request'), 'view':'purchase_request_create', 'famfam':'basket_add'}
purchase_request_update = {'text':_('edit request'), 'view':'purchase_request_update', 'args':'object.id', 'famfam':'basket_edit'}
purchase_request_delete = {'text':_('delete request'), 'view':'purchase_request_delete', 'args':'object.id', 'famfam':'basket_delete'}
purchase_request_close = {'text':_('close request'), 'view':'purchase_request_close', 'args':'object.id', 'famfam':'cross'}
purchase_request_open = {'text':_('open request'), 'view':'purchase_request_open', 'args':'object.id', 'famfam':'accept'}
purchase_request_po_wizard = {'text':_('purchase order wizard'), 'view':'purchase_order_wizard', 'args':'object.id', 'famfam':'wand'}

purchase_request_item_create = {'text':_('add new item'), 'view':'purchase_request_item_create', 'args':'object.id', 'famfam':'basket_put'}
purchase_request_item_update = {'text':_('edit item'), 'view':'purchase_request_item_update', 'args':'object.id', 'famfam':'basket_go'}
purchase_request_item_delete = {'text':_('delete item'), 'view':'purchase_request_item_delete', 'args':'object.id', 'famfam':'basket_remove'}

purchase_order_state_list = {'text':_('purchase order states'), 'view':'purchase_order_state_list', 'famfam':'pencil_go'}
purchase_order_state_create = {'text':_('create new purchase order state'), 'view':'purchase_order_state_create', 'famfam':'pencil_add'}
purchase_order_state_update = {'text':_('edit state'), 'view':'purchase_order_state_update', 'args':'object.id', 'famfam':'pencil'}
purchase_order_state_delete = {'text':_('delete state'), 'view':'purchase_order_state_delete', 'args':'object.id', 'famfam':'pencil_delete'}

purchase_order_item_state_list = {'text':_('purchase order item states'), 'view':'purchase_order_item_state_list', 'famfam':'pencil_go'}
purchase_order_item_state_create = {'text':_('create new item state'), 'view':'purchase_order_item_state_create', 'famfam':'pencil_add'}
purchase_order_item_state_update = {'text':_('edit state'), 'view':'purchase_order_item_state_update', 'args':'object.id', 'famfam':'pencil'}
purchase_order_item_state_delete = {'text':_('delete state'), 'view':'purchase_order_item_state_delete', 'args':'object.id', 'famfam':'pencil_delete'}

purchase_order_list = {'text':_('purchase orders'), 'view':'purchase_order_list', 'famfam':'cart_go'}
purchase_order_create = {'text':_('create new order'), 'view':'purchase_order_create', 'famfam':'cart_add'}
purchase_order_update = {'text':_('edit order'), 'view':'purchase_order_update', 'args':'object.id', 'famfam':'cart_edit'}
purchase_order_delete = {'text':_('delete order'), 'view':'purchase_order_delete', 'args':'object.id', 'famfam':'cart_delete'}
purchase_order_close = {'text':_('close order'), 'view':'purchase_order_close', 'args':'object.id', 'famfam':'cross'}
purchase_order_open = {'text':_('open order'), 'view':'purchase_order_open', 'args':'object.id', 'famfam':'accept'}

purchase_order_item_create = {'text':_('add new item'), 'view':'purchase_order_item_create', 'args':'object.id', 'famfam':'cart_put'}
purchase_order_item_update = {'text':_('edit item'), 'view':'purchase_order_item_update', 'args':'object.id', 'famfam':'cart_go'}
purchase_order_item_delete = {'text':_('delete item'), 'view':'purchase_order_item_delete', 'args':'object.id', 'famfam':'cart_remove'}
purchase_order_item_close = {'text':_('close item'), 'view':'purchase_order_item_close', 'args':'object.id', 'famfam':'cross'}

jump_to_template = {'text':_(u'template'), 'view':'template_view', 'args':'object.item_template.id', 'famfam':'page_go'}


purchase_request_state_filter = {'name':'purchase_request_status', 'title':_(u'status'), 'queryset':PurchaseRequestStatus.objects.all(), 'destination':'status'}
purchase_order_state_filter = {'name':'purchase_order_status', 'title':_(u'status'), 'queryset':PurchaseOrderStatus.objects.all(), 'destination':'status'}
#purchase_order_active_filter = {'name':'purchase_order_active', 'title':_(u'active'), 'queryset':[True, False], 'destination':'active'}

register_links(PurchaseRequestStatus, [purchase_request_state_update, purchase_request_state_delete])
register_links(['purchase_request_state_create', 'purchase_request_state_list', 'purchase_request_state_update', 'purchase_request_state_delete'], [purchase_request_state_create], menu_name='sidebar')

register_links(PurchaseRequest, [purchase_request_update, purchase_request_delete, purchase_request_item_create, purchase_request_close, purchase_request_open, purchase_request_po_wizard])
register_links(['purchase_request_list', 'purchase_request_create', 'purchase_request_update', 'purchase_request_delete', 'purchase_request_view', 'purchase_order_wizard'], [purchase_request_create], menu_name='sidebar')

register_links(PurchaseRequestItem, [purchase_request_item_update, purchase_request_item_delete, jump_to_template])
register_links(['purchase_request_item_create'], [purchase_request_create], menu_name='sidebar')

register_links(PurchaseOrderStatus, [purchase_order_state_update, purchase_order_state_delete])
register_links(['purchase_order_state_create', 'purchase_order_state_list', 'purchase_order_state_update', 'purchase_order_state_delete'], [purchase_order_state_create], menu_name='sidebar')

register_links(PurchaseOrderItemStatus, [purchase_order_item_state_update, purchase_order_item_state_delete])
register_links(['purchase_order_item_state_create', 'purchase_order_item_state_list', 'purchase_order_item_state_update', 'purchase_order_item_state_delete'], [purchase_order_item_state_create], menu_name='sidebar')

register_links(PurchaseOrder, [purchase_order_update, purchase_order_delete, purchase_order_item_create, purchase_order_close, purchase_order_open])
register_links(['purchase_order_list', 'purchase_order_create', 'purchase_order_update', 'purchase_order_delete', 'purchase_order_view', 'supplier_purchase_orders'], [purchase_order_create], menu_name='sidebar')

register_links(PurchaseOrderItem, [purchase_order_item_update, purchase_order_item_delete, jump_to_template, purchase_order_item_close])
register_links(['purchase_order_item_create'], [purchase_order_create], menu_name='sidebar')


register_menu([
    {'text':_('purchases'), 'view':'purchase_request_list', 'links':[
        purchase_request_list, purchase_request_create, purchase_order_list,
        purchase_order_create 
    ],'famfam':'basket','position':4}])

