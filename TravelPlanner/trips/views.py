from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from .models import Trip
from .forms import TripForm, ItineraryDayFormSet
from services.weather_service import WeatherService


class TripsIndexView(LoginRequiredMixin, generic.ListView):
    """
    Protected view to display the logged-in user's planned trips with pagination.
    """
    model = Trip
    template_name = 'trips/index.html'
    context_object_name = 'trips'
    paginate_by = 8

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user).order_by('-created_at')


class TripCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """
    Secure view for authenticated users to plan a new trip.
    Pre-populates the destination selection if passed via query parameters.
    """
    model = Trip
    form_class = TripForm
    template_name = 'trips/trip_form.html'
    success_url = reverse_lazy('trips:index')

    def get_initial(self):
        initial = super().get_initial()
        dest_id = self.request.GET.get('destination')
        if dest_id:
            initial['destination'] = dest_id
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        trip = self.object
        days = (trip.end_date - trip.start_date).days + 1
        
        from .models import ItineraryTemplate, ItineraryDay
        templates = list(ItineraryTemplate.objects.filter(destination=trip.destination).order_by('day_number'))
        total_templates = len(templates)
        
        for day_idx in range(1, days + 1):
            morning = "Explore local spots and landmarks"
            afternoon = "Enjoy local cuisine and markets"
            evening = "Relax and experience the nightlife"
            
            if total_templates > 0:
                template = next((t for t in templates if t.day_number == day_idx), None)
                if not template:
                    template = templates[(day_idx - 1) % total_templates]
                morning = template.morning
                afternoon = template.afternoon
                evening = template.evening
                
            ItineraryDay.objects.create(
                trip=trip,
                day_number=day_idx,
                morning=morning,
                afternoon=afternoon,
                evening=evening
            )
            
        return response

    def get_success_message(self, cleaned_data):
        return f"Your trip to {self.object.destination.destination_name} has been planned successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class TripDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Protected view to display details of a specific trip planned by the logged-in user.
    """
    model = Trip
    template_name = 'trips/trip_detail.html'
    context_object_name = 'trip'

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_weather'] = WeatherService.get_weather(self.object.destination.city)
        return context


class TripUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """
    Secure view to update properties of a trip planned by the logged-in user.
    """
    model = Trip
    form_class = TripForm
    template_name = 'trips/trip_form.html'
    success_url = reverse_lazy('trips:index')

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)

    def get_success_message(self, cleaned_data):
        return f"Your trip to {self.object.destination.destination_name} has been updated successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class TripDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Secure view to delete a trip planned by the logged-in user.
    """
    model = Trip
    template_name = 'trips/trip_confirm_delete.html'
    success_url = reverse_lazy('trips:index')

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        trip = self.get_object()
        messages.success(self.request, f"Your trip to {trip.destination.destination_name} has been deleted successfully.")
        return super().delete(request, *args, **kwargs)


class TripItineraryUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Secure view for authenticated trip owners to edit their trip itineraries.
    """
    model = Trip
    template_name = 'trips/itinerary_form.html'
    fields = []  # We don't edit Trip fields here

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ItineraryDayFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = ItineraryDayFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            formset.save()
            messages.success(self.request, "Your trip itinerary has been updated successfully!")
            return redirect('trips:detail', pk=self.object.pk)
        else:
            return self.form_invalid(form)
