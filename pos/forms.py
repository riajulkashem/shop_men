from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, HTML, \
    ButtonHolder, Submit
from django import forms
from django.forms import inlineformset_factory, Textarea, BaseInlineFormSet

from people.models import People
from pos.models import Shop, Shopping, ShopItem, Payment, CashOut, CashIn, \
    Expanse
from utilities.custom_layout_object import Formset


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        exclude = [
            'owner', 'admin_limit', 'staff_limit', 'cash_amount', 'capital',
            'creator', 'is_active'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ShopForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(
            Submit('submit', 'Submit', css_class='float-right')
        )


class CashInForm(forms.ModelForm):
    class Meta:
        model = CashIn
        fields = ['amount', 'note']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CashInForm, self).__init__(*args, **kwargs)


class CashOutForm(forms.ModelForm):
    class Meta:
        model = CashOut
        fields = ['amount', 'note']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CashOutForm, self).__init__(*args, **kwargs)


class ExpanseForm(forms.ModelForm):
    class Meta:
        model = Expanse
        fields = ['amount', 'note']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ExpanseForm, self).__init__(*args, **kwargs)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'payment_type', 'amount',
            'date', 'note',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PaymentForm, self).__init__(*args, **kwargs)


class ShopItemForm(forms.ModelForm):
    class Meta:
        model = ShopItem
        fields = ['product', 'quantity', 'price', 'tax_type', 'tax', 'total']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ShopItemForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['tax', 'tax_type']:
                self.fields[field].widget.attrs['class'] = field
                self.fields[field].widget.attrs['required'] = True
        self.fields['tax'].widget.attrs['class'] = 'product_tax'
        self.fields['tax_type'].widget.attrs['class'] = 'product_tax_type'
        for field in self.fields:
            self.fields[field].label = ''


class ProductBaseFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProductBaseFormset, self).__init__(*args, **kwargs)
        if user:
            for form in self.forms:
                if form.instance.pk is None:
                    form.instance.creator = user


ProductFormSet = inlineformset_factory(
    Shopping, ShopItem, form=ShopItemForm, extra=1, can_delete=True,
    exclude=['creator'], formset=ProductBaseFormset
)

ProductUpdateFormSet = inlineformset_factory(
    Shopping, ShopItem, form=ShopItemForm, extra=0, can_delete=True,
    exclude=['creator'], formset=ProductBaseFormset
)


