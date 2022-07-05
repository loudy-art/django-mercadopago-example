from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from payments import RedirectNeeded
from payments import get_payment_model
from pagos.forms import TestPaymentForm
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

# Index site
def index(request):
    return TemplateResponse(request, "pagos/index.html")


# This function is provided by Django-Payments
# it generates a payment_id once form is validated and submitted
def payment_details(request, payment_id):

    payment = get_object_or_404(get_payment_model(), id=payment_id)
    request.session[
        "payment_id"
    ] = payment_id  # will be used to validate payment.status later
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(
        request, "pagos/payment.html", {"form": form, "payment": payment}
    )


# Function called once payment is done via our payment provider
def payment_success(request):

    # Retreiving payment status from payment_id previously stored in session
    payment_id = request.session["payment_id"]
    payment = get_object_or_404(get_payment_model(), pk=payment_id)
    status = payment.status

    # User data + mail setup
    name = request.session["name"]
    apellido = request.session["apellido"]
    buyer_email = request.session["email"]
    phone = request.session["phone"]
    phone_final = str(phone)
    from_email = settings.EMAIL_HOST_USER

    subject_welcome = "¡Bienvenidxs a mi_proyecto!"
    subject_client_info = 'Nuevo pago desde la web'

    html_message_welcome = render_to_string('pagos/bienvenidx.html', {'name': name}) #You can pass multiple contexts so they can be used on the email template
    message =  name + " " + apellido + " acaba de pagar, este es su email: " + buyer_email + " este es su numero: " + phone_final

    #Basic info about how send_mail works
    #send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    if status == "confirmed":

        #Sends welcome email template to client
        send_mail(subject_welcome, "¡Bienvenidx a mi_proyecto! gracias por tu compra", from_email, [buyer_email], html_message=html_message_welcome)

        #Sends email with client's info to our provider 
        send_mail(subject_client_info, message, from_email, [from_email])

        try:
            return TemplateResponse(
                request,
                "pagos/payment_success.html",
                {
                    "email": buyer_email,
                    "email_from": from_email,
                    "name": name,
                    "payment_id": payment_id,
                    "status": status,
                },
            )
        finally:
            # Payment_id is destroyed to prevent payment-success page refreshing 
            del request.session["payment_id"]
    else:
        return TemplateResponse(request, "pagos/index.html")


# Basic templating for payment_failure status
def payment_failure(request):
    return TemplateResponse(request, "pagos/payment_failure.html")



def create_test_payment(request):
    form = TestPaymentForm(
        initial={
            "name": request.session.get("name", None),
            "number": "",
            "email": request.session.get("email", None),
            "variant": "mercadopago",
            "currency": "ARS",
            "total": "5000",
        },
        data=request.POST or None,
    )
    if request.method == "POST" and form.is_valid(): 
        # Form data is stored into a session so it can be used in payment_success
        request.session["name"] = form.cleaned_data["name"]
        request.session["apellido"] = form.cleaned_data["apellido"]
        request.session["email"] = form.cleaned_data["email"]
        request.session["phone"] = form.cleaned_data["number"]
        p = form.instance
        p.description = "Your product description"
        p.save()
        return redirect(f"/payment-details/{p.id}")
    return TemplateResponse(request, "pagos/create_payment.html", {"form": form})
