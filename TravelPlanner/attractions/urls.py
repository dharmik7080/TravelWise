from django.urls import path
from .views import (
    AttractionListView, AttractionDetailView, AttractionCreateView,
    AttractionUpdateView, AttractionDeleteView
)

app_name = 'attractions'

urlpatterns = [
    path('', AttractionListView.as_view(), name='list'),
    path('add/', AttractionCreateView.as_view(), name='create'),
    path('<int:pk>/', AttractionDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', AttractionUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', AttractionDeleteView.as_view(), name='delete'),
]
