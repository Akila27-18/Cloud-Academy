from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),  # <-- important
    path("logout/", views.logout_view, name="logout"),
]