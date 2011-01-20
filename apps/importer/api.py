import os
import csv

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode

def perform_import(csvfilename, model, mappings, remove_top=None, dryrun=True):
    csvfile = open(csvfilename, 'rb')
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    
    try:
        csvfile = file(csvfilename, 'r')
    except IOError:
        self.error(_(u'Could not open specified csv file, %s, or it does not exist') % datafile, 0)
    else:
        # CSV Reader returns an iterable, but as we possibly need to
        # perform list commands and since list is an acceptable iterable, 
        # we'll just transform it.
        csvfile = list(csv.reader(csvfile, dialect=dialect))

    if remove_top:
        self.csvfile.pop(0)


    #model_fields = dict([(f.name,f) for f in self.model._meta.fields])
    model_fields = model._meta.init_name_map()
    imported_lines = 0
    errors = 0
    results = []
    line = 1
    for column in csvfile:
        column = [smart_unicode(c) for c in column]
        model_line = {}
        line_error = False
        for field_exp in mappings:
            if field_exp['enabled']:
                try:
                    field = model_fields[field_exp['model_field']][0]

                    expression = eval(field_exp['expression'], {'csv_column':column})
                    if hasattr(field, 'related'):
                        arguments = {field_exp['arguments']:expression}
                        value = field.related.parent_model.objects.get(**arguments)
                    else:
                        value = expression

                    model_line[field_exp['model_field']] = value

                except Exception, err:
                    value = None
                    line_error = True
                    errors += 1
                    results.append(_(u'Foreign key fetch error, line: %s, expression: %s, error: %s') % (line, expression, err))
        try:
            if not line_error:
                if dryrun:
                    entry = model(**model_line)
                else:
                    entry = model.objects.create(**model_line)

                imported_lines += 1
        except Exception, err:
            errors += 1
            results.append(_(u'Import error, line: %s, error: %s') % (line, err))
        
        line += 1
    
    results.append(_(u'Imported %s lines') % imported_lines)
    results.append(_(u'There were %s errors') % errors)
    
    return results
