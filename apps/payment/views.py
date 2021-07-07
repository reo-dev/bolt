from django.shortcuts import get_object_or_404, render

def payment_view(request):
    return render(
        request, 'payment/payment.html',
        {}
    )