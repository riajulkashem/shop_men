from django import forms
from django.forms import Textarea

from people.models import People


class PeopleForm(forms.ModelForm):
    class Meta:
        model = People
        fields = [
            'name', 'email', 'photo', 'phone', 'address',
            'opening_balance',
        ]

        widgets = {
            'address': Textarea(attrs={'rows': 1, 'cols': 20}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PeopleForm, self).__init__(*args, **kwargs)
