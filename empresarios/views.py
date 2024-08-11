from django.shortcuts import render, redirect
from .models import Empresas, Documento, Metricas
from investidores.models import PropostaInvestimento
from .forms import EmpresaForm
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Q


def cadastrar_empresa(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')

    if request.method == "GET":
        form = EmpresaForm()
        return render(request, 'cadastrar_empresa.html', {
            'form': form,
            'tempo_existencia': Empresas.tempo_existencia_choices,
            'areas': Empresas.area_choices,
        })
    elif request.method == "POST":
        form = EmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.user = request.user
            empresa.save()
            messages.add_message(request, constants.SUCCESS, 'Empresa criada com sucesso')
            return redirect('/empresarios/cadastrar_empresa')
        else:
            for field, error in form.errors.items():
                messages.add_message(request, constants.ERROR, f'{field}: {error}')
            return render(request, 'cadastrar_empresa.html', {
                'form': form,
                'tempo_existencia': Empresas.tempo_existencia_choices,
                'areas': Empresas.area_choices,
            })


def listar_empresas(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')

    query = request.GET.get('empresa')

    if query:
        empresas = Empresas.objects.filter(user=request.user).filter(Q(nome__icontains=query))
    else:
        empresas = Empresas.objects.filter(user=request.user)
    return render(request, 'listar_empresas.html', {'empresas': empresas})


def empresa(request, id):
    empresa = Empresas.objects.get(id=id)

    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, "Essa empresa não é sua")
        return redirect('/empresarios/listar_empresas/')

    if request.method == "GET":
        documentos = Documento.objects.filter(empresa=empresa)
        proposta_investimentos = PropostaInvestimento.objects.filter(empresa=empresa)
        proposta_investimentos_enviada = proposta_investimentos.filter(status='PE')
        return render(
            request,
            'empresa.html',
            {
                'empresa': empresa,
                'documentos': documentos,
                'proposta_investimentos_enviada': proposta_investimentos_enviada
            }
        )


def add_doc(request, id):
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get('titulo')
    arquivo = request.FILES.get('arquivo')
    extensao = arquivo.name.split('.')

    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, "Essa empresa não é sua")
        return redirect('/empresarios/listar_empresas/')

    if extensao[1] != 'pdf':
        messages.add_message(request, constants.ERROR, "Envie apenas PDF's")
        return redirect(f'/empresarios/empresa/{empresa.id}')

    if not arquivo:
        messages.add_message(request, constants.ERROR, "Envie um arquivo")
        return redirect(f'/empresarios/empresa/{empresa.id}')

    documento = Documento(
        empresa=empresa,
        titulo=titulo,
        arquivo=arquivo
    )
    documento.save()
    messages.add_message(request, constants.SUCCESS, "Arquivo cadastrado com sucesso")
    return redirect(f'/empresarios/empresa/{empresa.id}')


def excluir_dc(request, id):
    documento = Documento.objects.get(id=id)

    if documento.empresa.user != request.user:
        messages.add_message(request, constants.ERROR, "Esse documento não é seu")
        return redirect(f'/empresarios/empresa/{empresa.id}')

    documento.delete()
    messages.add_message(request, constants.SUCCESS, "Documento excluído com sucesso")
    return redirect(f'/empresarios/empresa/{documento.empresa.id}')


def add_metrica(request, id):
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get('titulo')
    valor = request.POST.get('valor')

    metrica = Metricas(
        empresa=empresa,
        titulo=titulo,
        valor=valor
    )
    metrica.save()

    messages.add_message(request, constants.SUCCESS, "Métrica cadastrada com sucesso")
    return redirect(f'/empresarios/empresa/{empresa.id}')
