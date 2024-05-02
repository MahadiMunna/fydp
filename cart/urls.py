from django.urls import path
from . import views

urlpatterns = [
   path('add-to-cart/<int:fruit_id>/', views.add_to_cart, name='add_to_cart'),
   path('', views.show_cart, name='cart'),
   path('update-cart/', views.update_cart, name='update_cart'),
   path('checkout/', views.checkout, name='checkout'),
]