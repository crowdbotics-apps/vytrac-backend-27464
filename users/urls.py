from django.urls import path
from users import myviews
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)
from .views import userssettings


urlpatterns = [
    path('usersettings/', userssettings.Views.as_view(), name="usersettings"),
    path('usersettings/<int:pk>/',
         userssettings.View.as_view(), name='userettings'),

    path('register/', myviews.RegisterView.as_view(), name="register"),
    path('login/', myviews.LoginView.as_view(), name='login'),
    path('logout/', myviews.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='verfy_token'),

    path('request-reset-email/', myviews.RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset-complete/', myviews.SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('verify_email/', myviews.VerifyEmail.as_view(), name="email-verify"),

    path('', myviews.UsersView.as_view(), name='all_users'),
    path('<int:pk>/', myviews.UserView.as_view(), name='user_url'),
    # path('groups/', myviews.UsersView.as_view(), name='all_users'),
    # path('groups/<int:pk>/', myviews.UserView.as_view(), name='get, update'),

]
