from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import datetime

@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_cancelled(request):
    return render(request, 'payment/cancelled.html')


def payment_process(request):
    # What you want the button to do.
    user = request.user
    user.profile.history.ordered_items = user.profile.cart_items.all()
    user.profile.history.ordered_date = datetime.datetime.now()
    user.save()
    print(user.profile.history.ordered_items)
    cart_names = []
    amount = 0
    for obj in user.profile.cart_items.all():
        cart_names.append(obj.item.name)
        amount = amount + (obj.item.price * obj.quantity)

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": amount,
        "item_name": cart_names,
        "invoice": cart_names,
        "currency_code": 'INR',
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment:done')),
        "cancel_return": request.build_absolute_uri(reverse('payment:cancelled')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment/payment.html", context)
