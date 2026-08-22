from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm

class RegisterView(SuccessMessageMixin, generic.CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    success_message = "Your account was created successfully. You can now log in!"

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    authentication_form = UserLoginForm
    
    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)


class UserLogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You have been successfully logged out.")
        return super().dispatch(request, *args, **kwargs)


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = "Your profile has been updated successfully."

    def get_object(self, queryset=None):
        return self.request.user

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class UserPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, auth_views.PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = "Your password has been changed successfully."

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class UserPasswordResetView(auth_views.PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = UserSetPasswordForm
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

from django.http import JsonResponse
from django.views import View


class WishlistToggleView(LoginRequiredMixin, View):
    """
    AJAX endpoint to add or remove a destination from the user's saved wishlist.
    Returns JSON with the updated saved state.
    """
    def post(self, request, dest_pk, *args, **kwargs):
        from destinations.models import Destination
        from .models import UserProfile
        try:
            dest = Destination.objects.get(pk=dest_pk)
        except Destination.DoesNotExist:
            return JsonResponse({'error': 'Destination not found.'}, status=404)
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        if dest in profile.saved_destinations.all():
            profile.saved_destinations.remove(dest)
            saved = False
        else:
            profile.saved_destinations.add(dest)
            saved = True
        return JsonResponse({'saved': saved, 'dest_id': dest_pk})


class DeleteAccountView(LoginRequiredMixin, View):
    """
    Allows users to permanently delete their own account after modal confirmation.
    """
    def post(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('home')


class AvatarUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """
    Allows users to upload or change their profile avatar image.
    """
    success_url = reverse_lazy('accounts:profile')
    success_message = 'Profile photo updated successfully.'

    def get_form_class(self):
        from .forms import UserAvatarForm
        return UserAvatarForm

    def get_object(self, queryset=None):
        from .models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
