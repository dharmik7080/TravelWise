from django import forms
from .models import Package

class PackageForm(forms.ModelForm):
    """
    ModelForm for creating and editing travel packages,
    styling widgets with Bootstrap 5 dynamically.
    """
    class Meta:
        model = Package
        fields = [
            'package_name', 'destination', 'duration', 'package_type',
            'price', 'description', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
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
