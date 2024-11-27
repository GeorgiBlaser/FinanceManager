from django.urls import path
from .views import RegisterView, LoginView, ProfileView, CreatePostView, ContactView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('contact/', ContactView.as_view(), name='contact'),
]