from django.shortcuts import render
from .models import Items


# Create your views here.
def main(request):
    data = Items.objects.all()
    return render(request, "main/main.html", {'data': data})
