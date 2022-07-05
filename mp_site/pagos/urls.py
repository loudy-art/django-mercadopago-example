from django.urls import  path
from . import views

# Basic url patterns
app_name = 'pagos'
urlpatterns = [
    path('', views.index, name='index'),
    path("payment-details/<int:payment_id>", views.payment_details),
    path("pago-exitoso", views.payment_success),
    path("pago-rechazado", views.payment_failure,),
    path("inscripcion", views.create_test_payment, name='inscripcion'),
]