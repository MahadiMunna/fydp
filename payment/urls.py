from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.CheckoutTemplateView.as_view(), name='checkout'),
    # path('sslc/status/',views.sslc_status, name='status'),
    # path('sslc/complete/',views.sslc_complete, name='complete'),
]