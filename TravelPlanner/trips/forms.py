from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    """
    ModelForm for registering a traveler's Trip, including date,
    traveler count, and budget validation checks.
    """
    package_type = forms.ChoiceField(
        choices=[],
        required=False,
        label="Package Type (for Cost Estimation)",
        initial='Standard',
    )

    class Meta:
        model = Trip
        fields = [
            'destination', 'start_date', 'end_date', 'number_of_travelers',
            'budget', 'travel_type', 'notes'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from packages.models import Package
        try:
            db_types = sorted(list(Package.objects.values_list('package_type', flat=True).distinct()))
            choices = [(t, t) for t in db_types if t]
        except Exception:
            choices = [('Budget', 'Budget'), ('Standard', 'Standard'), ('Luxury', 'Luxury')]
        
        self.fields['package_type'].choices = choices

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_number_of_travelers(self):
        travelers = self.cleaned_data.get('number_of_travelers')
        if travelers is not None and travelers < 1:
            raise forms.ValidationError("Number of travelers must be at least 1.")
        return travelers

    def clean_budget(self):
        budget = self.cleaned_data.get('budget')
        if budget is not None and budget <= 0:
            raise forms.ValidationError("Budget must be a positive number.")
        return budget

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                self.add_error('end_date', "End date must be after the start date.")
        return cleaned_data


from django.forms import inlineformset_factory
from .models import ItineraryDay

class ItineraryDayForm(forms.ModelForm):
    """
    ModelForm to edit details of a single day within a trip itinerary.
    """
    class Meta:
        model = ItineraryDay
        fields = ['morning', 'afternoon', 'evening']
        widgets = {
            'morning': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'afternoon': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'evening': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

# Define an inline formset to allow batch editing itinerary days for a specific trip
ItineraryDayFormSet = inlineformset_factory(
    Trip,
    ItineraryDay,
    form=ItineraryDayForm,
    extra=0,
    can_delete=False
)
