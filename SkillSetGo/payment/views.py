from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse,\
                             get_object_or_404
from shop.models import Order
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def enviar_correo(total, items, order_id, email, code):
    subject = 'Your SkillSetGo Order Details'
    from_email = 'skillsetgo4@gmail.com'
    to_email = [email]
    order = get_object_or_404(Order, pk=order_id)

    context = {
        'total': total,
        'items': items,
        'order': order,
        'code': code,
        }

    html_message = render_to_string('payment/completed.html', context)
    plain_message = strip_tags(html_message)

    send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

def payment_process(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_id = order.id
    items = order.orderitem_set.all()

    if request.method == 'POST':
        success_url = request.build_absolute_uri(f'/payment/completed/{order.id}/')
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        # Stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        # Add order items to the Stripe checkout session
        for item in items:
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.product.price * Decimal('100')),
                    'currency': 'eur',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })

        # Create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)

        # Redirect to Stripe payment form
        return redirect(session.url, code=303)
    else:
        return render(request, "payment/process.html", locals())

def payment_completed(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    items = order.orderitem_set.all()
    code = order.code
    total = order.get_cart_total
    email = order.customer.emails
    enviar_correo(total, items, order_id, email, code)
    # Decrement product quota for each item in the order
    for item in items:
        product = item.product
        product.quota -= 1
        product.save()

    # Mark Order as complete, so that user gets assigned a new order with an empty cart
    order.completed = True
    order.save()
    return render(request, 'payment/completed.html', {'order': order,
        'items': items, 'code': code})
    

def payment_canceled(request):
    return render(request, 'payment/canceled.html')