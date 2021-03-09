import json

from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import View, UpdateView

from people.forms import PeopleForm
from people.models import People
from pos.forms import (
    ShopForm, SaleForm, ProductFormSet,
    ProductUpdateFormSet,
    PurchaseForm, CashInForm, CashOutForm,
    ExpanseForm
)
from pos.models import (
    Shop, Shopping, ShopItem,
    PaymentType, CashIn,
    CashOut, Expanse
)
from product.models import Product, Category
from utilities.views import CRUDView


class ShopCRUDView(CRUDView):
    model = Shop
    template_name = 'shop.html'
    success_url = reverse_lazy('pos:shop')
    form_class = ShopForm
    assign_shop = False

    def get_queryset(self):
        qs = super(ShopCRUDView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class CashInCRUDView(CRUDView):
    model = CashIn
    template_name = 'cash.html'
    success_url = reverse_lazy('pos:cashin')
    form_class = CashInForm
    add_amount = True


class CashOutCRUDView(CRUDView):
    model = CashOut
    template_name = 'cash.html'
    success_url = reverse_lazy('pos:cashout')
    form_class = CashOutForm


class ExpanseCRUDView(CRUDView):
    model = Expanse
    template_name = 'cash.html'
    success_url = reverse_lazy('pos:expanse')
    form_class = ExpanseForm


def shopping_context_data(self, sale=True, **kwargs):
    data = {}
    form_kwargs = {'request': self.request}
    if sale:
        data['page_title'] = "Sale"
    else:
        data['page_title'] = 'Purchase'
    if self.request.POST:
        if self.object:
            data['products'] = ProductUpdateFormSet(
                self.request.POST, form_kwargs=form_kwargs,
                instance=self.object,
            )
        else:
            data['products'] = ProductFormSet(
                self.request.POST, form_kwargs=form_kwargs
            )
    else:
        if self.object:
            data['products'] = ProductUpdateFormSet(
                form_kwargs=form_kwargs, instance=self.object
            )
        else:
            data['products'] = ProductFormSet(form_kwargs=form_kwargs)
    for form in data['products']:
        for field in form.fields:
            form.fields[field].label = ''
    return data


def shopping_form_valid(self, form, sale=True):
    cache.delete(self.get_cache_key())
    context = self.get_context_data()
    products = context['products']
    items = context['products'].cleaned_data
    with transaction.atomic():
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.shop = self.request.user.staff_shop
        self.object.save()
        if products.is_valid():
            products.instance = self.object
            products.save()
        for p in items:
            product = p['product']
            if sale:
                product.stock = product.stock - int(p['quantity'])
            else:
                product.stock = product.stock + int(p['quantity'])
            product.save()
    return HttpResponseRedirect(self.get_success_url())


class SaleView(CRUDView):
    model = Shopping
    template_name = 'sale_list.html'
    success_url = reverse_lazy('pos:sale_list')
    form_class = SaleForm
    pdf_template = 'invoice.html'
    pdf_file_name = 'purchase_invoice'

    def get_success_url(self):
        return reverse_lazy('pos:sale_invoice', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = shopping_context_data(self, sale=True, **kwargs)
        context.update(**data)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(people__people_type='customer')

    def get(self, request, *args, **kwargs):
        if reverse_lazy('pos:sale_create') == request.path:
            self.template_name = 'shopping_form.html'
        if 'update' in request.path:
            self.template_name = 'shopping_form.html'
        if 'invoice' in request.path:
            self.pdf_response = True

        return super(SaleView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        return shopping_form_valid(self, form, sale=False)


class PurchaseView(CRUDView):
    model = Shopping
    template_name = 'purchase_list.html'
    success_url = reverse_lazy('pos:purchase_list')
    form_class = PurchaseForm
    pdf_template = 'invoice.html'
    pdf_file_name = 'purchase_invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = shopping_context_data(self, sale=False, **kwargs)
        context.update(**data)
        return context

    def get_success_url(self):
        return reverse_lazy(
            'pos:purchase_invoice', kwargs={'pk': self.object.id}
        )

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(people__people_type='supplier')

    def get(self, request, *args, **kwargs):
        if reverse_lazy('pos:purchase_create') == request.path:
            self.template_name = 'shopping_form.html'
        if 'update' in request.path:
            self.template_name = 'shopping_form.html'
        if 'invoice' in request.path:
            self.pdf_response = True

        return super(PurchaseView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        return shopping_form_valid(self, form, sale=False)


class PosView(LoginRequiredMixin, View):
    model = Shopping
    template = 'pos.html'

    def get_context_data(self, **kwargs):
        context = {
            'customers': People.objects.all(),
            'products': Product.objects.all(),
            'categories': Category.objects.all(),
            'payments': PaymentType.objects.all(),
            'form': PeopleForm(),
        }
        return context

    def get(self, request):
        return render(request, self.template, self.get_context_data())

    def post(self, request):
        data = products_data = {}
        dt = request.POST.copy()
        items = dt.pop('items')
        dt.pop('csrfmiddlewaretoken')
        for key in list(dt.keys()):
            data[key] = dt.get(key)

        data['quantity'] = len(items)
        data['sale_status'] = 'final'
        data['creator_id'] = request.user.id
        data['shop_id'] = request.user.staff_shop_id
        data['date'] = timezone.now()
        if not People.objects.filter(id=0).exists():
            People.objects.create(
                id=0, people_type='customer', name='Walk In Customer',
                creator_id=1
            )
        items = json.loads(items[0])
        sale = Shopping.objects.create(**data)
        products = []
        for dt in items:
            dt['creator_id'] = request.user.id
            dt['shopping_id'] = sale.id
            ShopItem(products_data)
        ShopItem.objects.bulk_create(products)

        # Upadte Product Stock
        with transaction.atomic():
            for p in items:
                product = Product.objects.get(id=p['product_id'])
                product.stock = product.stock - int(p['quantity'])
                product.save()
        context = {
            'msg': 'Sale Information Saved Successfuly',
            'pk': sale.shopping_id
        }
        return JsonResponse(context)


class ShopSettings(LoginRequiredMixin, UpdateView):
    model = Shop
    form_class = ShopForm
    success_url = reverse_lazy('dashboard')
    template_name = 'settings.html'
