import os

from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from inventory.models import Settings

from forms import PhotoForm

from models import GenericPhoto

def generic_photos(request, model, object_id, max_photos=5):
    model_instance = get_object_or_404(model, pk=object_id)
    photos = GenericPhoto.objects.photos_for_object(model_instance)

    if (photos.count() < max_photos):
        if request.method == 'POST':
            post_data = request.POST
            
            action = post_data.get('action','')
            photo_num = post_data.get('photo_num','')
            
            if action == 'make_main':
                photos.update(main=False)
                main_photo=GenericPhoto.objects.get(pk=photo_num)
                main_photo.main=True
                main_photo.save()

                messages.success(request, _(u'The main photo has been changed.'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

            if action == 'delete':
                try:
                    photo = GenericPhoto.objects.get(pk=photo_num)
                    if photo.main:
                        if photos.count() == 2:
                            photos.update(main=True)
                            messages.success(request, _(u'The photo was deleted successfully.  The remaining photo has been selected as the main photo.'))
                        else:
                            messages.success(request, _(u'The photo was deleted successfully.  You have deleted the main photo, make sure you mark another one as the main photo.'))
                    else:
                        messages.success(request, _(u'The photo was deleted successfully.'))

                    photo.delete()
                except:
                    pass

                return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

            form = PhotoForm(post_data, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                if instance.image.size > Settings.objects.get(pk=1).max_photo_size:
                    messages.error(request, _(u'The photo is too big.'))
                    os.unlink(instance.photo.path)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

    #				ext = os.path.splitext(os.path.split(instance.get_photo_filename()))
    #				if ext != '.png' and ext != '.jpg' and ext != '.gif':
    #					_flash_message(request, _(u'El solo fotos de tipo: PNG, JPG o GIF son permitidas.'), type='error')
    #					os.unlink(instance.get_photo_filename())
    #					return HttpResponseRedirect('/photos/' + str(ad.number))
                    
                if photos.count() == 0:
                    instance.main = True
                
                instance.object_id = object_id
                instance.content_type = ContentType.objects.get_for_model(model)                
                instance.save()
                
                messages.success(request, _(u'The photo was added.'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        else:
            form = PhotoForm()
    else:
        form = ''

    return render_to_response('photos.html', {
        'object_id':object_id,
        'model_instance':model_instance,
        'photos':photos,
        'form':form,
        'max_photos':max_photos,
    },
    context_instance=RequestContext(request))
    
