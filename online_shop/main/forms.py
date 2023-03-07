from django.forms import ModelForm, NumberInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput, ImageField, FileInput
from .models import Items
from django import forms


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewItemForm(ModelForm):
    class Meta:
        model = Items

        fields = ["product_name", "price", "img"]

        widgets = {
            "product_name": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Name of product"
            }),

            "price": NumberInput(attrs={
                "placeholder": "Input price",
                'class': 'form-control'}),
            "img": FileInput(attrs={
                "upload_to": f"'main/static/main/img'"
            })
        }
