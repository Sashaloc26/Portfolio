from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Каталог'

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()  # получаем queryset
        category_id = self.kwargs.get('category_id')  # создаем ключ как в url
        return queryset.filter(
            category_id=category_id) if category_id else queryset  # фильтруем по этому ключи и проверяем что приходти

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():  # Если корзина не пуста то добавить этот обьект в корзину
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])  # Возвращение на ту страницу на которой юзер


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
