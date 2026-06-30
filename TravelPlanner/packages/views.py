from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Package
from .forms import PackageForm

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


class PackageCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
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


class PackageUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
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


class PackageDeleteView(LoginRequiredMixin, generic.DeleteView):
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
