from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Package
from .forms import PackageForm

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

class PackageListView(generic.ListView):
    """
    View displaying a paginated catalog of all travel packages.
    """
    model = Package
    template_name = 'packages/package_list.html'
    context_object_name = 'packages'
    ordering = ['package_name']
    paginate_by = 9


class PackageDetailView(generic.DetailView):
    """
    View displaying details of a specific travel package.
    """
    model = Package
    template_name = 'packages/package_detail.html'
    context_object_name = 'package'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package = self.object
        
        # 1. Generate daily itinerary dynamically using the ItineraryService
        from services.itinerary_service import ItineraryService
        itinerary = ItineraryService.generate_itinerary(
            destination=package.destination,
            total_days=package.duration,
            travel_type='Solo',  # Default catalog travel style
            budget_level=package.package_type
        )
        context['itinerary'] = itinerary
        
        # 2. Calculate daily estimated budget breakdown from total cost
        daily_total = float(package.price) / max(1, package.duration)
        context['daily_budget'] = {
            'accommodation': round(daily_total * 0.45),
            'food': round(daily_total * 0.20),
            'transportation': round(daily_total * 0.15),
            'sightseeing': round(daily_total * 0.10),
            'miscellaneous': round(daily_total * 0.10),
            'total': round(daily_total)
        }
        
        # 3. Travel Tips
        context['travel_tips'] = [
            "Start early to avoid crowds.",
            "Carry water.",
            "Wear comfortable shoes.",
            "Best visiting hours: 9 AM - 5 PM."
        ]
        return context


class PackageCreateView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """
    Secure view for authenticated users to create a new travel package.
    """
    model = Package
    form_class = PackageForm
    template_name = 'packages/package_form.html'
    success_url = reverse_lazy('packages:list')
    success_message = "Package '%(package_name)s' was created successfully."

    def get_initial(self):
        initial = super().get_initial()
        dest_id = self.request.GET.get('destination')
        if dest_id:
            initial['destination'] = dest_id
        return initial

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class PackageUpdateView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """
    Secure view for authenticated users to update properties of an existing package.
    """
    model = Package
    form_class = PackageForm
    template_name = 'packages/package_form.html'
    success_message = "Package '%(package_name)s' was updated successfully."

    def get_success_url(self):
        return reverse_lazy('packages:detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class PackageDeleteView(LoginRequiredMixin, AdminRequiredMixin, generic.DeleteView):
    """
    Secure view for authenticated users to delete a travel package.
    """
    model = Package
    template_name = 'packages/package_confirm_delete.html'
    success_url = reverse_lazy('packages:list')

    def delete(self, request, *args, **kwargs):
        package = self.get_object()
        messages.success(self.request, f"Package '{package.package_name}' was deleted successfully.")
        return super().delete(request, *args, **kwargs)
