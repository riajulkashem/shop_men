from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from people.forms import PeopleForm
from people.models import People
from utilities.views import CRUDView


class CustomerCRUDView(CRUDView):
    model = People
    template_name = 'customer.html'
    success_url = reverse_lazy('people:customer')
    form_class = PeopleForm
    has_update_url = True

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(people_type='customer')

    def form_valid(self, form):
        cache.delete(self.get_cache_key())
        if self.object:
            form = self.get_form()
            messages.success(
                self.request, f'{self.object} Update Successfully')
        else:
            form.instance.creator = self.request.user
            if self.assign_shop:
                form.instance.shop_id = self.request.user.staff_shop_id
                form.instance.people_type = 'customer'
            messages.success(
                self.request,
                f'{self.model._meta.verbose_name} Created Successfully'
            )
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class SupplierCRUDView(CRUDView):
    model = People
    template_name = 'customer.html'
    success_url = reverse_lazy('people:supplier')
    form_class = PeopleForm
    has_update_url = True

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(people_type='supplier')

    def form_valid(self, form):
        cache.delete(self.get_cache_key())
        if self.object:
            form = self.get_form()
            messages.success(
                self.request, f'{self.object} Update Successfully')
        else:
            form.instance.creator = self.request.user
            if self.assign_shop:
                form.instance.shop_id = self.request.user.staff_shop_id
                form.instance.people_type = 'supplier'
            messages.success(
                self.request,
                f'{self.model._meta.verbose_name} Created Successfully')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())