class SaleForm(forms.ModelForm):
    class Meta:
        model = Shopping
        fields = [
            'people', 'sale_status', 'quantity',
            'other_charge_type', 'other_charge',
            'discount_type', 'discount', 'note',
            'date', 'reference', 'grand_total', 'paid',
            'due', 'sub_total', 'charge_total', 'discount_total',
            'payment_type'
        ]
        labels = {
            'people': 'Customer',
            'date': 'Sale Date',
        }
        widgets = {
            'note': Textarea(attrs={'rows': 1, 'cols': 20}),
            'grand_total': forms.HiddenInput(),
            'sub_total': forms.HiddenInput(),
            'charge_total': forms.HiddenInput(),
            'discount_total': forms.HiddenInput(),
            'due': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SaleForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].label = ''
        self.fields['paid'].widget.attrs['required'] = True
        if self.request:
            self.fields['people'].queryset = People.objects.filter(
                people_type='customer',
                shop=self.request.user.staff_shop
            ).exclude(id=0)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Row(
                Column('sub_total', css_class='col'),
                Column('charge_total', css_class='col'),
                Column('discount_total', css_class='col'),
                Column('grand_total', css_class='col'),
                Column('due', css_class='col'),
            ),
            Row(
                Column('people', css_class='col-sm-3'),
                Column('sale_status', css_class='col-md-3'),
                Column('date', css_class='col-md-3'),
                Column('reference', css_class='col-md-3'),
            ),
            Fieldset('Add Products', Formset('products')),
            Row(
                Column(
                    HTML('<h3>Quantity</h3>'),
                    css_class="col-md-3"
                ),
                Column('quantity',
                       css_class="col-md-3"
                       ),
                Column(
                    HTML('<h3>Sub Total:</h3> '),
                    css_class='col-md-3 text-right'
                ),
                Column(
                    HTML('<h3 id="sub_total">0.0</h3> '),
                    css_class='col-md-3 text-center'
                ),
                css_class="align-items-center mb-1 mt-3"
            ),
            Row(
                Column('other_charge', css_class='col-md-3'),
                Column('other_charge_type', css_class='col-md-3'),
                Column(
                    HTML('<h3>Other Charges: </h3> '),
                    css_class='col-md-3 text-right'
                ),
                Column(
                    HTML('<h3 id="other_charges">0.0</h3> '),
                    css_class='col-md-3 text-center'
                ),
                css_class="align-items-center"
            ),
            Row(
                Column('discount', css_class='col-md-3'),
                Column('discount_type', css_class='col-md-3'),
                Column(
                    HTML('<h3>Discount On All:</h3> '),
                    css_class='col-md-3 text-right'
                ),
                Column(
                    HTML('<h3 id="discount_on_all">0.0</h3> '),
                    css_class='col-md-3 text-center'
                ),
                css_class="align-items-center"
            ),
            Row(
                Column('note', css_class='col-md-6'),
                Column(
                    HTML('<h3>Grand Total:</h3> '),
                    css_class='col-md-3 text-right'
                ),
                Column(
                    HTML('<h3 id="grand_total">0.0</h3> '),
                    css_class='col-md-3 text-center'
                ),
                css_class="align-items-center"
            ),
            Fieldset(
                'Payment Information',
                Row(
                    Column('payment_type', css_class='col-md-3'),
                    Column(
                        'paid',
                        css_class='col-md-3 text-center'
                    ),
                    Column(
                        HTML('<h3>Due: </h3> '),
                        css_class='col-md-3 text-right'
                    ),
                    Column(
                        HTML('<h3 id="due">0</h3> '),
                        css_class='col-md-3'
                    ),

                    css_class="align-items-center"
                ),
            ),

            HTML("<br>"),
            ButtonHolder(Submit('submit', 'save'), css_class="float-right"),
        )


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Shopping
        fields = [
            'people', 'purchase_status', 'quantity',
            'other_charge_type', 'other_charge',
            'discount_type', 'discount', 'note',
            'date', 'reference', 'grand_total', 'paid',
            'due', 'sub_total', 'charge_total', 'discount_total',
            'payment_type'
        ]
        labels = {
            'people': 'Supplier',
            'date': 'Purchase Date',
        }
        widgets = {
            'note': Textarea(attrs={'rows': 1, 'cols': 20}),
            'grand_total': forms.HiddenInput(),
            'sub_total': forms.HiddenInput(),
            'charge_total': forms.HiddenInput(),
            'discount_total': forms.HiddenInput(),
            'due': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].label = ''
        self.fields['paid'].widget.attrs['required'] = True
        if self.request:
            self.fields['people'].queryset = People.objects.filter(
                people_type='supplier',
                shop=self.request.user.staff_shop
            )
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Row(
                Column('sub_total', css_class='col'),
                Column('charge_total', css_class='col'),
                Column('discount_total', css_class='col'),
                Column('grand_total', css_class='col'),
                Column('due', css_class='col'),
            ),
            Row(
                Column('people', css_class='col-sm-3'),
                Column('purchase_status', css_class='col-md-3'),
                Column('date', css_class='col-md-3'),
                Column('reference', css_class='col-md-3'),
            ),
            Fieldset('Add Products', Formset('products')),
            Row(
                Column(
                    HTML('<h3>Quantity</h3>'),
                    css_class="col-md-3"
                ),
                Column('quantity',
                       css_class="col-md-3"
                       ),
                Column(
                    HTML('<h3>Sub Total:</h3> '),
                    css_class='col-md-3 text-right'
                ),
                Column(
                    HTML('<h3 id="sub_total">0.0</h3> '),
                    css_class='col-md-3 text-center'
                ),
                css_class="align-items-center mb-1 mt-3"
            ),
            Row(
                Column('other_charge', css_class='col-md-3'),
                Column('other_charge_type', css_class='col-md-3'),
                Column(
                    HTML('<h3>Other Charges: </h3> '),
                    css_class='col-md-3 text-right'
                ),
                Column(
                    HTML('<h3 id="other_charges">0.0</h3> '),
                    css_class='col-md-3 text-center'
                ),
                css_class="align-items-center"
            ),
            Row(
                Column('discount', css_class='col-md-3'),
                Column('discount_type', css_class='col-md-3'),
                Column(
                    HTML('<h3>Discount On All:</h3> '),
                    css_class='col-md-3 text-right'
                ),
                Column(
                    HTML('<h3 id="discount_on_all">0.0</h3> '),
                    css_class='col-md-3 text-center'
                ),
                css_class="align-items-center"
            ),
            Row(
                Column('note', css_class='col-md-6'),
                Column(
                    HTML('<h3>Grand Total:</h3> '),
                    css_class='col-md-3 text-right'
                ),
                Column(
                    HTML('<h3 id="grand_total">0.0</h3> '),
                    css_class='col-md-3 text-center'
                ),
                css_class="align-items-center"
            ),
            Fieldset(
                'Payment Information',
                Row(
                    Column('payment_type', css_class='col-md-3'),
                    Column(
                        'paid',
                        css_class='col-md-3 text-center'
                    ),
                    Column(
                        HTML('<h3>Due: </h3> '),
                        css_class='col-md-3 text-right'
                    ),
                    Column(
                        HTML('<h3 id="due">0</h3> '),
                        css_class='col-md-3'
                    ),

                    css_class="align-items-center"
                ),
            ),

            HTML("<br>"),
            ButtonHolder(Submit('submit', 'save'), css_class="float-right"),
        )
