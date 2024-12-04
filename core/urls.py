from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import RegisterView, LoginView, ProfileView, CreatePostView, ContactView, HomeView, PostListView, \
    PostDetailView, UpdatePostView, DeletePostView, logout_view, category_list_view, transaction_list_view, \
    create_category_view, edit_category_view, delete_category_view, create_transaction_view, create_budget_view, \
    delete_transaction_view, edit_transaction_view, budget_list_view, edit_budget_view, delete_budget_view, \
    EditProfileView, delete_comment_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('budgets/', budget_list_view, name='budgets'),
    path('budgets/create/', create_budget_view, name='create_budget'),
    path('budgets/edit/<int:pk>/', edit_budget_view, name='edit_budget'),
    path('budgets/delete/<int:pk>/', delete_budget_view, name='delete_budget'),
    path('categories/', category_list_view, name='categories'),
    path('categories/create/', create_category_view, name='create_category'),
    path('categories/edit/<int:pk>/', edit_category_view, name='edit_category'),
    path('categories/delete/<int:pk>/', delete_category_view, name='delete_category'),
    path('transactions/create/', create_transaction_view, name='create_transaction'),
    path('transactions/', transaction_list_view, name='transactions'),
    path('transactions/create/', create_transaction_view, name='create_transaction'),
    path('transactions/edit/<int:pk>/', edit_transaction_view, name='edit_transaction'),
    path('transactions/delete/<int:pk>/', delete_transaction_view, name='delete_transaction'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', UpdatePostView.as_view(), name='update_post'),
    path('posts/<int:pk>/delete/', DeletePostView.as_view(), name='delete_post'),
    path('delete_comment/<int:pk>/', delete_comment_view, name='delete_comment'),
    path('logout/', logout_view, name='logout'),
]
