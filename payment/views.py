from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
# from sslcommerz_python.payment import SSLCSession
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from .forms import BillingAddressForm, PaymentMethodForm
from .models import BillingAddress
from django.views.generic import TemplateView
from order.models import Cart, Order

# Create your views here.
class CheckoutTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
        saved_address = saved_address[0]
        form = BillingAddressForm(instance=saved_address)
        payment_method = PaymentMethodForm()
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        order_item = order_qs[0].order_items.all()
        order_total = order_qs[0].get_totals()

        context = {
            'billing_address':form,
            'payment_method':payment_method,
            'order_item':order_item,
            'order_total':order_total,
        }

        return render(request, 'checkout.html', context)
    
    def post(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
        saved_address = saved_address[0]
        form = BillingAddressForm(instance=saved_address)
        payment_obj = Order.objects.filter(user=request.user, ordered=False)[0]
        payment_form = PaymentMethodForm(instance=payment_obj)
        if request.method == 'post' or request.method == 'POST':
            form = BillingAddressForm(request.POST, instance=saved_address)
            pay_form = PaymentMethodForm(request.POST, instance=payment_obj)
            if form.is_valid() and pay_form.is_valid():
                form.save()
                pay_method = pay_form.save()
                
                if not saved_address.is_fully_filled():
                    return redirect('checkout')
                
                if pay_method.payment_method == 'Cash on delivery':
                    order_qs = Order.objects.filter(user=request.user, ordered=False)
                    order = order_qs[0]
                    order.ordered = True
                    order.orderId = order.id
                    order.paymentId = pay_method.payment_method
                    order.save()

                    cart_items = Cart.objects.filter(user=request.user, purchased=False)
                    for item in cart_items:
                        item.purchased = True
                        item.save()
                    
                    return redirect('home')
        else:
            return redirect('home')



# store_id = 'fruit663233e40ff3a'
# store_pass = 'fruit663233e40ff3a@ssl'
# mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=store_pass)

# status_url = request.build_absolute_uri(reverse('status'))
# mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

# mypayment.set_product_integration(total_amount=Decimal('20.20'), currency='BDT', product_category='clothing', product_name='demo-product', num_of_item=2, shipping_method='YES', product_profile='None')

# @csrf_exempt
# def sslc_status(request):
#     if request.method == 'post' or request.method == 'POST':
#         payment_data = request.POST
#         print(payment_data)


# def sslc_complete(request, val_id,tran_id):
#     pass