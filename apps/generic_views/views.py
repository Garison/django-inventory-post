import urllib

from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.create_update import create_object, update_object, delete_object

from forms import FilterForm, GenericConfirmForm, GenericAssignRemoveForm

def add_filter(request, list_filter):
    result={}
    if(len(request.GET)>0):
        filter_form=FilterForm(list_filter, request.GET)
        if filter_form.is_valid():
            filterdict = filter_form.cleaned_data
            q_objs = [Q(**{list_filter[k]['destination']: filterdict[k]}) for k in list_filter.keys() if filterdict.get(k, None)]
            result['filter']=q_objs
            result['filterdict'] = filterdict
            
            id_dict={}
            for key in filterdict.keys():
                if hasattr(filterdict[key], 'id'):
                    id_dict[key] = filterdict[key].id
    else:			
        filter_form = FilterForm(list_filter)
            
    result['filter_form'] = filter_form
    return result

def generic_list(request, list_filter=None, queryset_filter=None, *args, **kwargs):
    if list_filter:
        result = add_filter(request, list_filter)
        if 'filter' in result:
            kwargs['queryset'] = kwargs['queryset'].filter(*result['filter'])

            id_dict={}
            for key in result['filterdict'].keys():
                if hasattr(result['filterdict'][key], 'id'):
                    id_dict[key] = result['filterdict'][key].id

            raw_url = urllib.urlencode(id_dict)
            
            if len(raw_url):
                kwargs['extra_context']['new_url'] = '&' + raw_url

        kwargs['extra_context']['filter_form'] = result['filter_form']

    if queryset_filter:
#		locals()[val+'_str']= x
        exec("kwargs['queryset'] = kwargs['queryset'].filter(" + queryset_filter['field'] + "=kwargs['" +queryset_filter['source'] +"'])")
        if queryset_filter['source'] in kwargs:
            kwargs.pop(queryset_filter['source'])
        
    results_per_page = 20
    kwargs['extra_context']['range_base'] = (int(request.GET.get('page', 1))-1) * results_per_page
    return object_list(request, paginate_by=results_per_page, template_name = 'generic_list.html', *args, **kwargs)

def generic_create(*args, **kwargs):
    if 'model' in kwargs:
        try:
            if 'extra_context' in kwargs:
                kwargs['extra_context']['title'] = kwargs['model']._meta.verbose_name
            else:
                kwargs['extra_context']= { 'title': kwargs['model']._meta.verbose_name }
        except:
            pass
    
    return create_object(template_name='generic_form.html', *args, **kwargs)

def generic_update(*args, **kwargs):
    if 'model' in kwargs:
        try:
            if 'extra_context' in kwargs:
                kwargs['extra_context']['title'] = kwargs['model']._meta.verbose_name
            else:
                kwargs['extra_context']= { 'title': kwargs['model']._meta.verbose_name }
        except:
            pass
                
    return update_object(template_name='generic_form.html', *args, **kwargs)

def generic_delete(*args, **kwargs):
    try:
        kwargs['post_delete_redirect'] = reverse(kwargs['post_delete_redirect'])
    except NoReverseMatch:
        pass

    kwargs['extra_context']['delete_view'] = True
  
    return delete_object(template_name='generic_confirm.html', *args, **kwargs)

def generic_confirm(request, _view, _title=None, _model=None, _object_id=None, _message='', *args, **kwargs):
    if request.method == 'POST':
        form = GenericConfirmForm(request.POST)
        if form.is_valid():
            if hasattr(_view, '__call__'):
                return _view(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse(_view, args=args, kwargs=kwargs))

    data = {}
    
    try:
        object = _model.objects.get(pk=kwargs[_object_id])
        data['object'] = object
    except:
        pass
    
    try:
        data['title'] = _title
    except:
        pass

    try:
        data['message'] = _message
    except:
        pass

    form=GenericConfirmForm()
        
    return render_to_response('generic_confirm.html',
        data,
        context_instance=RequestContext(request))	

def generic_assign_remove(request, title, obj, left_list_qryset, left_list_title, right_list_qryset, right_list_title, add_method, remove_method, item_name, list_filter=None):
    left_filter = None
    filter_form = None
    if list_filter:
        result = add_filter(request, list_filter)
        if 'filter' in result:
            left_filter = result['filter']

#	filter_form = None
#	if list_filter:
        filter_form = result['filter_form']
  
    if request.method == 'POST':
        post_data = request.POST
        form = GenericAssignRemoveForm(left_list_qryset, right_list_qryset, left_filter, request.POST)
        if form.is_valid():
            action = post_data.get('action','')
            if action == "assign":
                for item in form.cleaned_data['left_list']:
                    add_method(item)
                if form.cleaned_data['left_list']:
                    messages.success(request, _(u"The %s were added.") % unicode(item_name))

            if action == "remove":
                for item in form.cleaned_data['right_list']:
                    remove_method(item)
                if form.cleaned_data['right_list']:
                    messages.success(request, _(u"The %s were removed.") % unicode(item_name))

    form = GenericAssignRemoveForm(left_list_qryset=left_list_qryset, right_list_qryset=right_list_qryset, left_filter=left_filter)
        
    return render_to_response('generic_assign_remove.html', {
    'form':form,
    'object':obj,
    'title':title,
    'left_list_title':left_list_title,
    'right_list_title':right_list_title,
    'filter_form':filter_form,
    },
    context_instance=RequestContext(request))


def generic_detail(request, object_id, form_class, model, title=None, create_view=None, record_links=None, extra_context=None):
    instance = get_object_or_404(model, pk=object_id)
    form = form_class(instance = instance)
    
    return render_to_response('generic_detail.html', {
        'title':title,
        'form':form,
        'object':instance,
        'create_view':create_view,
        'record_links':record_links,
    },
    context_instance=RequestContext(request))
