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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.utils import timezone
        import sys
        today = timezone.localtime(timezone.now()).date()
        
        for trip in context['trips']:
            start = trip.start_date
            end = trip.end_date
            
            if today < start:
                trip.dynamic_status = "upcoming"
                trip.dynamic_status_label = "Upcoming"
                trip.dynamic_status_badge = "bg-primary"
                days = (start - today).days
                trip.dynamic_days_label = f"Starts in {days} days"
                trip.test_legacy_days_left = f"{days} Days Left"
            elif start <= today <= end:
                trip.dynamic_status = "ongoing"
                trip.dynamic_status_label = "Ongoing"
                trip.dynamic_status_badge = "bg-success"
                
                day_number = (today - start).days + 1
                total_days = (end - start).days + 1
                
                if today == start:
                    trip.dynamic_days_label = "Starts Today"
                elif today == end:
                    trip.dynamic_days_label = "Final Day"
                else:
                    trip.dynamic_days_label = f"Day {day_number} of {total_days}"
                trip.test_legacy_days_left = "0 Days Left"
            else:
                trip.dynamic_status = "completed"
                trip.dynamic_status_label = "Completed"
                trip.dynamic_status_badge = "bg-secondary"
                trip.dynamic_days_label = "Completed ✓"
                trip.test_legacy_days_left = "0 Days Left"
                
        return context


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
        import json
        
        # Check if custom generated itinerary JSON is passed from the client-side
        generated_itinerary_str = self.request.POST.get('generated_itinerary')
        if generated_itinerary_str:
            try:
                gen_itinerary = json.loads(generated_itinerary_str)
                for day_str, slots in gen_itinerary.items():
                    day_idx = int(day_str)
                    ItineraryDay.objects.create(
                        trip=trip,
                        day_number=day_idx,
                        morning=slots.get('morning') or f"Explore scenic spots in {trip.destination.destination_name}",
                        afternoon=slots.get('afternoon') or "Visit local markets and enjoy regional cuisine",
                        evening=slots.get('evening') or f"Relax and enjoy evening views in {trip.destination.destination_name}"
                    )
                return response
            except Exception:
                pass

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
        
        from django.utils import timezone
        today = timezone.localtime(timezone.now()).date()
        trip = self.object
        start = trip.start_date
        end = trip.end_date
        
        if today < start:
            trip.dynamic_status = "upcoming"
            trip.dynamic_status_label = "Upcoming"
            trip.dynamic_status_badge = "bg-primary"
            days = (start - today).days
            trip.dynamic_days_label = f"Starts in {days} days"
            trip.test_legacy_days_left = f"{days} Days Left"
        elif start <= today <= end:
            trip.dynamic_status = "ongoing"
            trip.dynamic_status_label = "Ongoing"
            trip.dynamic_status_badge = "bg-success"
            
            day_number = (today - start).days + 1
            total_days = (end - start).days + 1
            
            if today == start:
                trip.dynamic_days_label = "Starts Today"
            elif today == end:
                trip.dynamic_days_label = "Final Day"
            else:
                trip.dynamic_days_label = f"Day {day_number} of {total_days}"
            trip.test_legacy_days_left = "0 Days Left"
        else:
            trip.dynamic_status = "completed"
            trip.dynamic_status_label = "Completed"
            trip.dynamic_status_badge = "bg-secondary"
            trip.dynamic_days_label = "Completed ✓"
            trip.test_legacy_days_left = "0 Days Left"

        # Maps Integration (Phase 3)
        from services.maps_data_service import MapsDataService
        import json

        dest = trip.destination
        d_lat, d_lon = MapsDataService.get_destination_coords(dest)

        def get_slot_data(slot_text):
            if not slot_text:
                return None
            target_attr = None
            for attr in dest.attractions.all():
                if attr.attraction_name.lower() in slot_text.lower():
                    target_attr = attr
                    break
            
            if target_attr:
                a_lat, a_lon = MapsDataService.get_attraction_coords(d_lat, d_lon, target_attr.attraction_name)
                return {
                    'name': target_attr.attraction_name,
                    'category': target_attr.category,
                    'lat': a_lat,
                    'lon': a_lon
                }
            return None

        itinerary_data = {}
        for day_row in trip.itinerary_days.all():
            itinerary_data[str(day_row.day_number)] = {
                'morning': get_slot_data(day_row.morning),
                'afternoon': get_slot_data(day_row.afternoon),
                'evening': get_slot_data(day_row.evening)
            }

        context['itinerary_map_payload'] = json.dumps({
            'destination': {
                'name': dest.destination_name,
                'lat': d_lat,
                'lon': d_lon
            },
            'itinerary': itinerary_data
        })
            
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

        # Retrieve attractions for destination
        attractions_qs = destination.attractions.all()
        attractions_list = [{
            'name': attr.attraction_name,
            'category': attr.category,
            'image_url': attr.image.url if attr.image else None
        } for attr in attractions_qs[:4]]

        # Recommend activities based on category
        activities = []
        cat_lower = destination.category.lower()
        if 'hill' in cat_lower or 'mountain' in cat_lower or 'adventure' in cat_lower:
            activities = ['Trekking & Hiking', 'Cable Car Rides', 'Scenic Photography', 'Local Sightseeing']
        elif 'beach' in cat_lower or 'lake' in cat_lower or 'water' in cat_lower:
            activities = ['Boating & Water Sports', 'Sunset Cruises', 'Beach Volleyball', 'Seafood Tasting']
        elif 'heritage' in cat_lower or 'temple' in cat_lower or 'spiritual' in cat_lower:
            activities = ['Guided Heritage Walks', 'Spiritual Prayers', 'Archaeological Sightseeing', 'Cultural Shows']
        else:
            activities = ['Local Shopping', 'Food Tasting Walks', 'Photography Tours', 'City Exploration']

        from services.ml.budget_predictor import BudgetPredictor
        breakdown = BudgetPredictor.calculate_breakdown(
            destination=destination.destination_name,
            travelers=travelers,
            days=days,
            package_type=package_type,
            season=season
        )

        return JsonResponse({
            'estimated_cost': predicted_cost,
            'breakdown': breakdown,
            'attractions': attractions_list,
            'recommended_activities': activities,
            'package_type': package_type
        })


class TripItineraryGenerateView(LoginRequiredMixin, View):
    """
    Thin AJAX endpoint to generate a customized day-wise itinerary based on travel parameters
    entirely using existing database records.
    """
    def post(self, request, *args, **kwargs):
        destination_id = request.POST.get('destination_id')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        travel_type = request.POST.get('travel_type', 'Solo')
        budget_level = request.POST.get('budget_level', 'Moderate')
        regenerate = request.POST.get('regenerate') == 'true'

        if not all([destination_id, start_date_str, end_date_str]):
            return JsonResponse({'error': 'Please select Destination, Start Date, and End Date.'}, status=400)

        try:
            destination = Destination.objects.get(pk=destination_id)
        except Destination.DoesNotExist:
            return JsonResponse({'error': 'Selected destination does not exist.'}, status=400)

        # Parse duration (total days)
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            total_days = (end_date - start_date).days + 1
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid date format.'}, status=400)

        if total_days <= 0:
            return JsonResponse({'error': 'End date must be after or equal to start date.'}, status=400)

        from services.itinerary_service import ItineraryService
        # Generate using service
        itinerary = ItineraryService.generate_itinerary(
            destination=destination,
            total_days=total_days,
            travel_type=travel_type,
            budget_level=budget_level,
            regenerate=regenerate
        )

        return JsonResponse({'itinerary': itinerary})
