from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from courses.models import Course, Enrollment
from .models import Payment


@login_required
def checkout(request, slug):
    """
    Show checkout page (mock payment).
    """
    course = get_object_or_404(Course, slug=slug)

    # Fixed amount for demo (₹500)
    amount = 500  

    # Create payment record
    payment = Payment.objects.create(
        student=request.user,
        course=course,
        amount=amount,
        status="pending"
    )

    return render(request, "payments/checkout.html", {
        "course": course,
        "payment": payment
    })


@login_required
def payment_success(request, payment_id):
    """
    Simulate successful payment.
    """
    payment = get_object_or_404(Payment, id=payment_id)

    # Mark payment as paid
    payment.status = "paid"
    payment.razorpay_payment_id = "FAKE_PAYMENT_ID"
    payment.razorpay_order_id = "FAKE_ORDER_ID"
    payment.razorpay_signature = "FAKE_SIGNATURE"
    payment.save()

    # Auto-enroll student
    Enrollment.objects.get_or_create(
        student=payment.student,
        course=payment.course
    )

    return render(request, "payments/success.html", {
        "payment": payment
    })
