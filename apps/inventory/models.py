from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse

class Settings(models.Model):
    max_photo_size = models.IntegerField(default=1000000, verbose_name=_(u'Maximum photo size.'), help_text=_(u'Limit in kilobytes.'))
    max_item_photos = models.IntegerField(default=5, verbose_name=_(u'Maximum photos per item.'))
    max_template_photos = models.IntegerField(default=5, verbose_name=_(u'Maximum photos per item template.'))
    max_person_photos = models.IntegerField(default=5, verbose_name=_(u'Maximum photos per user.'))
    is_anon_restricted = models.BooleanField(default=True, verbose_name=_(u'Required login?'))

    class Meta:
        verbose_name = _(u"settings")

    def __unicode__(self):
        return unicode(_(u"settings"))

    def get_absolute_url(self):
        return reverse('settings')
 
 
class Photo(models.Model):
    #http://code.google.com/p/django-profile-images/
#	def get_image_path(instance, filename):
#		return 'photos/%s/%s' % (instance.id, filename)
    
    """
    A photo for my site
    from http://superjared.com/entry/django-quick-tips-2-image-thumbnails/
    """
    #filename
    title = models.CharField(max_length=10, null=True, blank=True, verbose_name = _(u"Title"))
    photo = models.ImageField(upload_to="userfiles/photos/",verbose_name = _(u"Photo"))
    thumbnail = models.ImageField(upload_to="userfiles/photos/thumbnails/", editable=False)
    preview = models.ImageField(upload_to="userfiles/photos/previews/", editable=False)
    main = models.BooleanField(default=False, verbose_name = _(u"Main photo?"))

#	def _super
#		self.file_name = str(random.randint(0,99999999))


    def resize(self, source, destination, size):
        from PIL import Image	
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
        #print im.format, im.size, im.mode
        #PPM (512, 512) RGB	
        
        THUMBNAIL_SIZE = (80, 60)
        PREVIEW_SIZE = (420, 315)
        FINAL_SIZE = (800, 600)
    
        import os
        import random
        from django.conf import settings
        
        if instance == None:
            return

        old_path = self.photo.name
        path, name = os.path.split(old_path)
        name, ext = os.path.splitext(name)
        new_path = os.path.join(path, str(random.randint(0,99999999)) + ext)
        setattr(instance, 'photo', new_path)
        os.rename(settings.MEDIA_ROOT + old_path, settings.MEDIA_ROOT+new_path)
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


class RegionalOffice(models.Model):
    name = models.CharField(verbose_name=_(u"Regional"), max_length=32)

    class Meta:
        ordering = ['name']
        verbose_name = _(u"regional")
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('regional_list')


class Department(models.Model):
    regional_office = models.ForeignKey(RegionalOffice, verbose_name=_("Regional"))
    name = models.CharField(verbose_name=_(u"Department/Section/Area"), max_length=32)

    class Meta:
        ordering = ['name']
        verbose_name = _(u"department")

    def __unicode__(self):
        return self.regional_office.name + '/' + self.name

    def get_absolute_url(self):
        return reverse('department_list')


class Supply(models.Model):
    description = models.CharField(verbose_name=_(u"Description"), max_length=64)
    brand = models.CharField(verbose_name=_("Brancd"), max_length=32, null=True, blank=True)
    model = models.CharField(verbose_name=_("Model"), max_length=32, null=True, blank=True)
    part_number = models.CharField(verbose_name=_(u"Part number"), max_length=32, null=True, blank=True)
    photos = models.ManyToManyField(Photo, null=True, blank=True, verbose_name = _("Photos"))
    notes = models.TextField(_("Notes/Observations"), null=True, blank=True)	
    
    class Meta:
        ordering = ['description']	
        verbose_name = _(u"article")
    
    def get_absolute_url(self):
        return ('supply_view', [str(self.id)])
    get_absolute_url = models.permalink(get_absolute_url)
    
    def __unicode__(self):
        return self.description

    def get_owners(self):
        try:
            return self.itemtemplate_set.all()
        except:
            return None

    def get_nonowners(self):
        return ItemTemplate.objects.all().exclude(id__in=self.itemtemplate_set.values_list("id",  flat=True))	
    
    def add_owner(self, template):
        if self not in template.supplies.all():
            template.supplies.add(self)		

    def remove_owner(self, template):
        if self in template.supplies.all():
            template.supplies.remove(self)		

            
