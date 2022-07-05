from django import forms

from payments import get_payment_model


# Payment form, added some extra fields so we can store user data 
# into session to validate payment status/send user data through email
class TestPaymentForm(forms.ModelForm):

    name = forms.CharField()
    email = forms.EmailField()
    number = forms.IntegerField()
    apellido = forms.CharField()

    class Meta:
        model = get_payment_model()
        fields = ["name", "email", "number", "apellido", "variant", "currency", "total"]
        widgets = {
            'total': forms.TextInput(attrs={'class': 'clase_de_totales'}),
            'apellido': forms.TextInput(attrs={'id': 'apellido'})
           }

# Extra validation to prevent alternative price injection
# This validation must be updated if client decides to change price, otherwise form  will not work
    def clean(self):
        cleaned_data = self.cleaned_data
        total = cleaned_data.get('total')
        valid_list = [5000, 13000, 9000, 24000]
        if total not in valid_list:
            raise forms.ValidationError('Wrong price')
        return cleaned_data