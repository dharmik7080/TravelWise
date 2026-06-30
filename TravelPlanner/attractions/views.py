from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from destinations.models import Destination
from .models import Attraction
from .forms import AttractionForm

class AttractionListView(generic.ListView):
    """
    View displaying a list of all tourist attractions with pagination,
    supporting name search and destination/category/entry type filtering.
    """
    model = Attraction
    template_name = 'attractions/attraction_list.html'
    context_object_name = 'attractions'
    ordering = ['attraction_name']
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 1. Search Query
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(attraction_name__icontains=query)
            
        # 2. Dynamic Filtering
        destination_id = self.request.GET.get('destination', '').strip()
        category = self.request.GET.get('category', '').strip()
        entry_type = self.request.GET.get('entry_type', '').strip()

        if destination_id:
            queryset = queryset.filter(destination_id=destination_id)
        if category:
            queryset = queryset.filter(category__iexact=category)
        if entry_type == 'free':
            queryset = queryset.filter(entry_fee=0.00)
        elif entry_type == 'paid':
            queryset = queryset.filter(entry_fee__gt=0.00)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Dynamic selections lookup options list
        context['destinations_list'] = Destination.objects.all().order_by('destination_name')
        context['categories'] = sorted(list(Attraction.objects.values_list('category', flat=True).distinct().exclude(category='')))
        
        # Build clean query parameters mapping dict
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


class AttractionDetailView(generic.DetailView):
    """
    View displaying the details profile of a specific tourist attraction.
    """
    model = Attraction
    template_name = 'attractions/attraction_detail.html'
    context_object_name = 'attraction'


class AttractionCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """
    Secure view for authenticated users to register a new tourist attraction.
    Pre-populates the destination selection if passed via query parameters.
    """
    model = Attraction
    form_class = AttractionForm
    template_name = 'attractions/attraction_form.html'
    success_url = reverse_lazy('attractions:list')
    success_message = "Attraction '%(attraction_name)s' was created successfully."

    def get_initial(self):
        initial = super().get_initial()
        dest_id = self.request.GET.get('destination')
        if dest_id:
            initial['destination'] = dest_id
        return initial

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class AttractionUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """
    Secure view for authenticated users to edit an existing attraction.
    """
    model = Attraction
    form_class = AttractionForm
    template_name = 'attractions/attraction_form.html'
    success_message = "Attraction '%(attraction_name)s' was updated successfully."

    def get_success_url(self):
        return reverse_lazy('attractions:detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class AttractionDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Secure view for authenticated users to delete a tourist attraction.
    """
    model = Attraction
    template_name = 'attractions/attraction_confirm_delete.html'
    success_url = reverse_lazy('attractions:list')

    def delete(self, request, *args, **kwargs):
        attraction = self.get_object()
        messages.success(self.request, f"Attraction '{attraction.attraction_name}' was deleted successfully.")
        return super().delete(request, *args, **kwargs)
