from django.urls import path
from . import views

app_name='product'
urlpatterns = [
   path('',views.IndexView.as_view(),name='index'),
   path('products/center/',views.ProductsView.as_view(),name='product_center'),
   path('products/detail/<int:p_id>/',views.ProductDetailView.as_view(),name='product_detail'),

   path('contact/',views.ContactView.as_view(),name='contact'),
]