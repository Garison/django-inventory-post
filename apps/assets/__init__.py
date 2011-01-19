from django.utils.translation import ugettext_lazy as _

state_list = {'text':_('States'), 'view':'state_list'}
state_edit = {'text':_(u'Edit'), 'view':'state_update'}
state_delete = {'text':_(u'Delete'), 'view':'state_delete'}

state_record_links = [
    state_edit, state_delete
]

person_list = {'text':_('View all people'), 'view':'person_list'}
person_create = {'text':_('Create new person'), 'view':'person_create'}
person_update = {'text':_(u'Edit'), 'view':'person_update'}
person_delete = {'text':_(u'Delete'), 'view':'person_delete'}
person_photos = {'text':_(u'Edit photos'), 'view':'person_photos'}
person_assign_item = {'text':_(u'Assign/Remove asset'), 'view':'person_assign_item'}

person_record_links = [
    person_update, person_delete, person_photos, person_assign_item
]

asset_list = {'text':_('View all assets'), 'view':'item_list'}
asset_create = {'text':_('Create new asset'), 'view':'item_create'}
asset_orphan_list = {'text':_('Orphans assets'), 'view':'item_orphans_list'}
asset_edit = {'text':_(u'Edit'), 'view':'item_update'}
asset_delete = {'text':_(u'Delete'), 'view':'item_delete'}
asset_photos = {'text':_(u'Photos'), 'view':'item_photos'}
asset_assign_person = {'text':_(u'Assign/Remove people'), 'view':'item_assign_person'}
asset_template = {'text':_(u'Template'), 'view':'template_view', 'args':'object.item_template.id'}


asset_record_links = [
    asset_edit, asset_delete, asset_photos, asset_assign_person, asset_template
]

group_list = {'text':_(u'View all groups'), 'view':'group_list'}
group_create = {'text':_(u'Create group'), 'view':'group_create'}
group_update = {'text':_(u'Edit'), 'view':'group_update'}
group_delete = {'text' : _(u'Delete'), 'view':'group_delete'}

group_record_links = [
    group_update, group_delete
]
