import imp
from applications.home.models import Home

# Procesor para recuperar telefono y correo del registro HOME

def home_contact(request):
    """ Processor para recuperar correo y telefono para mostrarlo en todos los footers

    Returns:
        dic: diccionario con clave personalizada, y el valor es la consulta a la DB
    """
    home = Home.objects.latest("created")
    
    return {
        "telefono": home.phone,
        "correo": home.contact_mail,
    }