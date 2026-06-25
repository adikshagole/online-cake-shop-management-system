from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Order, CustomCake
from .forms import MenuItemForm, OrderForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings



def login_page(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Unauthorized User!")

    return render(request, 'auth/login_page.html')


def logout_page(request):
    logout(request)
    return redirect("login_page")


def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmed_password = request.POST.get("confirmed_password")

        if password != confirmed_password:
            messages.error(request, "Passwords don't match! Try again")
            return redirect("register_page")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register_page")

        User.objects.create_user(username=username, email=email, password=password)

        send_mail(
            subject="User Registration on Django App",
            message=f"{username} has successfully registered! Their account is on app",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )

        return redirect("login_page")

    return render(request, 'auth/register_page.html')




@login_required(login_url="login_page")
def index(request):
    return render(request, 'index.html')


def menu(request):
    items = MenuItem.objects.all().order_by('id')
    return render(request, 'menu.html', {'items': items})


def add_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = MenuItemForm()

    return render(request, 'add_item.html', {'form': form})


def edit_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)

    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = MenuItemForm(instance=item)

    return render(request, 'edit_item.html', {'form': form, 'item': item})


def delete_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('menu')

    return render(request, 'delete_item.html', {'item': item})


def about(request):
    return render(request, 'about.html')




def customize(request):
    if request.method == "POST":
        CustomCake.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            cake_type=request.POST.get('cake_type'),
            flavor=request.POST.get('flavor'),
            weight=request.POST.get('weight'),
            date=request.POST.get('date'),
            message=request.POST.get('message'),
            details=request.POST.get('details'),
        )
        return render(request, 'customize.html', {'success': True})

    return render(request, 'customize.html')



def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return render(request, 'my_orders.html', {'order': order})
    else:
        form = OrderForm()

    return render(request, 'order.html', {'form': form})



def add_to_cart(request, pk):
    item = MenuItem.objects.get(pk=pk)

    cart = request.session.get('cart', [])

    # check if already exists
    for i in cart:
        if i['id'] == item.id:
            i['qty'] += 1
            break
    else:
        cart.append({
            'id': item.id,
            'name': item.name,
            'price': float(item.price),
            'qty': 1
        })

    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart_items = request.session.get('cart', [])

    total = 0
    for item in cart_items:
        item['item_total'] = item['price'] * item['qty']
        total += item['item_total']

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })
def order(request):
    cart_items = request.session.get('cart', [])

    total = sum(item['price'] * item['qty'] for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()


            request.session['cart'] = []

            return render(request, 'my_orders.html', {
                'order': order,
                'cart_items': cart_items,
                'total': total
            })

    else:
        form = OrderForm()

    return render(request, 'order.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total
    }) 


def update_quantity(request, pk, action):
    cart = request.session.get('cart', [])

    for item in cart:
        if item['id'] == pk:
            if action == 'increase':
                item['qty'] += 1
            elif action == 'decrease' and item['qty'] > 1:
                item['qty'] -= 1
            break

    request.session['cart'] = cart
    return redirect('cart')




def remove_item(request, pk):
    cart = request.session.get('cart', [])

    cart = [item for item in cart if item['id'] != pk]

    request.session['cart'] = cart
    return redirect('cart')       