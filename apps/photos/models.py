from photologue.models import ImageModel

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
        
        
class GenericPhotoManager(models.Manager):
    def photos_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id, object_id=obj.id)        
        
        
class GenericPhoto(ImageModel):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    title = models.CharField(max_length=10, null=True, blank=True, verbose_name=_(u"Title"))
    main = models.BooleanField(default=False, verbose_name=_(u"Main photo?"))

    objects = GenericPhotoManager()

    class Meta:
        verbose_name = _(u"photo")
        verbose_name_plural = _(u"photos")
        
    def __unicode__(self):
        return "%s - %s" % (self.content_object, self.title) 
