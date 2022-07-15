from django.contrib import admin
from django.urls import path, include
from base import views as base_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # authentication urls
    path("login/", base_views.LoginPageView.as_view(), name="login"),
    path("logout/", base_views.Logout.as_view(), name="logout"),
    # path("signup/", base_views.SignupView.as_view(), name="signup"),
    path("signup/", base_views.signup, name="signup"),

    
    # chat urls
    path("", include("chat.urls", namespace="")),
]
 