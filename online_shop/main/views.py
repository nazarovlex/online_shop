from .models import Items, Carts
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import sqlite3


# Create your views here.
def main(request):
    items = Items.objects.all()
    return render(request, "main/main.html", {'items': items})


def user_cart(request):
    cart = Carts.objects.filter(user_id=request.user.id)
    return render(request, "main/user_cart.html", {'cart': cart})


def add_to_user_cart(request):
    # new_item_id = int(str(request)[46:-2])
    new_item_id = request.META['QUERY_STRING'].split("=")[1]
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()
    user = request.user.id
    print(f"user id - {user}\n item - {new_item_id}")
    with connection:
        cart = connection.execute(
            """select cart from main_carts where user_id = {}""".format(user)
        )
        tmp_cart_to_update = cart.fetchone()
        if tmp_cart_to_update is None:
            # Делаем когда нету человека в бд
            cursor.execute(f"INSERT INTO main_carts (user_id, cart) VALUES ({user}, '[{new_item_id}]')")

        else:
            # Делаем когда есть человек в бд
            cart_to_update = tmp_cart_to_update[0].strip('][').split(', ')
            print(f"type - {type(cart_to_update)}  old_cart{cart_to_update}")
            cart_to_update.append(new_item_id)
            print(f"type - {type(cart_to_update)} new_cart{cart_to_update}")
            # connection.execute(f"UPDATE main_carts SET cart={cart_to_update} WHERE user_id={user}")
            # cursor.execute('UPDATE main_carts SET cart=? WHERE user_id=?', (cart_to_update, user,))
            cursor.execute('UPDATE main_carts SET cart = ? WHERE user_id = ?', (f"{cart_to_update}", user))

    items = Items.objects.all()
    cart = Carts.objects.filter(user_id=request.user.id)
    return render(request, "main/main.html", {'items': items})
    # return render(request, "main/user_cart.html", {'cart': cart})


def remove_from_user_cart(request):
    items = Items.objects.all()
    cart = Carts.objects.filter(user_id=request.user.id)
    return render(request, "main/user_cart.html", {'cart': cart})


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
        except Exception as e:
            messages.info(request, "Something went wrong!")
    return redirect("main")


def profile_settings(request):
    return render(request, "main/profile_settings.html")
