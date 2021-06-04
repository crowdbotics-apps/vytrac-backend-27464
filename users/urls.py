from django.urls import path
from users import Usersviews
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)
from .views import userssettings

urlpatterns = [
    path('usersettings/', userssettings.Views.as_view(), name="usersettings"),
    path('usersettings/<int:pk>/',
         userssettings.View.as_view(), name='userettings'),

    path('register/', Usersviews.RegisterView.as_view(), name="register"),
    path('login/', Usersviews.LoginView.as_view(), name='login'),
    path('logout/', Usersviews.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='verfy_token'),

    path('request-reset-email/', Usersviews.RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset-complete/', Usersviews.SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('verify_email/', Usersviews.VerifyEmail.as_view(), name="email-verify"),

    path('', Usersviews.UsersView.as_view(), name='all_users'),
    path('<int:pk>/', Usersviews.UserView.as_view(), name='user_url'),
    # path('groups/', Usersviews.UsersView.as_view(), name='all_users'),
    # path('groups/<int:pk>/', Usersviews.UserView.as_view(), name='get, update'),

]
