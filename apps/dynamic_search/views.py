import re

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.db.models import Q

from api import search_list
from forms import SearchForm


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(terms, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    #terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search(request):
    query_string = ''
    found_entries = {}
    form = SearchForm()

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        terms = normalize_query(query_string)
        
        for model, data in search_list.items():
            #print model, fields
            query = get_query(terms, data['fields'])            

#            for entry in model.objects.filter(query):
            results = model.objects.filter(query)
            if results:
                found_entries[data['text']] = results
        #found_entries = Entry.objects.filter(entry_query).order_by('-pub_date')

    return render_to_response('search_results.html', {
                            'query_string':query_string, 
                            'found_entries':found_entries,
                            'form':form },
                          context_instance=RequestContext(request))
"""                          
                              
    keyword = ''
    results = {}
    form = SearchForm()
    
    if request.method == 'GET':
        keyword=request.GET.get('keyword','')
        form = SearchForm(initial={'keyword':keyword})        
        if keyword:
            for model, fields in search_list.items():
                model_searches = Q(
            results = []
#            people = Person.objects.filter(
#                Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(second_name__icontains=keyword) | Q(second_last_name__icontains=keyword ) | Q(location__name__icontains=keyword)
#                )		

#            items = Item.objects.filter(
#                Q(property_number__icontains=keyword) | Q(notes__icontains=keyword) | Q(serial_number__icontains=keyword) | Q(location__name__icontains=keyword) | Q(item_template__description__icontains=keyword)
#                )		

#            templates = ItemTemplate.objects.filter(
#                Q(description__icontains=keyword) | Q(brand__icontains=keyword) | Q(model__icontains=keyword) | Q(part_number__icontains=keyword) | Q(notes__icontains=keyword)
#                )		

#            groups = ItemGroup.objects.filter(
#                Q(name__icontains=keyword)
#                )	
         

    return render_to_response('search_results.html', {
        'form':form,
        'results':results,
        'keyword':keyword,
        },
    context_instance=RequestContext(request))


def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['title', 'body',])
        
        found_entries = Entry.objects.filter(entry_query).order_by('-pub_date')

    return render_to_response('search/search_results.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))
"""
