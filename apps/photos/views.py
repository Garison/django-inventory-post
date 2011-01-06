import os

from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from inventory.models import Settings

from forms import PhotoForm


def generic_photos(request, model, object_id, max_photos = 5):
    model_instance = model.objects.get(pk=object_id)
    photos = model_instance.photos.all()

    if (photos.count() < max_photos):
        if request.method == 'POST':
            post_data = request.POST
            
            action = post_data.get('action','')
            photo_num = post_data.get('photo_num','')
            
            if action == 'make_main':
                photos.update(main=False)
                main_photo=Photo.objects.get(pk=photo_num)
                main_photo.main=True
                main_photo.save()

                _flash_(request, _(u'The main photo has been changed.'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

            if action == 'delete':
                try:
                    photo = Photo.objects.get(pk=photo_num)
                    if photo.main:
                        if photos.count() == 2:
                            photos.update(main=True)
                            _flash_message(request, _(u'The photo was deleted successfully.  The remaining photo has been selected as the main photo.'))
                        else:
                            _flash_message(request, _(u'The photo was deleted successfully.  You have deleted the main photo, make sure you mark another one as the main photo.'))
                    else:
                        _flash_message(request, _(u'The photo was deleted successfully.'))

                    photo.delete()
                except:
                    pass

                return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

            form = PhotoForm(post_data, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                if instance.photo.size > Settings.objects.get(pk=1).max_photo_size:
                    _flash_message(request, _(u'The photo is too big.'), type='error')
                    os.unlink(instance.photo.path)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

    #				ext = os.path.splitext(os.path.split(instance.get_photo_filename()))
    #				if ext != '.png' and ext != '.jpg' and ext != '.gif':
    #					_flash_message(request, _(u'El solo fotos de tipo: PNG, JPG o GIF son permitidas.'), type='error')
    #					os.unlink(instance.get_photo_filename())
    #					return HttpResponseRedirect('/photos/' + str(ad.number))
                    
                if photos.count() == 0:
                    instance.main = True
                
                new_instance = instance.create(instance=instance)
                model_instance.photos.add(instance)
                model_instance.save()
                _flash_message(request, _(u'The photo was added.'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        else:
            form = PhotoForm()
    else:
        form = ''

    return render_to_response('photos.html', {
        'object_id': object_id,
        'model_instance': model_instance,
        'photos': photos,
        'form': form,
        'max_photos': max_photos,
        },
    context_instance=RequestContext(request))
    
