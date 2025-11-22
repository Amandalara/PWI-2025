from django.shortcuts import render, redirect
from loja.models import Produto
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime
from django.utils import timezone
from loja.models import Produto, Fabricante, Categoria
from django.core.files.storage import FileSystemStorage
@login_required
def edit_produto_view(request, id=None):
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    print(produto)
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    context = {'produto': produto, 'fabricantes' : Fabricantes, 'categorias' : Categorias}
    context = { 'produto': produto }
    return render(request, template_name='produto/produto-edit.html', context=context,status=200)

def list_produto_view(request, id=None):
    produto = request.GET.get("produto")
    destaque = request.GET.get("destaque")
    promocao = request.GET.get("promocao")
    categoria = request.GET.get("categoria")
    fabricante = request.GET.get("fabricante")
    dias = request.GET.get("dias")
    produtos = Produto.objects.all()
    if dias is not None:
        now = timezone.now()
        now = now - timedelta(days = int(dias))
        produtos = produtos.filter(criado_em__gte=now)
    if produto is not None:
        produtos = produtos.filter(Produto__contains=produto )
    if promocao is not None:
        produtos = produtos.filter(promocao=promocao)
    if destaque is not None:
        produtos = produtos.filter(destaque=destaque)
    print(produtos)
    if categoria is not None:
        produtos = produtos.filter(categoria__Categoria=categoria)
    if fabricante is not None:
        produtos = produtos.filter(fabricante__Fabricante=fabricante)
    if id is not None:
        produtos = produtos.filter(id=id)

    context = {'produtos': produtos}
    return render(request, template_name='produto/produto.html',context=context, status=200)

def edit_produto_postback(request, id=None):
    if request.method == 'POST':
        # Salva dados editados
        id = request.POST.get("id")
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        categoria = request.POST.get("CategoriaFk")
        fabricante = request.POST.get("FabricanteFk")
        print("postback")
        print(id)
        print(produto)
        print(destaque)
        print(promocao)
        print(msgPromocao)
        try:
            obj_produto = Produto.objects.filter(id=id).first()
            obj_produto.Produto = produto
            obj_produto.destaque = (destaque is not None)
            obj_produto.promocao = (promocao is not None)
            obj_produto.fabricante = Fabricante.objects.filter(id=fabricante).first()
            obj_produto.categoria = Categoria.objects.filter(id=categoria).first()
            
            if msgPromocao is not None:
                obj_produto.msgPromocao = msgPromocao
                obj_produto.save()
                print("Produto %s salvo com sucesso" % produto)
        except Exception as e:
            print("Erro salvando edição de produto: %s" % e)
    return redirect("/produto")

def details_produto_view(request, id=None):
    produto = Produto.objects.filter(id=id).first()
    fabricantes = Fabricante.objects.all()
    categorias = Categoria.objects.all()

    context = {
        'produto': produto,
        'fabricantes': fabricantes,
        'categorias': categorias,
    }
    return render(request, template_name='produto/produto-details.html', context=context, status=200)


def delete_produto_view(request, id=None):
    produto = Produto.objects.filter(id=id).first()
    fabricantes = Fabricante.objects.all()
    categorias = Categoria.objects.all()

    context = {
        'produto': produto,
        'fabricantes': fabricantes,
        'categorias': categorias
    }
    return render(request, 'produto/produto-delete.html', context=context, status=200)


def delete_produto_postback(request, id=None):
    if request.method == 'POST':
        id = request.POST.get("id")
        produto = request.POST.get("Produto")
        print("postback-delete")
        print(id)
        try:
            Produto.objects.filter(id=id).delete()
            print("Produto %s excluido com sucesso" % produto)
        except Exception as e:
            print("Erro salvando edição de produto: %s" % e)
    return redirect("/produto")
    
def create_produto_view(request, id=None):
    if request.method == 'POST':
        nome = request.POST.get("nome")  # campo correto do model
        destaque = request.POST.get("destaque") is not None
        promocao = request.POST.get("promocao") is not None
        msgPromocao = request.POST.get("msgPromocao")
        preco = request.POST.get("preco")
        categoria_id = request.POST.get("CategoriaFk")
        fabricante_id = request.POST.get("FabricanteFk")

        try:
            obj_produto = Produto()
            obj_produto.nome = nome
            obj_produto.destaque = destaque
            obj_produto.promocao = promocao
            obj_produto.msgPromocao = msgPromocao or ""
            obj_produto.preco = preco or 0
            obj_produto.criado_em = timezone.now()
            obj_produto.alterado_em = obj_produto.criado_em

            # Relaciona Categoria e Fabricante
            if categoria_id and categoria_id != "-1":
                obj_produto.categoria = Categoria.objects.filter(id=categoria_id).first()
            if fabricante_id and fabricante_id != "-1":
                obj_produto.fabricante = Fabricante.objects.filter(id=fabricante_id).first()

            if 'image' in request.FILES:
                imagefile = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(imagefile.name, imagefile)
                obj_produto.image = filename

            obj_produto.save()
            print("Produto salvo com sucesso")
        except Exception as e:
            import traceback
            print("Erro inserindo produto:")
            traceback.print_exc()

        return redirect("/produto")
    
    # Se GET, enviar fabricantes e categorias para o form de criação
    fabricantes = Fabricante.objects.all()
    categorias = Categoria.objects.all()
    context = {
        'fabricantes': fabricantes,
        'categorias': categorias,
    }
    return render(request, template_name='produto/produto-create.html', context=context, status=200)
