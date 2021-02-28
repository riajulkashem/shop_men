from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render

from people.models import People
from product.models import Product

class DashboardView(LoginRequiredMixin, View):
    template_name = "home.html"

    def get(self, request):
        context = {
            'customer_list':People.objects.exclude(
                id=0
            ).filter(
                people_type='customer',
                shop=request.user.staff_shop
            ).order_by('-shoppings__count')[:10],

            'supplier_list':People.objects.filter(
                people_type='supplier',
                shop=request.user.staff_shop
            ).order_by('-shoppings__count')[:10],

            'product_list':Product.objects.filter(
                shoppings__shopping__people__people_type='customer',
                shop_id=request.user.staff_shop
            ).order_by('-shoppings__count')[:10]
        }
        return render(request, self.template_name, context)
