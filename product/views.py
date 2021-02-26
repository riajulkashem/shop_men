from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from product.forms import BrandForm, CategoryForm, ProductForm
from product.models import Brand, Category, Product
from utilities.views import CRUDView


class BrandCRUDView(CRUDView):
    model = Brand
    template_name = 'brand.html'
    success_url = reverse_lazy('product:brand')
    form_class = BrandForm


class CategoryCRUDView(CRUDView):
    model = Category
    template_name = 'category.html'
    success_url = reverse_lazy('product:category')
    form_class = CategoryForm


class ProductCRUDView(CRUDView):
    model = Product
    template_name = 'product.html'
    success_url = reverse_lazy('product:product')
    form_class = ProductForm


@login_required
def product_details(request, pk):
    if request.is_ajax() and request.user.staff_shop_id is not None:
        product = get_object_or_404(Product, pk=pk)
        return JsonResponse(
            {
                'buy_price': product.purchase_price,
                'stock': product.stock,
                'sell_price': product.sell_price
            }
        )
    return JsonResponse(
        {'error': 'You don\'t have permission to view details'})
