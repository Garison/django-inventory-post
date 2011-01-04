from django.db.models.signals import post_save, pre_save
#from models import *
from django.contrib.auth.models import Message

def __get_changelog(sender, instance, old_record=True):
    new_instance = instance

    if old_record:
        try:
            old_instance = sender.objects.get(pk=new_instance.id)
        except:
            old_record = False
    
    change_log = ''

    for field in new_instance.__class__._meta.fields:# + new_instance.__class__._meta.many_to_many:
        new_value = unicode(getattr(new_instance,field.name))

        if old_record:
            old_value = unicode(getattr(old_instance,field.name))
        else:
            old_value = None
        
        if not old_value == new_value:
            if new_value:
                change_log += "field: %s\n===========\n" % unicode(field.verbose_name)
                if old_value:
                    change_log += "old value:\n%s\n\n" % (old_value)
                change_log += "new value:\n%s\n===========\n\n" % (new_value)

    return change_log

def update_log_object_update(sender, **kwargs):
    if sender!=Item or sender!=ItemTemplate or sender!=ItemGroup or sender!=Item or sender!=Person:
        return
        
    try:
        old_instance = sender.objects.get(pk=kwargs['instance'].id)
    except:
        return

    entry = Log(content_object=kwargs['instance'], action="object updated: %s" % kwargs['instance'], description=__get_changelog(sender, kwargs['instance']))
    entry.save()		


def update_log_object_create(sender, **kwargs):
    if sender!=Item or sender!=ItemTemplate or sender!=ItemGroup or sender!=Item or sender!=Person:
        return
        
    if 'created' in kwargs:
        if kwargs['created']:
            entry = Log(content_object=kwargs['instance'], action="object created: %s" % kwargs['instance'], description=__get_changelog(sender, kwargs['instance'],old_record=False))
            entry.save()		

#pre_save.connect(update_log_object_update)
#post_save.connect(update_log_object_create)
