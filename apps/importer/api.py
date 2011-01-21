import csv

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode

def perform_import(csvfilename, model, mappings, dialect_settings=None, start_row=1, dryrun=True):
    csvfile = open(csvfilename, 'rb')
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    if dialect_settings:
        dialect.delimiter = str(dialect_settings['dialect_delimiter'])
        dialect.doublequote = dialect_settings['dialect_doublequote']
        dialect.escapechar = str(dialect_settings['dialect_escapechar'])
        dialect.quotechar = str(dialect_settings['dialect_quotechar'])
        dialect.skipinitialspace = dialect_settings['dialect_skipinitialspace']
        
    csvfile.seek(0)
    
    try:
        csvfd = file(csvfilename, 'r')
    except IOError:
        self.error(_(u'Could not open specified csv file, %s, or it does not exist') % datafile, 0)
    else:
        # CSV Reader returns an iterable, but as we possibly need to
        # perform list commands and since list is an acceptable iterable, 
        # we'll just transform it.
        csvfile = list(csv.reader(csvfd, dialect=dialect))

    model_fields = model._meta.init_name_map()
    imported_lines = 0
    errors = 0
    results = []
    for line, column in enumerate(csvfile[start_row-1:], start_row):
        column = [smart_unicode(c) for c in column]
        model_line = {}
        line_error = False
        for field_exp in mappings:
            if field_exp['enabled']:
                expression = None
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
                    results.append(_(u'Foreign key fetch error, line: %(line)s, expression: %(exp)s, error: %(err)s') % {'line':line, 'exp':expression, 'err':err})
        try:
            if not line_error:
                if dryrun:
                    entry = model(**model_line)
                else:
                    entry = model.objects.create(**model_line)

                imported_lines += 1
        except Exception, err:
            errors += 1
            results.append(_(u'Import error, line: %(line)s, error: %(err)s') % {'line':line, 'err':err})
        

    results.append(_(u'Processed %s lines.') % len(csvfile[start_row-1:]))
    results.append(_(u'Imported %s lines.') % imported_lines)
    results.append(_(u'There were %s errors.') % errors)
    
    csvfd.close()
    return results
