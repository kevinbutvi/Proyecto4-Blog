from django import forms

# Models
from .models import Suscribers, Contact


class SuscribersForm(forms.ModelForm):
    """Fomrulario para registro de suscritores"""

    class Meta:
        """Meta definition for Suscribersform."""

        model = Suscribers
        fields = ('email',)
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Correo electronico...",
                    }
                ),
            }


class ContactForm(forms.ModelForm):
    """ Formulario del Footer para contacto """

    class Meta:
        """Meta definition for Contactform."""

        model = Contact
        fields = ('__all__')

