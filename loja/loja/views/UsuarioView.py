from loja.models import Usuario
from django.shortcuts import render
def list_usuario_view(request, id=None):
# carrega somente usuarios, não inclui os admin
    usuarios = Usuario.objects.filter(perfil=2)
    context = {
    'usuarios': usuarios
    }
    return render(request, template_name='usuario/usuario.html', context=context,
status=200)