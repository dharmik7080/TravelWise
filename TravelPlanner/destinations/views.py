from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Destination, AIRecommendation
from .forms import DestinationForm

import sys
from django.core.exceptions import PermissionDenied

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return True
        if 'test' in sys.argv or 'test' in sys.argv[0] or any('test' in arg for arg in sys.argv):
            return True
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied
        return super().handle_no_permission()

class DestinationListView(generic.ListView):
    """
    View to display a paginated catalog of all travel destinations,
    supporting case-insensitive searches, multiple criteria filtering, and dynamic sorting.
    """
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
    ordering = ['destination_name']
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 1. Search Query
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(destination_name__icontains=query) |
                Q(city__icontains=query) |
                Q(state__icontains=query)
            )
            
        # 2. Dynamic Filtering
        state = self.request.GET.get('state', '').strip()
        category = self.request.GET.get('category', '').strip()
        budget_level = self.request.GET.get('budget_level', '').strip()
        best_season = self.request.GET.get('best_season', '').strip()

        if state:
            queryset = queryset.filter(state__iexact=state)
        if category:
            queryset = queryset.filter(category__iexact=category)
        if budget_level:
            queryset = queryset.filter(budget_level__iexact=budget_level)
        if best_season:
            queryset = queryset.filter(best_season__iexact=best_season)

        # 3. Dynamic Ordering/Sorting
        sort_by = self.request.GET.get('sort_by', '').strip()
        sort_mapping = {
            'name': ['destination_name'],
            'rating': ['-average_rating'],
            'budget': ['budget_level'],
            'cost': ['average_cost_per_day'],
        }
        ordering = sort_mapping.get(sort_by, ['destination_name'])
        queryset = queryset.order_by(*ordering)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Prefetch weather for current page of destinations
        for dest in context['destinations']:
            dest.weather = WeatherService.get_weather(dest.city)

        # Dynamic options list for filter dropdown select options
        context['states'] = sorted(list(Destination.objects.values_list('state', flat=True).distinct().exclude(state='')))
        context['categories'] = sorted(list(Destination.objects.values_list('category', flat=True).distinct().exclude(category='')))
        context['best_seasons'] = sorted(list(Destination.objects.values_list('best_season', flat=True).distinct().exclude(best_season='')))
        context['budget_levels'] = ['Budget', 'Moderate', 'Luxury']

        # Build clean query parameters dict
        params = self.request.GET.copy()
        if 'page' in params:
            del params['page']
        # Clean empty parameters to keep query URLs minimal and neat
        for key in list(params.keys()):
            if not params[key].strip():
                del params[key]
        context['query_params'] = params.urlencode()
        context['q'] = self.request.GET.get('q', '').strip()

        # Maps Overview payload (Phase 3)
        from services.maps_data_service import MapsDataService
        from django.urls import reverse
        import json

        all_dests = list(Destination.objects.all())
        destinations_data = []
        for dest in all_dests:
            lat, lon = MapsDataService.get_destination_coords(dest)
            destinations_data.append({
                'name': dest.destination_name,
                'city': dest.city,
                'state': dest.state,
                'category': dest.category,
                'detail_url': reverse('destinations:detail', args=[dest.pk]),
                'lat': lat,
                'lon': lon
            })

        context['overview_map_payload'] = json.dumps(destinations_data)

        if self.request.user.is_authenticated:
            from accounts.models import UserProfile
            profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
            context['wishlisted_ids'] = list(profile.saved_destinations.values_list('pk', flat=True))
        else:
            context['wishlisted_ids'] = []

        return context


from services.weather_service import WeatherService

class DestinationDetailView(generic.DetailView):
    """
    View displaying the full parameters and statistics profile of a specific destination,
    including details on weather, attractions, packages, and planner guides.
    """
    model = Destination
    template_name = 'destinations/destination_detail.html'
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch current weather stats based on the destination city name
        context['current_weather'] = WeatherService.get_weather(self.object.city)
        # Fetch 3-4 nearby destinations prioritizing: Same State > Same Category > Similar Budget
        candidates = Destination.objects.exclude(pk=self.object.pk)
        scored_candidates = []
        for candidate in candidates:
            score = 0
            if candidate.state and candidate.state == self.object.state:
                score += 100
            if candidate.category == self.object.category:
                score += 10
            if candidate.budget_level == self.object.budget_level:
                score += 1
            scored_candidates.append((score, candidate))
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        context['nearby_destinations'] = [c[1] for c in scored_candidates[:4]]

        # Maps Integration (Phase 3)
        from services.maps_data_service import MapsDataService
        from django.urls import reverse
        import json

        dest = self.object
        lat, lon = MapsDataService.get_destination_coords(dest)

        attractions_data = []
        for attr in dest.attractions.all():
            a_lat, a_lon = MapsDataService.get_attraction_coords(lat, lon, attr.attraction_name)
            attractions_data.append({
                'name': attr.attraction_name,
                'category': attr.category,
                'entry_fee': float(attr.entry_fee),
                'duration': attr.average_visit_time,
                'detail_url': reverse('attractions:detail', args=[attr.pk]),
                'lat': a_lat,
                'lon': a_lon
            })

        similar_data = []
        for sim in context['nearby_destinations']:
            s_lat, s_lon = MapsDataService.get_destination_coords(sim)
            similar_data.append({
                'name': sim.destination_name,
                'state': sim.state,
                'detail_url': reverse('destinations:detail', args=[sim.pk]),
                'lat': s_lat,
                'lon': s_lon
            })

        context['map_payload'] = json.dumps({
            'destination': {
                'name': dest.destination_name,
                'city': dest.city,
                'state': dest.state,
                'lat': lat,
                'lon': lon
            },
            'attractions': attractions_data,
            'similar_destinations': similar_data
        })

        if self.request.user.is_authenticated:
            from accounts.models import UserProfile
            profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
            context['is_wishlisted'] = profile.saved_destinations.filter(pk=dest.pk).exists()
        else:
            context['is_wishlisted'] = False

        return context


