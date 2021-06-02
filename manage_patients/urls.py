from django.urls import path
from .views import goals, dalyplan, roster, payment, profiles


urlpatterns = [
    path('goals/', goals.Views.as_view(), name='Goals'),
    path('goals/<int:pk>/', goals.View.as_view(), name='Goal'),

    path('dalyplans/', dalyplan.Views.as_view(), name='plans'),
    path('dalyplans/<int:pk>/', dalyplan.View.as_view(), name='plan'),

    path('rosters/', roster.Views.as_view(), name='rosters'),
    path('rosters/<int:pk>/', roster.View.as_view(), name='roster'),

    path('billings/', payment.Views.as_view(), name='billings'),
    path('billings/<int:pk>/', payment.View.as_view(), name='billing'),

    path('', profiles.Views.as_view(), name='PationtsView'),
    path('<int:pk>/', profiles.View.as_view(), name='PationtsView'),
]
