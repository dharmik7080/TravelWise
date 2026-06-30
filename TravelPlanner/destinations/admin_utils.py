import csv
from django.http import StreamingHttpResponse

class Echo:
    """
    An object that implements just the write method of the file-like interface.
    """
    def write(self, value):
        return value

def export_queryset_to_csv(queryset, fields, filename):
    """
    Generates a StreamingHttpResponse containing the CSV serialization of the queryset.
    Supports nested field lookups via double underscores (__).
    """
    echo = Echo()
    writer = csv.writer(echo)
    
    def rows():
        # Header
        yield writer.writerow(fields)
        # Rows
        for obj in queryset.iterator():
            row = []
            for field in fields:
                if '__' in field:
                    parts = field.split('__')
                    val = obj
                    for part in parts:
                        if val is not None:
                            val = getattr(val, part, None)
                else:
                    val = getattr(obj, field, None)
                
                if callable(val):
                    row.append(val())
                else:
                    row.append(str(val) if val is not None else '')
            yield writer.writerow(row)

    response = StreamingHttpResponse(rows(), content_type="text/csv")
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
