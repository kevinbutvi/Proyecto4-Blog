from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, View
from django.views.generic.edit import FormView

from .forms import (LoginForm, UpdatePasswordForm, UserRegisterForm, VerificationForm)
#
from .functions import code_generator
from .models import User




class UserRegisterView(FormView):
    """ Vista para Registro de nuevo usuario. Requiere autenticacion con codigo de validacion por email """
    
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users_app:user-login')
    
    def form_valid(self, form):
        #
        # Generamos codigo de verificacion
        codigo = code_generator()
        # Se guarda la instancia de USUARIO en dicha variable para poder manipular el ID y poder enviarlo por url para hacer la validacion del codigo de seguridad
        usuario = User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['full_name'],
            form.cleaned_data['password1'],
            ocupation=form.cleaned_data['ocupation'],
            genero=form.cleaned_data['genero'],
            date_birth=form.cleaned_data['date_birth'],
            codregistro = codigo,
        )

        # Enviar el codigo al email del usuario se usa 'send_email'
        asunto = "Confirmacion de usuario"
        mensaje = "Codigo de Verificacion: " + codigo
        email_remitente = "developertest.kevin@gmail.com"
        #
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data["email"],])
        # Redirigir a pantalla de validacion
        
        return(HttpResponseRedirect(reverse(
            "users_app:user-verification",
            kwargs={"pk": usuario.id}
            )))


class CodVerificationView(FormView):
    """ Clase de verificacion de usuario"""
    
    template_name = "users/verification.html"
    form_class = VerificationForm
    success_url = reverse_lazy("users_app:user-login")
    
    def get_form_kwargs(self):
        """ Funcion para obtener Kwargs y poder utilizarlos como validacion en el FORM """
        kwargs = super(CodVerificationView, self).get_form_kwargs()
        kwargs.update({
            "pk": self.kwargs["pk"]
        })
        return (kwargs)

    def form_valid(self, form):
        User.objects.filter(
            id = self.kwargs["pk"]
        ).update(is_active = True)
        return super(CodVerificationView, self).form_valid(form)


class LoginUser(FormView):
    """ Vista de Login """
    
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('favoritos_app:perfil')

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):
    """ Vista de cierre de sesion """
    
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )


class UpdatePasswordView(LoginRequiredMixin, FormView):
    """ Vista para cambio de password """
    
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            email=usuario.email,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)
