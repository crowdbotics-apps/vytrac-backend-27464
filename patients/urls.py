
from django.urls import path

from .views import goals, dalyplan, roster, payment, patients, Emergency_contact

urlpatterns = [

    path('emergency_contact/', Emergency_contact.Views.as_view(), name='Emergency_contacts'),
    path('emergency_contact/<int:pk>/', Emergency_contact.View.as_view(), name='Emergency_contact'),


    path('goals/', goals.Views.as_view(), name='Goals'),
    path('goals/<int:pk>/', goals.View.as_view(), name='Goal'),

    path('dalyplans/', dalyplan.Views.as_view(), name='plans'),
    path('dalyplans/<int:pk>/', dalyplan.View.as_view(), name='plan'),

    path('rosters/', roster.Views.as_view(), name='rosters'),
    path('rosters/<int:pk>/', roster.View.as_view(), name='roster'),

    path('billings/', payment.Views.as_view(), name='billings'),
    path('billings/<int:pk>/', payment.View.as_view(), name='billing'),

    path('', patients.Views.as_view(), name='PationtsView'),
    path('<int:pk>/', patients.View.as_view(), name='PationtsView'),
]
