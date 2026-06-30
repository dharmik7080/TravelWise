from django import forms
from .models import Attraction

class AttractionForm(forms.ModelForm):
    """
    ModelForm for creating and editing Attraction records,
    using HTML5 time pickers and styling fields with Bootstrap 5.
    """
    class Meta:
        model = Attraction
        fields = [
            'attraction_name', 'destination', 'category', 'description',
            'entry_fee', 'opening_time', 'closing_time', 'average_visit_time', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
