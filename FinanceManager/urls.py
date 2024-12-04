from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]

handler403 = 'core.views.custom_permission_denied_view'
