from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import reverse, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ProductForm
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

from catalog.models import Product, Category
from django.shortcuts import get_object_or_404
from catalog.services import get_products_by_category

class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = cache.get('my_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('my_queryset', queryset, 60 * 15)
            if not self.request.user.has_perm('catalog.can_unpublish_product'):
                queryset = queryset.exclude(status='draft')
        return queryset

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_info.html'
    context_object_name = 'product'

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_success_url(self):
        return reverse('catalog:product_info', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if 'status' in form.changed_data:
            if form.cleaned_data['status'] == 'draft':
                if not self.request.user.has_perm('catalog.can_unpublish_product'):
                    messages.error(self.request, 'У вас нет прав на снятие с публикации')
                    return self.form_invalid(form)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner

    def handle_no_permission(self):
        messages.error(self.request, 'Вы можете редактировать только свои продукты')
        return redirect('catalog:product_info', pk=self.kwargs.get('pk'))

class ProductDeliteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'product_delite.html'
    success_url = reverse_lazy('catalog:home')

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав на удаление продукта')
        return redirect('catalog:product_info', pk=self.kwargs.get('pk'))

    def test_func(self):
        product = self.get_object()
        return (self.request.user == product.owner or
                self.request.user.has_perm('catalog.delete_product'))


class ProductUnpublishView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        if product.status != 'draft':
            product.status = 'draft'
            product.save()
            messages.success(request, 'Продукт снят с публикации')
        else:
            messages.warning(request, 'Продукт уже не опубликован')

        return redirect('catalog:product_info', pk=product.pk)

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав на снятие с публикации')
        return redirect('catalog:product_info', pk=self.kwargs.get('pk'))

class ProductsByCategoryDetailView(DetailView):
    model = Category
    template_name = 'products_by_category.html'
    context_object_name = 'product_by_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs.get('pk')
        context["category_products"] = get_products_by_category(cat_id)
        return context

    def get_queryset(self):
        queryset = cache.get('my_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('my_queryset', queryset, 60 * 15)  # Кешируем данные на 15 минут
        return queryset

class CategoryListView(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categorys'