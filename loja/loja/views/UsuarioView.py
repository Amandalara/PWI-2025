from django.shortcuts import render, get_object_or_404
from loja.models import Usuario
from loja.forms.UserUsuarioForm import UserUsuarioForm, UserForm
def list_usuario_view(request, id=None):
    # carrega somente usuarios, não inclui os admin
    usuarios = Usuario.objects.filter(perfil=2)
    context = {
        'usuarios': usuarios
    }
    return render(request, template_name='usuario/usuario.html', context=context, status=200)

def edit_usuario_view(request):
    print(request.user)
    usuario = get_object_or_404(Usuario, user=request.user)
    usuarioForm = UserUsuarioForm(instance=usuario)
    userForm = UserForm(instance=request.user)
    context = {
        'usuarioForm': usuarioForm,
        'userForm': userForm
    }
    return render(request, template_name='usuario/usuario-edit.html', context=context, status=200)
