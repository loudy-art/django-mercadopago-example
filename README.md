# django-mercadopago-example
example app using Django-Payments with MercadoPago provider

since i didn't find any real life examples using Django-Payments with MercadoPago, i'm uploading what i learned in my last project. 

the app catches Django-Payment's payment.status and stores users form-data into a session, after payment is 'confirmed' it will send an email to your client and your buyer. 
