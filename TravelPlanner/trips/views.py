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

        itinerary_data = {}
        for day_row in trip.itinerary_days.all():
            day_attrs = []
            # Find the actual attraction objects matching the slots
            for slot_text in [day_row.morning, day_row.afternoon, day_row.evening]:
                if not slot_text:
                    continue
                for attr in dest.attractions.all():
                    if attr.attraction_name.lower() in slot_text.lower():
                        day_attrs.append(attr)
                        break

            from services.route_optimizer import RouteOptimizer
            optimized_attrs, transitions = RouteOptimizer.optimize_route(day_attrs)

            slots_data = {'morning': None, 'afternoon': None, 'evening': None}
            slot_keys = ['morning', 'afternoon', 'evening']

            for idx, attr in enumerate(optimized_attrs):
                if idx < len(slot_keys):
                    a_lat, a_lon = MapsDataService.get_attraction_coords(d_lat, d_lon, attr.attraction_name)
                    slots_data[slot_keys[idx]] = {
                        'name': attr.attraction_name,
                        'category': attr.category,
                        'lat': a_lat,
                        'lon': a_lon
                    }

            day_distance = sum(t['distance_km'] for t in transitions)
            day_travel_time_min = sum(t['travel_time_min'] for t in transitions)

            itinerary_data[str(day_row.day_number)] = {
                'morning': slots_data['morning'],
                'afternoon': slots_data['afternoon'],
                'evening': slots_data['evening'],
                'distance_km': round(day_distance, 1),
                'travel_time_min': day_travel_time_min,
                'transitions': transitions
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
            # Save the formset with commit=False so we can adjust day numbers
            instances = formset.save(commit=False)
            
            # Delete objects marked for deletion
            for obj in formset.deleted_objects:
                obj.delete()

            # Collect remaining/new instances in the order submitted
            ordered_instances = []
            for f in formset.forms:
                if f in formset.deleted_forms or (f.instance.pk is None and not f.has_changed()):
                    continue
                ordered_instances.append(f.instance)

            # Assign temporary large positive day numbers to prevent UNIQUE constraint errors
            # while satisfying SQLite PositiveIntegerField CHECK constraint
            for idx, instance in enumerate(ordered_instances, start=1):
                instance.day_number = 10000 + idx
                if instance.pk:
                    instance.save(update_fields=['day_number'])

            # Now save them with the correct final positive day numbers in sequence
            for idx, instance in enumerate(ordered_instances, start=1):
                instance.day_number = idx
                instance.trip = self.object
                instance.save()

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


class TripCalendarView(LoginRequiredMixin, generic.TemplateView):
    """
    Screen 10: Trip Calendar / Timeline view.
    Renders all user trips as FullCalendar.js events colour-coded by status.
    """
    template_name = 'trips/trip_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.utils import timezone
        import json
        today = timezone.localtime(timezone.now()).date()
        trips = Trip.objects.filter(user=self.request.user).select_related('destination')
        events = []
        for trip in trips:
            if today < trip.start_date:
                color = '#0d6efd'
                status = 'Upcoming'
            elif trip.start_date <= today <= trip.end_date:
                color = '#198754'
                status = 'Ongoing'
            else:
                color = '#6c757d'
                status = 'Completed'
            events.append({
                'id': trip.pk,
                'title': trip.trip_name or trip.destination.destination_name,
                'start': str(trip.start_date),
                'end': str(trip.end_date),
                'color': color,
                'url': f'/trips/{trip.pk}/',
                'extendedProps': {
                    'destination': trip.destination.destination_name,
                    'budget': str(trip.budget),
                    'travel_type': trip.travel_type,
                    'status': status,
                }
            })
        context['calendar_events_json'] = json.dumps(events)
        context['today'] = str(today)
        return context


class TripShareToggleView(LoginRequiredMixin, View):
    """
    Screen 11: AJAX endpoint to toggle a trip's is_public flag.
    Returns JSON with the new state and public share URL.
    """
    def post(self, request, pk, *args, **kwargs):
        from django.http import JsonResponse
        try:
            trip = Trip.objects.get(pk=pk, user=request.user)
        except Trip.DoesNotExist:
            return JsonResponse({'error': 'Trip not found.'}, status=404)
        trip.is_public = not trip.is_public
        trip.save(update_fields=['is_public'])
        share_url = request.build_absolute_uri(f'/trips/shared/{trip.share_token}/')
        return JsonResponse({
            'is_public': trip.is_public,
            'share_url': share_url if trip.is_public else '',
        })


class TripPublicView(generic.DetailView):
    """
    Screen 11: Read-only public itinerary view — no authentication required.
    Accessed via /trips/shared/<share_token>/
    """
    template_name = 'trips/trip_public.html'
    context_object_name = 'trip'

    def get_object(self, queryset=None):
        from django.shortcuts import get_object_or_404
        token = self.kwargs['share_token']
        return get_object_or_404(Trip, share_token=token, is_public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = self.object
        context['share_url'] = self.request.build_absolute_uri(
            f'/trips/shared/{trip.share_token}/'
        )
        context['can_copy'] = self.request.user.is_authenticated
        return context


class TripCopyView(LoginRequiredMixin, View):
    """
    Screen 11: Copies a public trip to the logged-in user's account,
    duplicating itinerary days as well.
    """
    def post(self, request, share_token, *args, **kwargs):
        from django.shortcuts import get_object_or_404
        from .models import ItineraryDay
        source = get_object_or_404(Trip, share_token=share_token, is_public=True)
        new_trip = Trip.objects.create(
            user=request.user,
            destination=source.destination,
            start_date=source.start_date,
            end_date=source.end_date,
            number_of_travelers=source.number_of_travelers,
            budget=source.budget,
            travel_type=source.travel_type,
            notes=source.notes,
            trip_name=(
                f'Copy of {source.trip_name}'
                if source.trip_name
                else f'Copy of trip to {source.destination.destination_name}'
            ),
            description=source.description,
        )
        for day in source.itinerary_days.all():
            ItineraryDay.objects.create(
                trip=new_trip,
                day_number=day.day_number,
                morning=day.morning,
                afternoon=day.afternoon,
                evening=day.evening,
            )
        messages.success(request, 'Trip copied to your account successfully!')
        return redirect('trips:detail', pk=new_trip.pk)


class TripBudgetView(LoginRequiredMixin, generic.DetailView):
    """
    Screen 9: Dedicated Trip Budget and Cost Breakdown page.
    Shows pie and bar charts plus category rows and overbudget alerts.
    """
    model = Trip
    template_name = 'trips/trip_budget.html'
    context_object_name = 'trip'

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user).select_related('destination')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        import json
        trip = self.object
        days = (trip.end_date - trip.start_date).days + 1
        month = trip.start_date.month
        if month in [12, 1, 2]:
            season = 'Winter'
        elif month in [3, 4, 5]:
            season = 'Summer'
        elif month in [6, 7, 8]:
            season = 'Monsoon'
        else:
            season = 'Autumn'
        from services.ml.budget_predictor import BudgetPredictor
        breakdown = BudgetPredictor.calculate_breakdown(
            destination=trip.destination.destination_name,
            travelers=trip.number_of_travelers,
            days=days,
            package_type='Standard',
            season=season
        )
        total_estimated = sum(breakdown.values()) if breakdown else 0
        context['breakdown'] = breakdown
        context['total_estimated'] = total_estimated
        context['days'] = days
        context['daily_avg'] = round(total_estimated / days, 2) if days > 0 else 0
        context['is_overbudget'] = (
            total_estimated > float(trip.budget) if trip.budget else False
        )
        context['overbudget_by'] = (
            round(total_estimated - float(trip.budget), 2)
            if context['is_overbudget'] else 0
        )
        context['breakdown_json'] = json.dumps(breakdown)
        return context
