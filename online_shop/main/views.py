from .models import Items
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib.auth.models import User


# Create your views here.
def main(request):
    data = Items.objects.all()
    return render(request, "main/main.html", {'data': data})


# def registration(request):
#     return render(request, "main/register.html")

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
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


# def delete_account(request):
#     form = NewUserForm(request.POST)
#     user = form.delete(request.user.id)
#     # user_id = request.user.id
#     # user.objects.filter(id=user_id).delete()
#     return HttpResponseRedirect(reverse('index'))


def profile_settings(request):
    return render(request=request, template_name="main/profile_settings.html")


def delete_user(request):
    context = {}
    username = request.user.id
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == 'DELETE':
        try:
            user = request.user
            user.delete()
            context['msg'] = 'Bye Bye'
        except Exception as e:
            context['msg'] = 'Something went wrong!'

    else:
        context['msg'] = 'Request method should be "DELETE"!'

    return render(request, 'main/main.html', context=context)
