from django import forms
from .models import Destination

class DestinationForm(forms.ModelForm):
    """
    ModelForm class for creating and updating Destination database entries,
    applying Bootstrap 5 classes dynamically to all widgets upon instantiation.
    """
    class Meta:
        model = Destination
        fields = [
            'destination_name', 'city', 'state', 'region', 'category',
            'description', 'best_season', 'ideal_days', 'budget_level',
            'average_cost_per_day', 'family_friendly', 'couple_friendly',
            'solo_friendly', 'average_rating', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap 5 classes dynamically
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
