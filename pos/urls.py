from django.urls import path, include
from pos import views
from utilities.methods import get_urls_for_views

app_name = 'pos'

urlpatterns = [
    path('', include(get_urls_for_views(views))),
    path('point-of-sale/', views.PosView.as_view(), name='pos'),
    path('sale/', views.SaleView.as_view(), name='sale_list'),
    path('sale/create/', views.SaleView.as_view(), name='sale_create'),
    path('sale/update/<int:pk>/', views.SaleView.as_view(),
         name='sale_update'),
    path('sale/delete/<str:shopping_id>/', views.SaleView.as_view(),
         name='sale_delete'),
    path('sale/invoice/<int:pk>/', views.SaleView.as_view(),
         name='sale_invoice'),

    # Purchase
    path('purchase/', views.PurchaseView.as_view(), name='purchase_list'),
    path('purchase/create/', views.PurchaseView.as_view(),
         name='purchase_create'),
    path('purchase/update/<int:pk>/', views.PurchaseView.as_view(),
         name='purchase_update'),
    path('purchase/delete/<int:pk>/', views.PurchaseView.as_view(),
         name='purchase_delete'),
    path('purchase/invoice/<int:pk>/', views.PurchaseView.as_view(),
         name='purchase_invoice'),

    # ShopSettings
    path('shop-<int:pk>-settings', views.ShopSettings.as_view(),
         name='shop_settings'),
]
