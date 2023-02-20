from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path("", views.main, name="main"),
                  path("register", views.register_request, name="register"),
                  path("login", views.login_request, name="login"),
                  path("logout", views.logout_request, name="logout"),
                  path('delete_account', views.delete_user, name='delete_user'),
                  path("profile_settings", views.profile_settings, name="profile_settings"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
