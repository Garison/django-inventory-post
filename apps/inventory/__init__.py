from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from models import Location, State

user_menu_links = [
    {'text':_('View all'), 'view':'person_list'},
    {'text':_('Create new'), 'view':'person_create'},
]

user_links = [
    {'text':_(u'Edit'), 'view':'user_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'user_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
    {'text':_(u'Privileges'), 'view':'permission_list', 'icon':'#'}
]

template_menu_links = [
    {'text':_('View all'), 'view':'template_list'},
    {'text':_('Create new'), 'view':'template_create'},
    {'text':_('Orphans'), 'view':'template_orphans_list'},
]

template_record_links = [
    {'text':_(u'Edit'), 'view':'template_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'template_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
    {'text':_(u'Photos'), 'view':'template_photos', 'icon':settings.MEDIA_URL + 'images/camera-photo.png'},
    {'text':_(u'Assets that use this template'), 'view':'template_items_list', 'icon':settings.MEDIA_URL + 'images/folder-saved-search.png'},
    {'text':_(u'Assign/Remove supplies'), 'view':'template_assign_supply', 'icon':settings.MEDIA_URL + 'images/edit-redo.png'},
]


item_menu_links = [
    {'text':_('View all'), 'view':'item_list'},
    {'text':_('Create new'), 'view':'item_create'},
    {'text':_('Orphans'), 'view':'item_orphans_list'},
]


item_record_links = [
    {'text':_(u'Edit'), 'view':'item_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'item_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
    {'text':_(u'Photos'), 'view':'item_photos', 'icon':settings.MEDIA_URL + 'images/camera-photo.png'},
    {'text':_(u'Assign/Remove'), 'view':'item_assign_person', 'icon':settings.MEDIA_URL + 'images/item-plus-user.png'},
    {'text':_(u'Template'), 'view':'template_view', 'icon':settings.MEDIA_URL + 'images/font-x-generic.png', 'args':'object.item_template.id'},
]

inventory_menu_links = [
    {'text':_('View all'), 'view':'inventory_list'},
    {'text':_('Create new'), 'view':'inventory_create'},
]

inventory_links = [
    {'text':_(u'Edit'), 'view':'inventory_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'inventory_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
]

inventory_transactions_menu_links = [
    {'text':_('View all'), 'view':'inventory_transaction_list'},
    {'text':_('Create new'), 'view':'inventory_transaction_create'},
]

inventory_transaction_links = [
    {'text':_(u'Edit'), 'view':'inventory_transaction_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'inventory_transaction_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
]

tools_menu_links = [
    {'text':_('Locations'), 'view':'location_list'},
    {'text':_('States'), 'view':'state_list'},
    {'text':_('Settings'), 'view':'settings'},
]

#TODO: Item groups, item states
navigation = [
    {'text':_('Home'), 'view':'home'},
    {'text':_('Users'), 'view':'person_list', 'links':user_menu_links},
    {'text':_('Templates'), 'view':'template_list', 'links':template_menu_links},
    {'text':_('Assets'), 'view':'item_list', 'links':item_menu_links},
#    {'text':_('Assets states'), 'view':'', 'links':item_states_menu_links},
    {'text':_('Inventories'), 'view':'inventory_list', 'links':inventory_menu_links},
    {'text':_('Inventory transactions'), 'view':'inventory_transaction_list', 'links':inventory_transactions_menu_links},
    {'text':_('Tools'), 'view':'location_list', 'links':tools_menu_links},
    {'text':_('About'), 'view':'about'},
]

location_filter = {
    'location':{'queryset':Location.objects.all(), 'destination':'location'},
}

retireditem_filter = {
    'location':{'queryset':Location.objects.all(), 'destination':'item__location'},
}

    
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

state_links = [
    {'text':_(u'Edit'), 'view':'state_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'state_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
]

#inrepairsitem_links = [
#    {'text': _(u'Repaired'), 'view':'inrepairsitem_unrepair'}
#]


#permission_links = [
#        { 'text' : 	_(u'Edit'), 'view': 'permission_update', 'icon' : MEDIA_URL+'images/accessories-text-editor.png' },
#        { 'text' : 	_(u'Delete'), 'view' : 'permission_delete', 'icon' : MEDIA_URL+'images/emblem-unreadable.png'},
#    ]


