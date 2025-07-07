from .models import RedSocial

def redes_sociales(request):
    return {
        'redes': RedSocial.objects.all()
    }
