from django import forms
from django.contrib.auth import authenticate
#
from .models import User

class UserRegisterForm(forms.ModelForm):
    """ Formulario para registro de usuarios """
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña'
            }
        )
    )

    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = (
            'email',
            'full_name',
            'ocupation',
            'genero',
            'date_birth',
        )
        widgets = {
            "email": forms.EmailInput(
                attrs = {
                    "placeholder": "Correo Electronico...",
                }
            ),
            "full_name": forms.TextInput(
                attrs = {
                    "placeholder": "Nombre Completo",
                }
            ),
            "ocupation": forms.TextInput(
                attrs = {
                    "placeholder": "Ocupacion",
                }
            ),
            "date_birth": forms.DateInput(
                attrs = {
                    "type": "date",
                }
            ),
        }
    
    def clean_password2(self):
        """ Validacion de coincidencia en contraseña """
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')


class LoginForm(forms.Form):
    """ Formulario para Login """
    email = forms.CharField(
        label='E-mail',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Correo Electronico',
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'contraseña'
            }
        )
    )

    def clean(self):
        """ Validacion de credenciales para inicio de sesion """
        cleaned_data = super(LoginForm, self).clean()
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos')
        
        return self.cleaned_data


class UpdatePasswordForm(forms.Form):
    """ Vista para cambio de password """
    email = forms.CharField(
            label='E-mail',
            required=True,
            widget=forms.TextInput(
                attrs={
                    'placeholder': 'Correo Electronico',
                }
            )
        )
    password1 = forms.CharField(
        label='Contraseña1',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Actual'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña2',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Nueva'
            }
        )
    )
    
    password3 = forms.CharField(
        label='Contraseña3',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repita Contraseña'
            }
        )
    )

    def clean(self):
        """ Valida que los datos de usuario sean correctos y la coincidencia de la nueva password """
        cleaned_data = super(UpdatePasswordForm, self).clean()
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        pass3 = self.cleaned_data['password3']
        
        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos')
        
        if (pass2 != pass3):
            raise forms.ValidationError('Las contraseñas no coinciden')
        
        return self.cleaned_data


class VerificationForm(forms.Form):
    """ Fomrulario para verificacion de identidad con codigo via Mail """
    codregistro = forms.CharField(required=True, max_length=50)
    
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)
    
    def clean_codregistro(self):
        """ Validacion del que el codigo de seguridad sea correcto """
        codigo = self.cleaned_data["codregistro"]
        
        if len(codigo) == 6:
            #Verificamos si el codigo y el id del usuario son validos
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError("El codigo de seguridad es incorrecto")
        else:
            raise forms.ValidationError("El codigo debe ser de 6 digitos")