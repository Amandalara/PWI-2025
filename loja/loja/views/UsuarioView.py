from django.shortcuts import render, get_object_or_404, redirect
from loja.models import Usuario
from loja.forms.UserUsuarioForm import UserUsuarioForm, UserForm

def list_usuario_view(request, id=None):
    # Lista todos os usuários com perfil == 2 (exclui admins)
    usuarios = Usuario.objects.filter(perfil=2)
    context = {
        'usuarios': usuarios
    }
    return render(request, 'usuario/usuario.html', context=context, status=200)

def edit_usuario_view(request):
    usuario = get_object_or_404(Usuario, user=request.user)
    message = None

    if request.method == 'POST':
        usuarioForm = UserUsuarioForm(request.POST, instance=usuario)
        userForm = UserForm(request.POST, instance=request.user)

        email_existe = Usuario.objects.filter(
            user__email=request.POST.get('email')
        ).exclude(user__id=request.user.id).exists()

        if usuarioForm.is_valid() and userForm.is_valid() and not email_existe:
            usuarioForm.save()
            userForm.save()
            message = {'type': 'success', 'text': 'Dados atualizados com sucesso'}
            return redirect('nome_da_url_de_sucesso')
        else:
            if email_existe:
                message = {'type': 'warning', 'text': 'E-mail já usado'}
            else:
                message = {'type': 'danger', 'text': 'Dados inválidos'}
    else:
        # Aqui inicializa os formulários para GET, preenchidos com os dados atuais
        usuarioForm = UserUsuarioForm(instance=usuario)
        userForm = UserForm(instance=request.user)

    context = {
        'usuarioForm': usuarioForm,
        'userForm': userForm,
        'message': message
    }
    return render(request, 'usuario/usuario-edit.html', context=context, status=200)

