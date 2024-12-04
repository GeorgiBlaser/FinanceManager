from django.contrib import admin
from .models import Profile, Post, Comment, Category, ContactMessage,Transaction, Budget


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'first_name', 'last_name')
    search_fields = ('user__username', 'email', 'first_name', 'last_name')
    list_filter = ('last_login',)
    ordering = ('user__username',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'user')
    search_fields = ('name', 'user__username')
    list_filter = ('user',)
    ordering = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'category', 'created_at', 'description')
    search_fields = ('description', 'category__name')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('amount', 'user', 'category', 'from_date', 'to_date')
    search_fields = ('user__username', 'category__name')
    list_filter = ('from_date', 'to_date')
    ordering = ('-from_date',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'sent_at')
    search_fields = ('name', 'email', 'message')
