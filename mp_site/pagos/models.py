from payments import PurchasedItem
from payments.models import BasePayment
        
class Payment(BasePayment):
    def get_failure_url(self):
        return "localhost:8000/pago-rechazado" #replace with your success/rejected URL's

    def get_success_url(self):
        return "localhost:8000/pago-exitoso"

    def get_purchased_items(self):
        yield PurchasedItem(
            name=self.description,
            sku="BSKV",
            quantity=1,
            price=self.total,
            currency=self.currency,
        )
        