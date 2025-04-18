from django.shortcuts import render, redirect
from django.db.models import Q  # Добавьте этот импорт
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import RegisterForm
from .models import Product, Category
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})





class ProductListView(ListView):
    model = Product
    template_name = 'core/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['-created_at']  # Сортировка по умолчанию

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)

        # Поиск по названию и описанию
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Фильтрация по категории
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Фильтрация по цене
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'core/product_detail.html'
    context_object_name = 'product'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'core/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(seller=self.request.user)
        return context


def home(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    return render(request, 'core/home.html', {'products': products})