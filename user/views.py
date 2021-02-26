from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from user.forms import UserForm, ProfileForm
from user.models import User, Profile
from utilities.views import CRUDView


class UserCRUDView(CRUDView):
    model = User
    template_name = 'user_list.html'
    form_class = UserForm

    def get_queryset(self):
        qs = super(UserCRUDView, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        return self.request.user.staff_shop.staff_list.all()

    def form_valid(self, form):
        pin = form.instance.pin
        form.instance.set_password(pin)
        return super(UserCRUDView, self).form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('dashboard')


def sign_in(request):
    print('ajax requested for login')
    if request.is_ajax():
        user_id = request.POST.get('id')
        try:
            admin = get_object_or_404(User, pk=int(user_id))
            user = authenticate(username=admin.phone, password=admin.pin)
            if user is not None and user.is_active:
                login(request, user)
                print('success login')
                return JsonResponse(data={'success': 'success'})
            else:
                return JsonResponse(
                    data={
                        'error': 'Error User ' + str(user) + ' is not active'
                    }
                )
        except ObjectDoesNotExist or ValueError:
            return JsonResponse(data={'error': 'Error user is not exist'})

    if request.method == 'POST':
        username = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard')

            messages.add_message(
                request,
                messages.WARNING,
                'Your account has been disabled.. !\nPlease Contact With '
                + 'Administrator'
            )
            return redirect('user:sign_in')
        else:
            messages.add_message(
                request, messages.ERROR,
                "Username or password is incorrect."
            )
            return render(request, 'login.html',
                          {'form': AuthenticationForm()})

    return render(request, 'login.html', {'form': AuthenticationForm()})


def sign_out(request):
    logout(request)
    return redirect('user:sign_in')


@login_required
def dashboard(request):
    context = {'page_title': request.user.get_full_name()}
    return render(request, 'home.html', context)
