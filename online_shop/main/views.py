from .models import Items, Carts
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# Create your views here.
def main(request):
    data = Items.objects.all()

    return render(request, "main/main.html", {'data': data})


def user_cart(request):
    print(request.user.id)
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
