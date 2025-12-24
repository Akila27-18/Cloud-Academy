from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("checkout/<slug:slug>/", views.checkout, name="checkout"),
    path("success/<int:payment_id>/", views.payment_success, name="success"),
]
