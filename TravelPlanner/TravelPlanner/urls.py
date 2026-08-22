"""
URL configuration for TravelPlanner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from destinations.views import HomeView

# Wrap admin.site.index to inject quick homepage metrics
from django.contrib.auth import get_user_model
from destinations.models import Destination
from trips.models import Trip
from packages.models import Package

original_admin_index = admin.site.index

def custom_admin_index(request, extra_context=None):
    extra_context = extra_context or {}
    User = get_user_model()
    from attractions.models import Attraction
    
    extra_context.update({
        'total_users': User.objects.count(),
        'total_destinations': Destination.objects.count(),
        'total_trips': Trip.objects.count(),
        'total_packages': Package.objects.count(),
        'popular_cities': Destination.objects.order_by('-average_rating')[:3],
        'popular_activities': Attraction.objects.order_by('-average_visit_time')[:3],
    })

    return original_admin_index(request, extra_context)

admin.site.index = custom_admin_index

from dashboard.views import UniversalSearchView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('trips/', include('trips.urls')),
    path('destinations/', include('destinations.urls')),
    path('attractions/', include('attractions.urls')),
    path('packages/', include('packages.urls')),
    path('api/', include('api.urls')),
    path('universal-search/', UniversalSearchView.as_view(), name='universal_search'),
]

from django.urls import re_path
from django.views.static import serve

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

