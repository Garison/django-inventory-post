import os

from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from conf import settings as photos_settings

from forms import PhotoForm

from models import GenericPhoto

def generic_photos(request, model, object_id, max_photos=5, extra_context={}):
    model_instance = get_object_or_404(model, pk=object_id)
    photos = GenericPhoto.objects.photos_for_object(model_instance)

    if request.method == 'POST' and photos.count() < max_photos:
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.image.size > photos_settings.MAX_PHOTO_SIZE:
                messages.error(request, _(u'The photo is too big.'))
                os.unlink(instance.photo.path)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

#				ext = os.path.splitext(os.path.split(instance.get_photo_filename()))
#				if ext != '.png' and ext != '.jpg' and ext != '.gif':
#					_flash_message(request, _(u'El solo fotos de tipo: PNG, JPG o GIF son permitidas.'), type='error')
#					os.unlink(instance.get_photo_filename())
#					return HttpResponseRedirect('/photos/' + str(ad.number))
            
            instance.object_id = object_id
            instance.content_type = ContentType.objects.get_for_model(model)                
            instance.save()

            photos = GenericPhoto.objects.photos_for_object(model_instance)
            if photos.filter(main=True).count() == 0:
                new_main_photo = photos[0]
                new_main_photo.main=True
                new_main_photo.save()
                            
            messages.success(request, _(u'The photo was added successfully.'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    else:
        form = PhotoForm()
        
    extra_context.update({
        'title':_(u'photos for%(object_name)s%(max_photos)s: %(object)s') % {
                'object_name':' %s' % unicode(extra_context['object_name']) if 'object_name' in extra_context else '',
                'object':model_instance,
                'max_photos': (_(u' (maximum of %s)') % max_photos if max_photos else '')
            },
        'object':model_instance,
        'object_list':photos,
        'hide_object':True,
        'extra_columns':[
            {'name':_(u'photo'),'attribute':lambda x: '<div class="gallery"><a href="%s"><img src="%s" /></a></div>' % (x.get_display_url(), x.get_thumbnail_url())},
            {'name':_(u'main photo'),'attribute':lambda x: '<span class="famfam active famfam-accept"></span>' if x.main else '-'},
            {'name':_(u'title'),'attribute':lambda x: x.title if x.title else '-'}
        ],
    })

    if GenericPhoto.objects.photos_for_object(model_instance).count() < max_photos:
        extra_context.update({        
            'subforms_dict':[
                {
                    'name':'generic_form_subtemplate.html',
                    'title':_(u'Upload new photo'),
                    'form':form,
                },
            ],        
        })
    else:
        #subform_dict is persistent between views, clear it explicitly
        extra_context.update({'subforms_dict':[]})
       
    return render_to_response('photos.html', extra_context,
        context_instance=RequestContext(request))    


def generic_photo_mark_main(request, object_id):
    photo = get_object_or_404(GenericPhoto, pk=object_id)

    if request.method == 'POST':
        photos = GenericPhoto.objects.photos_for_object(photo.content_object)
        photos.update(main=False)
        photo.main=True
        photo.save()

        messages.success(request, _(u'The main photo has been changed.'))
        return HttpResponseRedirect(request.POST.get('next', '/'))
        
    return render_to_response('generic_confirm.html', {
        'next':request.META.get('HTTP_REFERER','/'),
        'previous':request.META.get('HTTP_REFERER','/'),
        'object':photo.content_object,
    },  context_instance=RequestContext(request))   


def generic_photo_delete(request, object_id):
    photo = get_object_or_404(GenericPhoto, pk=object_id)
    if request.method == 'POST':
        main = photo.main
        photo.delete()
        if main:
            photos = GenericPhoto.objects.photos_for_object(photo.content_object)
            if photos.count() > 0:
                new_main_photo = photos[0]
                new_main_photo.main=True
                new_main_photo.save()
                
                messages.success(request, _(u'The main photo was deleted successfully.  The another photo has been selected as the main photo.'))
            else:
                messages.success(request, _(u'The main photo was deleted successfully.'))
        else:
            messages.success(request, _(u'The photo was deleted successfully.'))
        
        return HttpResponseRedirect(request.POST.get('next', '/'))

    return render_to_response('generic_confirm.html', {
        'next':request.META.get('HTTP_REFERER','/'),
        'previous':request.META.get('HTTP_REFERER','/'),
        'title':_(u'Are you sure you wish to delete this photo?'),
        'object':photo.content_object,
        'delete_view':True,        
    },  context_instance=RequestContext(request)) 
