from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from user.models import User, Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'pin', 'email', 'groups']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserForm, self).__init__(*args, **kwargs)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['created', 'updated', 'user', 'is_active']

    helper = FormHelper()
    helper.add_input(
        Submit('submit', 'Submit', css_class='btn-primary float-right')
    )
    helper.form_method = 'POST'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