class ItemTemplate(models.Model):
    description = models.CharField(verbose_name=_(u"Description"), max_length=64)
    brand = models.CharField(verbose_name=_("Brand"), max_length=32, null=True, blank=True)
    model = models.CharField(verbose_name=_("Model"), max_length=32, null=True, blank=True)
    part_number = models.CharField(verbose_name=_(u"Part number"), max_length=32, null=True, blank=True)
    photos = models.ManyToManyField(Photo, null=True, blank=True, verbose_name = _("Photos"))
    notes = models.TextField(_("Notes/Observations"), null=True, blank=True)	
    supplies = models.ManyToManyField(Supply, null=True, blank=True, verbose_name=_(u"Articles"))
    
    class Meta:
        ordering = ['description']	
        verbose_name = _(u"item template")
    
    def get_absolute_url(self):
        return ('template_view', [str(self.id)])
    get_absolute_url = models.permalink(get_absolute_url)
    
#	def get_photos(self):
#		return ItemPhoto.objects.filter(item=self)

    def __unicode__(self):
        return self.description


class ItemManager(models.Manager):
    def get_query_set(self):
        return super(ItemManager, self).get_query_set().filter(active=True)


class ItemManagerPassthru(models.Manager):
    def get_query_set(self):
        return super(ItemManagerPassthru, self).get_query_set()


class Item(models.Model):
    item_template = models.ForeignKey(ItemTemplate, verbose_name=_(u"item template"))
    property_number = models.CharField(_(u"Asset number"), max_length=10)
    notes = models.TextField(_(u"Notes/Observations"), null=True, blank=True)	
    serial_number = models.CharField(verbose_name=_(u"Serial number"), max_length=30, null=True, blank=True)
    regional_office = models.ForeignKey(RegionalOffice, verbose_name=_("Regional"))
    department = models.ForeignKey(Department, verbose_name=_(u"Department/Section/Area"), null=True, blank=True)
    photos = models.ManyToManyField(Photo, null=True, blank=True,  verbose_name = _("Photos"))
    active = models.BooleanField(default=True)
    objects = ItemManager()
    objects_passthru = ItemManagerPassthru()
    
    class Meta:
        ordering = ['property_number']
        verbose_name = _(u"item")

    def get_absolute_url(self):
        return ('item_view', [str(self.id)])
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        in_repairs = self.is_inrepairs()
        if in_repairs:
            rep=_(u"(in repairs)")
        else:
            rep=''
            
        return "#%s, '%s' %s" % (self.property_number, self.item_template.description, rep)

    def is_orphan(self):
        if self.person_set.all():
            return False
        else:
            return True

    def get_owners(self):
        try:
            return self.person_set.all()
        except:
            return None

    def get_nonowners(self):
        return Person.objects.all().exclude(id__in=self.person_set.values_list("id",  flat=True))	
    
    def add_owner(self, person):
        if self not in person.inventory.all():
            person.inventory.add(self)		

    def remove_owner(self, person):
#		if self in person.inventory.all():
        person.inventory.remove(self)		

    def get_absolute_url(self):
        return ('item_view', [str(self.id)])
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_photos(self):
        return ItemPhoto.objects.filter(item=self)
        
    def is_inrepairs(self):
        try:
            return InRepairsItem.objects.get(item=self)
        except:
            return False

    
class ItemGroup(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=32)
    items = models.ManyToManyField(Item, verbose_name=_("Item"))
    
    class Meta:
        ordering = ['name']
        verbose_name = _(u"item group")
        
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return ('group_view', [str(self.id)])
    get_absolute_url = models.permalink(get_absolute_url)		

        
class RetiredItem(models.Model):
    date = models.DateField(verbose_name=_("date"), auto_now_add=True)
    item = models.OneToOneField(Item, verbose_name=_("item"))
    #user
    
    def get_absolute_url(self):
        return ('retireditem_view', [str(self.id)])
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return unicode(self.item)


class InRepairsItem(models.Model):		
    date = models.DateField(verbose_name=_("date"), auto_now_add=True)
    item = models.OneToOneField(Item, verbose_name=_("item"))
