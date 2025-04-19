from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Product  # Простой импорт
from .models import Cart, CartItem

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product')
    cart_total = sum(item.total_price for item in cart_items)

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Количество {product.title} увеличено")
    else:
        messages.success(request, f"{product.title} добавлен в корзину")

    return redirect('cart:detail')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.title
    cart_item.delete()
    messages.success(request, f"{product_name} удален из корзины")
    return redirect('cart:detail')


@login_required
def update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Количество обновлено")
    else:
        cart_item.delete()
        messages.success(request, "Товар удален из корзины")

    return redirect('cart:detail')

@login_required
def checkout(request):
    # Получаем корзину пользователя
    cart = get_object_or_404(Cart, user=request.user)

    # Очищаем корзину
    cart.items.all().delete()  # Используем 'items' вместо 'cartitem_set'

    # Добавляем сообщение об успешной покупке
    messages.success(request, "Спасибо за покупку!")

    return redirect('cart:detail')