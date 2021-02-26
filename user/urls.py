from django.urls import path, include
from user import views
from utilities.methods import get_urls_for_views

app_name = 'user'

urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path(
        'profile/<int:pk>/update/',
        views.ProfileUpdateView.as_view(),
        name='profile_update'
    ),
    path('', include(get_urls_for_views(views))),
]
