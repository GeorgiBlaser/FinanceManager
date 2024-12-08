from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, FormView, UpdateView, TemplateView, ListView, DetailView, DeleteView
from .forms import RegistrationForm, LoginForm, ProfileForm, CreatePostForm, ContactForm, TransactionForm, BudgetForm, \
    CategoryForm, CommentForm
from .models import Profile, Post, Transaction, Budget, Category, ContactMessage, Comment


class HomeView(TemplateView):
    template_name = 'home.html'


class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        # Create an account
        Profile.objects.get_or_create(user=user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('profile')  # Redirect to profile after login

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid username or password.")
            return self.form_invalid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Financial logic
        total_budget = Budget.objects.filter(user=self.request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        transactions = Transaction.objects.filter(category__user=self.request.user)
        total_income = transactions.filter(amount__gt=0).aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum'] or 0

        # Adding data to context
        context.update({
            'total_budget': total_budget,
            'total_income': total_income,
            'total_expense': total_expense,
        })
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)  # Create an account if you don't have one
        return profile


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'create_post.html'
    success_url = reverse_lazy('post_list')  # After publishing, returns to the list of posts
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Save the message in the database
        ContactMessage.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            message=form.cleaned_data['message'],
        )
        messages.success(self.request, "Your message has been sent successfully!")
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            context['new_comments'] = {
                post.id: post.has_new_comments() for post in context['posts']
            }
        else:
            context['new_comments'] = {}
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user == self.object.author:
            # Update `last_viewed`
            self.object.last_viewed = timezone.now()
            self.object.save()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return HttpResponseRedirect(reverse('post_detail', args=[self.object.id]))
        return self.get(request, *args, **kwargs)


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'update_post.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        # Checks if the current user is the author of the post
        post = self.get_object()
        return self.request.user == post.author


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        # Checks if the current user is the author of the post
        post = self.get_object()
        return self.request.user == post.author


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def budget_list_view(request):
    budgets = Budget.objects.filter(user=request.user)
    paginator = Paginator(budgets, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'budgets.html', {'page_obj': page_obj})


@login_required
def create_budget_view(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user  # Associate the budget with the current user
            budget.save()
            return redirect('budgets')  # Redirect to budget list
    else:
        form = BudgetForm()
        form.fields['category'].queryset = Category.objects.filter(user=request.user)  # Limiting the categories
    return render(request, 'create_budget.html', {'form': form})


@login_required
def edit_budget_view(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budgets')
    else:
        form = BudgetForm(instance=budget)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
    return render(request, 'edit_budget.html', {'form': form})


@login_required
def delete_budget_view(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == "POST":
        budget.delete()
        return redirect('budgets')
    return render(request, 'delete_budget.html', {'budget': budget})


@login_required
def category_list_view(request):
    categories = Category.objects.filter(user=request.user)
    paginator = Paginator(categories, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'categories.html', {'page_obj': page_obj})


@login_required
def transaction_list_view(request):
    transactions = Transaction.objects.filter(category__user=request.user).select_related('category')
    paginator = Paginator(transactions, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'transactions.html', {'page_obj': page_obj})


@login_required
def create_category_view(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('categories')
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})


@login_required
def edit_category_view(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form})


@login_required
def delete_category_view(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == "POST":
        category.delete()
        return redirect('categories')
    return render(request, 'delete_category.html', {'category': category})


@login_required
def create_transaction_view(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.category.user = request.user

            # Checking if the transaction is an expense (different from "Income")
            if transaction.category.name.lower() != 'income':
                transaction.amount = -abs(transaction.amount)  # Force a negative value

                # Reducing Total Budget
                user_budget = Budget.objects.filter(user=request.user, category=transaction.category).first()
                if user_budget:
                    user_budget.amount -= abs(transaction.amount)
                    user_budget.save()

            transaction.save()
            return redirect('transactions')
    else:
        form = TransactionForm()
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
    return render(request, 'create_transaction.html', {'form': form})


@login_required
def edit_transaction_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, category__user=request.user)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transactions')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'edit_transaction.html', {'form': form})


@login_required
def delete_transaction_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, category__user=request.user)
    if request.method == "POST":
        transaction.delete()
        return redirect('transactions')
    return render(request, 'delete_transaction.html', {'transaction': transaction})


@login_required
def delete_comment_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.author or request.user == comment.post.author:
        comment.delete()
        return HttpResponseRedirect(reverse('post_detail', args=[comment.post.id]))
    else:
        return HttpResponseRedirect(reverse('home'))


def custom_permission_denied_view(request, exception):
    return render(request, '403.html', status=403)














