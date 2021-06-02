from django.urls import path
from automations.views import automation

urlpatterns = [
    path('', automation.Views.as_view(), name='automations'),
    path('<int:pk>/', automation.View.as_view(), name='automation'),
]