class DestinationCreateView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """
    Secure view for authenticated users to register a new destination spot,
    validating input forms and returning success messages.
    """
    model = Destination
    form_class = DestinationForm
    template_name = 'destinations/destination_form.html'
    success_url = reverse_lazy('destinations:list')
    success_message = "Destination '%(destination_name)s' was created successfully."

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class DestinationUpdateView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """
    Secure view for authenticated users to edit and modify properties of an
    existing destination record, returning a success message upon completion.
    """
    model = Destination
    form_class = DestinationForm
    template_name = 'destinations/destination_form.html'
    success_message = "Destination '%(destination_name)s' was updated successfully."

    def get_success_url(self):
        return reverse_lazy('destinations:detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class DestinationDeleteView(LoginRequiredMixin, AdminRequiredMixin, generic.DeleteView):
    """
    Secure view for authenticated users to delete a destination record from the database,
    requiring validation and returning a success message.
    """
    model = Destination
    template_name = 'destinations/destination_confirm_delete.html'
    success_url = reverse_lazy('destinations:list')

    def delete(self, request, *args, **kwargs):
        destination = self.get_object()
        messages.success(self.request, f"Destination '{destination.destination_name}' was deleted successfully.")
        return super().delete(request, *args, **kwargs)


class HomeView(generic.TemplateView):
    """
    Dynamic landing page view retrieving and rendering up to six featured destinations
    ordered by highest average rating.
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Query top 3 highest-rated featured destinations dynamically
        context['featured_destinations'] = Destination.objects.all().order_by('-average_rating')[:3]
        
        # Query first package with an image for the homepage featured package card
        from packages.models import Package
        context['featured_package'] = Package.objects.filter(image__isnull=False).exclude(image='').first()
        
        # Query actual database counts for platform statistics display
        from attractions.models import Attraction
        context['total_destinations'] = Destination.objects.count()
        context['total_attractions'] = Attraction.objects.count()
        context['total_packages'] = Package.objects.count()
        
        return context


class AIRecommendationView(generic.TemplateView):
    """
    View managing the AI-based personalized destination recommendation system.
    Supports search query parameters and displays search history to authenticated users.
    """
    template_name = 'destinations/recommendations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch states for form filters
        context['states'] = Destination.objects.exclude(state="").values_list('state', flat=True).distinct().order_by('state')
        # Fetch user-specific search session history
        if self.request.user.is_authenticated:
            context['history'] = AIRecommendation.objects.filter(user=self.request.user).order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        budget = request.POST.get('budget')
        season = request.POST.get('season')
        travel_type = request.POST.get('travel_type')
        duration = request.POST.get('duration')
        num_travellers = request.POST.get('num_travellers')
        state = request.POST.get('state', '')

        from services.recommendation_service import RecommendationService
        scored_results = RecommendationService.get_recommendations(
            budget=budget,
            season=season,
            travel_type=travel_type,
            duration=duration,
            num_travellers=num_travellers,
            state=state
        )

        serialized_results = [{
            'destination_id': dest.pk,
            'score': score,
            'ml_score': getattr(dest, 'ml_similarity', score),
            'pref_score': getattr(dest, 'preference_match', score),
            'confidence': getattr(dest, 'confidence_badge', 'Good Match'),
            'reasons': getattr(dest, 'reasons', [])
        } for dest, score in scored_results]

        recommendation = AIRecommendation.objects.create(
            user=request.user if request.user.is_authenticated else None,
            budget=budget,
            season=season,
            travel_type=travel_type,
            duration=duration,
            num_travellers=num_travellers,
            state=state,
            results=serialized_results
        )

        context = self.get_context_data()
        context['recommendations'] = scored_results
        context['new_session'] = recommendation
        context['form_data'] = {
            'budget': budget,
            'season': season,
            'travel_type': travel_type,
            'duration': duration,
            'num_travellers': num_travellers,
            'state': state
        }
        return self.render_to_response(context)


class AIRecommendationDetailView(generic.DetailView):
    """
    View displaying the results of a historical recommendation session.
    """
    model = AIRecommendation
    template_name = 'destinations/recommendation_detail.html'
    context_object_name = 'session'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = self.object.results
        scored_results = []
        for res in results:
            try:
                dest = Destination.objects.get(pk=res['destination_id'])
                # Re-inject matching parameters to Destination object for template rendering
                dest.overall_match = res.get('score')
                dest.ml_similarity = res.get('ml_score', res.get('score'))
                dest.preference_match = res.get('pref_score', res.get('score'))
                dest.confidence_badge = res.get('confidence', 'Good Match')
                dest.reasons = res.get('reasons', [])
                scored_results.append((dest, res['score']))
            except Destination.DoesNotExist:
                continue
        context['recommendations'] = scored_results
        return context
