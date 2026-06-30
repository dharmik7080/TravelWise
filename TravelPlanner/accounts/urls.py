from django.urls import path
from .views import (
    RegisterView, UserLoginView, UserLogoutView, ProfileUpdateView,
    UserPasswordChangeView, UserPasswordResetView, UserPasswordResetDoneView,
    UserPasswordResetConfirmView, UserPasswordResetCompleteView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
