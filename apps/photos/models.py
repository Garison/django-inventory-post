import os
import random

from PIL import Image	

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
        
THUMBNAIL_SIZE = (80, 60)
PREVIEW_SIZE = (420, 315)
FINAL_SIZE = (800, 600)
        
class Photo(models.Model):
    """
    A photo for my site
    from http://superjared.com/entry/django-quick-tips-2-image-thumbnails/
    """
    #filename
    title = models.CharField(max_length=10, null=True, blank=True, verbose_name=_(u"Title"))
    photo = models.ImageField(upload_to="photos/",verbose_name=_(u"Photo"))
    thumbnail = models.ImageField(upload_to="photos/thumbnails/", editable=False)
    preview = models.ImageField(upload_to="photos/previews/", editable=False)
    main = models.BooleanField(default=False, verbose_name=_(u"Main photo?"))

    def resize(self, source, destination, size):
#		self.save_thumbnail_file(self.get_photo_filename(), '')
        image = Image.open(source)
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')
        image.thumbnail(size, Image.ANTIALIAS)
#try:
#thumbnail.save(self.filename, "JPEG",  quality=75, optimize=1) 
#except IOError: 
#thumbnail.save(self.filename, "JPEG",  quality=75) 			
        if destination != None:
            image.save(destination)
        else:
            return image.getdata()
    
    def create(self, instance=None, item=None):
        if instance == None:
            return

        old_path = self.photo.name
        path, name = os.path.split(old_path)
        name, ext = os.path.splitext(name)
        new_path = os.path.join(path, str(random.randint(0,99999999)) + ext)
        setattr(instance, 'photo', new_path)
        os.rename(os.path.join(settings.MEDIA_ROOT, old_path), os.path.join(settings.MEDIA_ROOT, new_path))
        self.thumbnail.save(self.photo.name, self.photo, save=False)
        self.preview.save(self.photo.path, self.photo, save=False)
        self.resize(self.photo.path, self.preview.path, PREVIEW_SIZE) 
        self.resize(self.photo.path, self.thumbnail.path, THUMBNAIL_SIZE) 
        self.resize(self.photo.path, self.photo.path, FINAL_SIZE) 
        super(Photo, self).save()
        
    class Meta:
        verbose_name = _(u"photo")
        
    def __unicode__(self):
        return self.title 
