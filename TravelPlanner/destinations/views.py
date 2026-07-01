from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Destination
from .forms import DestinationForm

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
        return context


class DestinationCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
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


class DestinationUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
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


class DestinationDeleteView(LoginRequiredMixin, generic.DeleteView):
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
        # Query top 6 highest-rated featured destinations dynamically
        context['featured_destinations'] = Destination.objects.all().order_by('-average_rating')[:6]
        
        # Query first package with an image for the homepage featured package card
        from packages.models import Package
        context['featured_package'] = Package.objects.filter(image__isnull=False).exclude(image='').first()
        
        return context
