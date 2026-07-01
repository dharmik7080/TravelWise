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


from django.http import JsonResponse
from django.views import View
from datetime import datetime
from destinations.models import Destination
from ml.prediction_service import PredictionService

class TripCostEstimateView(LoginRequiredMixin, View):
    """
    AJAX view to predict/estimate total trip cost based on form inputs.
    """
    def post(self, request, *args, **kwargs):
        destination_id = request.POST.get('destination_id')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        travelers_str = request.POST.get('number_of_travelers', '1')
        package_type = request.POST.get('package_type', 'Standard')

        if not (destination_id and start_date_str and end_date_str):
            return JsonResponse({'error': 'Please select Destination, Start Date, and End Date.'}, status=400)

        try:
            destination = Destination.objects.get(pk=destination_id)
        except Destination.DoesNotExist:
            return JsonResponse({'error': 'Selected destination does not exist.'}, status=400)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            if start_date > end_date:
                return JsonResponse({'error': 'End date must be after or equal to start date.'}, status=400)
            
            days = (end_date - start_date).days + 1
        except ValueError:
            return JsonResponse({'error': 'Invalid date values provided.'}, status=400)

        try:
            travelers = int(travelers_str)
            if travelers < 1:
                return JsonResponse({'error': 'Number of travelers must be at least 1.'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid number of travelers.'}, status=400)

        # Infer Season from start_date
        month = start_date.month
        if month in [12, 1, 2]:
            season = 'Winter'
        elif month in [3, 4, 5]:
            season = 'Summer'
        elif month in [6, 7, 8]:
            season = 'Monsoon'
        elif month in [9, 10, 11]:
            season = 'Autumn'
        else:
            season = 'Spring'

        # Get Prediction
        predicted_cost = PredictionService.predict_cost(
            destination=destination.destination_name,
            travelers=travelers,
            days=days,
            package_type=package_type,
            season=season
        )

        if predicted_cost is None:
            return JsonResponse({'error': 'Estimation model failed. Please try again later.'}, status=500)

        return JsonResponse({'estimated_cost': predicted_cost})
