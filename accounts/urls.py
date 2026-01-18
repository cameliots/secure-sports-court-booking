from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),

    # User features
    path("profile/", views.profile, name="profile"),
    path("change-password/", views.change_password, name="change_password"),
]
