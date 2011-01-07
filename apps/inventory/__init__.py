from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from models import Location


location_filter = {
    'location':{'queryset':Location.objects.all(), 'destination':'location'},
}

retireditem_filter = {
    'location':{'queryset':Location.objects.all(), 'destination':'item__location'},
}

template_record_links = [
    {'text':_(u'Edit'), 'view':'template_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'template_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
    {'text':_(u'Photos'), 'view':'template_photos', 'icon':settings.MEDIA_URL + 'images/camera-photo.png'},
    {'text':_(u'Assets that use this template'), 'view':'template_items_list', 'icon':settings.MEDIA_URL + 'images/folder-saved-search.png'},
    {'text':_(u'Assign/Remove supplies'), 'view':'template_assign_supply', 'icon':settings.MEDIA_URL + 'images/edit-redo.png'},
]
    
item_record_links = [
    {'text':_(u'Edit'), 'view':'item_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'item_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
    {'text':_(u'Photos'), 'view':'item_photos', 'icon':settings.MEDIA_URL + 'images/camera-photo.png'},
    {'text':_(u'Assign/Remove'), 'view':'item_assign_person', 'icon':settings.MEDIA_URL + 'images/item-plus-user.png'},
#    {'text':_(u'Retire'), 'view':'item_retire', 'icon':settings.MEDIA_URL + 'images/user-trash.png'},
#    {'text':_(u'Repair'), 'view':'item_sendtorepairs', 'icon':settings.MEDIA_URL + 'images/broken-computer.png'},
    {'text':_(u'Template'), 'view':'template_view', 'icon':settings.MEDIA_URL + 'images/font-x-generic.png', 'args':'object.item_template.id'},
]
    
#retireditem_links = [
#    {'text':_(u'Reactivate'), 'view':'retireditem_unretire' }
#]

person_links = [
    {'text':_(u'Edit'), 'view':'person_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'person_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
    {'text':_(u'Edit photos'), 'view':'person_photos', 'icon':settings.MEDIA_URL + 'images/camera-photo.png' },
    {'text':_(u'Assign/Remove asset'), 'view':'person_assign_item', 'icon':settings.MEDIA_URL + 'images/item-plus-user.png'},
]

#TODO: autodetect update or delete
group_links = [
    {'text':_(u'Edit'), 'view':'group_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text' : _(u'Delete'), 'view':'group_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
]

location_links = [
    {'text':_(u'Edit'), 'view':'location_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'location_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
]

#inrepairsitem_links = [
#    {'text': _(u'Repaired'), 'view':'inrepairsitem_unrepair'}
#]

user_links = [
    {'text':_(u'Edit'), 'view':'user_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'user_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
    {'text':_(u'Privileges'), 'view':'permission_list', 'icon':'#'}
]

#permission_links = [
#        { 'text' : 	_(u'Edit'), 'view': 'permission_update', 'icon' : MEDIA_URL+'images/accessories-text-editor.png' },
#        { 'text' : 	_(u'Delete'), 'view' : 'permission_delete', 'icon' : MEDIA_URL+'images/emblem-unreadable.png'},
#    ]

inventory_links = [
    {'text':_(u'Edit'), 'view':'inventory_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'inventory_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
]

inventory_transaction_links = [
    {'text':_(u'Edit'), 'view':'inventory_transaction_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'inventory_transaction_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
]
