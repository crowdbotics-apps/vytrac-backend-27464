from rest_framework_swagger.views import get_swagger_view
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import permissions
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),

    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('billing/', include('billings.urls')),
    path('calendars/', include('calendars.urls')),
    path('patient/', include('patientsprofiles.urls')),
    path('groups/', include('permissions.urls')),
    path('statistics/', include('timesheets.urls')),
    path('reports/', include('reports.urls')),

]
