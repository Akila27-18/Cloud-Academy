from django.urls import path
from .views import checkout, payment_success
app_name = 'payments'
urlpatterns = [
    path('checkout/<slug:slug>/', checkout, name='checkout'),
    path('success/', payment_success, name='payment_success'),
]