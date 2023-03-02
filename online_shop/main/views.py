
from .models import Items, Carts
from django.shortcuts import render, redirect
from .forms import NewUserForm, NewItemForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# class AddNewItem(CreateView):
#     model = Items
#     template_name = "main/shop_new_item.html"
#     context_object_name = "New_item"


def main(request):
    items = Items.objects.all()
    return render(request, "main/main.html", {'items': items})


def shop_items(request):
    items = Items.objects.all()
    shop = []
    for item in items:
        if str(item.shop_name) == str(request.user):
            shop.append(item.id)

    return render(request, "main/shop_items.html", {'items': items, 'shop': shop})


def add_item_to_shop(request):
    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)
        form.instance.shop_name = request.user
        if form.is_valid():
            form.save()
            return redirect("shop_items")
        else:
            messages.error(request, "Incorrect form")
    form = NewItemForm()
    return render(request, "main/shop_new_item.html", {'form': form})


def remove_shop_item(request):
    delete_item_id = request.META['QUERY_STRING'].split("=")[1]
    Items.objects.filter(id=delete_item_id).delete()
    messages.warning(request, "The item was removed from your shop!")
    return redirect("shop_items")


def user_cart(request):
    items = Items.objects.all()
    try:
        cart = (Carts.objects.get(user_id=request.user.id)).cart
    except Carts.DoesNotExist:
        cart = None
    return render(request, "main/user_cart.html", {'cart': cart, 'items': items})


def add_to_user_cart(request):
    new_item_id = request.META['QUERY_STRING'].split("=")[1]
    user = request.user.id

    existed_row = Carts.objects.filter(user_id=user).exists()
    if not existed_row:
        # Делаем когда нету человека в бд
        new_cart = Carts(user_id=user, cart=[new_item_id])
        new_cart.save()
        messages.success(request, "Product was added to your cart!")
    else:
        # Делаем когда есть человек в бд
        record = Carts.objects.get(user_id=user)

        cart_to_update = record.cart
        if new_item_id in cart_to_update:
            messages.error(request, "This item already in your cart!")
        else:
            cart_to_update.append(new_item_id)
            record.delete()

            updated_cart = Carts(user_id=user, cart=cart_to_update)
            updated_cart.save()
            messages.success(request, "Product was added to your cart!")

    return redirect("main")


def remove_from_user_cart(request):
    delete_item_id = request.META['QUERY_STRING'].split("=")[1]
    user = request.user.id

    record = Carts.objects.get(user_id=user)
    cart_to_update = record.cart

    cart_to_update.remove(delete_item_id)
    record.delete()

    record = Carts(user_id=user, cart=cart_to_update)
    record.save()
    messages.warning(request, "The item was removed from your cart!")
    return redirect("user_cart")


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if request.POST["User_Shop_Radio"] == "User":
                Group.objects.get_or_create(name="Users")
                my_group = Group.objects.get(name="Users")
                my_group.user_set.add(user)

            elif request.POST["User_Shop_Radio"] == "Shop":
                Group.objects.get_or_create(name="Shops")
                my_group = Group.objects.get(name="Shops")
                my_group.user_set.add(user)

            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main")


def delete_user(request):
    username = request.user
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == 'GET':
        try:
            u = User.objects.get(username=username)
            u.delete()
        except Exception:
            messages.info(request, "Something went wrong!")
    return redirect("main")


def profile_settings(request):
    return render(request, "main/profile_settings.html")
