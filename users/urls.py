from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='verfy_token'),

    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('verify_email/', views.VerifyEmail.as_view(), name="email-verify"),

    path('', views.UsersView.as_view(), name='all_users'),
    path('<int:pk>/', views.UserView.as_view(), name='user_url'),
    # path('groups/', views.UsersView.as_view(), name='all_users'),
    # path('groups/<int:pk>/', views.UserView.as_view(), name='get, update'),

]
