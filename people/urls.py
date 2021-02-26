from django.urls import path, include

from people import views
from utilities.methods import get_urls_for_views

app_name = 'people'

urlpatterns = [
    path('', include(get_urls_for_views(views))),
]