#	user

    def get_absolute_url(self):
        return ('inrepairsitem_view', [str(self.id)])
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return unicode(self.item)


class Person(models.Model):
    last_name = models.CharField(_("last name"), max_length=32)
    second_last_name = models.CharField(_("second last name"), max_length=32, blank=True, null=True)
    first_name = models.CharField(_("first name"), max_length=32)
    second_name = models.CharField(_("second name or initial"), max_length=32, blank=True, null=True)
    regional_office = models.ForeignKey(RegionalOffice, verbose_name=_("regional"))
    inventory = models.ManyToManyField(Item, blank=True, null=True, verbose_name=_("inventory"))
    photos = models.ManyToManyField(Photo, null=True, blank=True,  verbose_name = _("photos"))

    class Meta:
        ordering = ['last_name', 'second_last_name', 'first_name', 'second_name']
        verbose_name = _(u"user")

    def get_absolute_url(self):
        return ('person_view', [str(self.id)])
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return "%s %s, %s %s" % (self.last_name, self.second_last_name, self.first_name, self.second_name)


class CustomUser(User):
    person = models.ForeignKey(Person, blank=True, null=True)
    regional = models.ForeignKey(RegionalOffice, blank=True, null=True)
    department = models.ForeignKey(Department, blank=True, null=True)

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()
    
    def __unicode__(self):
        return "%s - %s" % (self.username, self.person)
        
    def get_absolute_url(self):
        return ('user_view', [str(self.id)])
    get_absolute_url = models.permalink(get_absolute_url)		

        
class Permission(models.Model):
    user = models.ForeignKey(CustomUser)
    regional_office = models.ForeignKey(RegionalOffice, unique=True)

    PERMISSION_CHOICES = (
        ('ro', 'Read-only'),
        ('rw', 'Read-Write'),
        ('wd', 'Read-Write-Delete'),
       )
    permission = models.CharField(max_length=2, choices=PERMISSION_CHOICES)

    def get_absolute_url(self):
        return ('permission_update', [str(self.id)])
    get_absolute_url = models.permalink(get_absolute_url)	

    def __unicode__(self):
        return "%s - %s - %s" % (self.user.username, self.regional_office, self.get_permission_display())

    
class Log(models.Model):
    timedate = models.DateTimeField(auto_now_add=True, verbose_name=_(u"timedate"))
    action = models.CharField(max_length=32)
    description = models.TextField(verbose_name=_(u"description"), null=True, blank=True)
    #user = models.ForeignKey(User, unique=True)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    def __unicode__(self):
#		return "%Y-%m-%d %H:%M:%S" % (self.timedate) #& user  && item
        return "%s, %s - %s" % (self.timedate, self.action, self.content_object)

    def get_absolute_url(self):
        return ('log_view', [str(self.id)])
    get_absolute_url = models.permalink(get_absolute_url)


class Inventory(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u'name'))
    regional_office = models.ForeignKey(RegionalOffice, verbose_name=_(u'regional'))

    def get_absolute_url(self):
        return ('inventory_view', [str(self.id)])
    get_absolute_url = models.permalink(get_absolute_url)		

    def __unicode__(self):
        return "%s, %s" % (self.regional_office, self.name)


class InventoryCheckPoint(models.Model):
    import datetime
    inventory = models.ForeignKey(Inventory)
    datetime = models.DateTimeField(default=datetime.datetime.now())	
    supplies = models.ManyToManyField(Supply, null=True, blank=True, through='InventoryCPQty')


class InventoryCPQty(models.Model):
    supply = models.ForeignKey(Supply)
    check_point = models.ForeignKey(InventoryCheckPoint)
    quantity = models.IntegerField()

    
class InventoryTransaction(models.Model):
    import datetime
    inventory = models.ForeignKey(Inventory)
    supply = models.ForeignKey(Supply)
    quantity = models.IntegerField()
    date = models.DateField(default=datetime.date.today(), verbose_name=_(u"date"))
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = _(u'transaction')
        verbose_name_plural = _(u'transactions')

    def get_absolute_url(self):
        return ('inventory_transaction_view', [str(self.id)])
    get_absolute_url = models.permalink(get_absolute_url)	
    
    def __unicode__(self):
        return "%s: '%s' qty=%s @ %s" % (self.inventory, self.supply, self.quantity, self.date)
