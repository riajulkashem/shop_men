from django.urls import path, include

from product import views
from utilities.methods import get_urls_for_views

app_name = 'product'

urlpatterns = [
    path('', include(get_urls_for_views(views))),
    path(
        'product_details/<int:pk>/',
        views.product_details,
        name='product_details'
    ),
]
