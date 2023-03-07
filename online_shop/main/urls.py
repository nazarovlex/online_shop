from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.main, name="main"),
    path("register", views.register_request, name="register"),
    path("shops", views.shops, name="shops"),
    path("selected_store", views.selected_store, name="selected_store"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path('delete_user', views.delete_user, name='delete_user'),
    path('delete_shop', views.delete_shop, name='delete_shop'),
    path("profile_settings", views.delete_account, name="profile_settings"),
    path("user_cart", views.user_cart, name="user_cart"),
    path("add_to_user_cart", views.add_to_user_cart, name="add_to_user_cart"),
    path("remove_from_user_cart", views.remove_from_user_cart, name="remove_from_user_cart"),
    path("shop_items", views.shop_items, name="shop_items"),
    path("remove_shop_item", views.remove_shop_item, name="remove_shop_item"),
    path("shop_new_item", views.add_item_to_shop, name="shop_new_item"),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
