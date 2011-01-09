from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from models import Location, State

person_list = {'text':_('View all people'), 'view':'person_list'}
person_create = {'text':_('Create new person'), 'view':'person_create'}
person_update = {'text':_(u'Edit'), 'view':'person_update'}
person_delete = {'text':_(u'Delete'), 'view':'person_delete'}
person_photos = {'text':_(u'Edit photos'), 'view':'person_photos'}
person_assign_item = {'text':_(u'Assign/Remove asset'), 'view':'person_assign_item'}

asset_list = {'text':_('View all assets'), 'view':'item_list'}
asset_create = {'text':_('Create new asset'), 'view':'item_create'}
asset_orphan_list = {'text':_('Orphans assets'), 'view':'item_orphans_list'}

person_links = [
    person_update, person_delete, person_photos, person_assign_item
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
    asset_list, asset_create, asset_orphan_list   
]

item_record_links = [
    {'text':_(u'Edit'), 'view':'item_update'},
    {'text':_(u'Delete'), 'view':'item_delete'},
    {'text':_(u'Photos'), 'view':'item_photos'},
    {'text':_(u'Assign/Remove people'), 'view':'item_assign_person'},
    {'text':_(u'Template'), 'view':'template_view'},
]


group_list = {'text':_(u'View all groups'), 'view':'group_list'}
group_create = {'text':_(u'Create group'), 'view':'group_create'}
group_update = {'text':_(u'Edit'), 'view':'group_update'}
group_delete = {'text' : _(u'Delete'), 'view':'group_delete'}

group_links = [
    group_update, group_delete
]

inventory_list = {'text':_('View all inventories'), 'view':'inventory_list'}
inventory_create = {'text':_('Create new inventory'), 'view':'inventory_create'}

inventory_transaction_list = {'text':_('View all transactions'), 'view':'inventory_transaction_list'}
inventory_transaction_create = {'text':_('Create new transaction'), 'view':'inventory_transaction_create'}

inventory_menu_links = [
    inventory_list, inventory_create, inventory_transaction_list, inventory_transaction_create
]

inventory_links = [
    {'text':_(u'Current balances'), 'view':'inventory_current'},
    {'text':_(u'Edit'), 'view':'inventory_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'inventory_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
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

navigation = [
    {'text':_('Home'), 'view':'home', 'famfam':'house'},
    {'text':_('People'), 'view':'person_list', 'links':[
        person_list, person_create
    ]},
    {'text':_('Templates'), 'view':'template_list', 'links':template_menu_links, 'famfam':'page'},
    {'text':_('Assets'), 'view':'item_list', 'links':[
        asset_list, asset_create, asset_orphan_list, group_list, group_create 
    ]},
    {'text':_('Asset states'), 'view':'item_state_list_init'},
    {'text':_('Inventories'), 'view':'inventory_list', 'links':inventory_menu_links,'famfam':'book'},
    {'text':_('Tools'), 'view':'location_list', 'links':tools_menu_links,'famfam':'wrench'},
    {'text':_('Search'), 'view':'search', 'famfam':'zoom'},
    {'text':_('About'), 'view':'about'},
]

location_filter = {
    'location':{'queryset':Location.objects.all(), 'destination':'location'},
}

location_links = [
    {'text':_(u'Edit'), 'view':'location_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'location_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
]

state_links = [
    {'text':_(u'Edit'), 'view':'state_update', 'icon':settings.MEDIA_URL + 'images/accessories-text-editor.png'},
    {'text':_(u'Delete'), 'view':'state_delete', 'icon':settings.MEDIA_URL + 'images/emblem-unreadable.png'},
]

