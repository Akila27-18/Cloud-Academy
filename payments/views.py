import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from courses.models import Course
from .models import Payment
from courses.models import Enrollment

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def checkout(request, slug):
    course = get_object_or_404(Course, slug=slug)
    amount = 50000  # ₹500.00 in paise

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    payment = Payment.objects.create(
        student=request.user,
        course=course,
        amount=amount/100,
        razorpay_order_id=order['id']
    )

    return render(request, "payments/checkout.html", {
        "course": course,
        "order": order,
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })



@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        payment = Payment.objects.get(razorpay_order_id=data.get("razorpay_order_id"))
        payment.razorpay_payment_id = data.get("razorpay_payment_id")
        payment.razorpay_signature = data.get("razorpay_signature")
        payment.status = "paid"
        payment.save()

        # Auto-enroll student
        Enrollment.objects.get_or_create(student=payment.student, course=payment.course)

        return render(request, "payments/success.html", {"payment": payment})
    return redirect("course_list")