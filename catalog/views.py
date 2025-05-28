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
        queryset = super().get_queryset()
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

class ProductsByCategoryView(ListView):
    model = Category
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        if 'category_slug' in self.kwargs:
            self.current_category = get_object_or_404(Category, slag=self.kwargs['category_slug'])
            return Product.objects.filter(
                category=self.current_category,
                status='published'
            ).select_related('category')
        return Product.objects.filter(status='published').select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.get()
        if hasattr(self, 'current_category'):
            context['current_category'] = self.current_category
        return context