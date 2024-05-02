from django.shortcuts import render, get_object_or_404, redirect
from fruits.models import FruitModel
from .models import Cart, Order

# Create your views here.
def add_to_cart(request, pk):
    item = get_object_or_404(FruitModel, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            return redirect('home')
        else:
            order.order_items.add(order_item[0])
            return redirect('home')
    else:
        order = Order(user=request.user)
        order.save()
        order.order_items.add(order_item[0])
        return redirect('home')

def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        context = {
            'carts':carts,
            'order':order
        }
        return render(request, 'cart.html', context)
    else:
        return render(request, 'cart.html')

def remove_from_cart(request, pk):
    item = get_object_or_404(FruitModel, pk=pk)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if orders.exists():
        order = orders[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.order_items.remove(order_item)
            order_item.delete()
            return redirect('cart')
        else:
            return redirect('cart')
    else:
        return redirect('cart')

def increase_decrease(request, pk, type):
    item = get_object_or_404(FruitModel, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if type=='increase':
                if order_item.quantity >= 1:
                    order_item.quantity += 1
                    order_item.save()
                    return redirect('cart')
            elif type=='decrease':
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    return redirect('cart')
                else:
                    order.order_items.remove(order_item)
                    order_item.delete()
                    return redirect('cart')
        else:
            return redirect('cart')
    else:
        return redirect('cart')
    