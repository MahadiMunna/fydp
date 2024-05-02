from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from fruits.models import FruitModel
from .forms import CheckoutForm

# Create your views here.

def add_to_cart(request, fruit_id):
    fruit = get_object_or_404(FruitModel, id=fruit_id)
    cart = request.session.get('cart', {})
    item_id = str(fruit.id)  # Convert id to string to avoid issues with JSON serialization

    if item_id in cart:
        cart[item_id]['quantity'] += 1
        messages.success(request,f'{fruit.name} Successfully added to cart!')
    else:
        cart[item_id] = {'price': str(fruit.price), 'quantity': 1, 'name': fruit.name}
        messages.success(request,f'{fruit.name} Successfully added to cart!')

    request.session['cart'] = cart    
    referer_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer_url)

def show_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        if 'remove_item' in request.POST:
            item_id = request.POST['remove_item']
            if item_id in cart:
                del cart[item_id]

        else:
            for item_id, item_details in cart.items():
                item_quantity = request.POST.get(f'quantity_{item_id}', 0)
                if int(item_quantity) > 0:
                    cart[item_id]['quantity'] = int(item_quantity)

        request.session['cart'] = cart
        return redirect('cart')

    else:
        cart = request.session.get('cart', {})
        return render(request, 'show_cart.html', {'cart': cart})

def update_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        # Update quantities
        for item_id, item_details in cart.items():
            quantity_key = f'quantity_{item_id}'
            if quantity_key in request.POST:
                new_quantity = int(request.POST[quantity_key])
                if new_quantity > 0:
                    cart[item_id]['quantity'] = new_quantity
                else:
                    del cart[item_id]  # Remove item if quantity is zero or less
        if 'remove_item' in request.POST:
            item_id_to_remove = request.POST['remove_item']
            if item_id_to_remove in cart:
                del cart[item_id_to_remove]

        request.session['cart'] = cart
        return redirect('cart')  # Redirect to cart page after updating
    return redirect('cart') 


def checkout(request):
    cart = request.session.get('cart', {})
    total_price = 0

    for item_id, item in cart.items():
        # Convert price to float
        price = float(item['price'])
        total_price += price * item['quantity']

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process the order (e.g., save order details to the database, send confirmation email, etc.)
            # Redirect to a thank you page or order summary page
            return redirect('order_confirmation')
    else:
        form = CheckoutForm(user=request.user)
    return render(request, 'checkout.html', {'form': form, 'cart': cart, 'total_price': total_price})
