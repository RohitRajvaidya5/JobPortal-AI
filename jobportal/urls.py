from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.api.urls')),
    path('jobs/', include('jobs.api.urls')),
    path('matching/', include('matching.api.urls')),
]
