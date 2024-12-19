#Criação da View da página de edição de perfil

from django.views.generic import TemplateView

###

#Configuração da página de cadastro para o redirecionamento até a página de edição de perfil

#Os códigos da biblioteca servem tanto para o cadastro quanto para o login
from django.contrib.auth import login, authenticate 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

"""
Protocolo HTTP: protocolo para buscar recursos (como página HTML) pela web

Método GET: pega algum dado, dado na URL (usado para pegar uma informação dentro da página)
Método POST: enviar informação ao servidor, dado no body (nesse caso, o "envio"[criação] de um usuário)
"""

def register(request):

    #Padrões são enviados assim caso seja um GET, desse jeito, eu posso acessar a página de cadastro da primeira vez
    email = ''
    username = ''
    password = ''
    password_confirm = ''

    if request.method == 'POST':
        email=request.POST.get('emailUsuario')
        username=request.POST.get('nomeUsuario')
        password=request.POST.get('senhaUsuario')
        password_confirm = request.POST.get('senhaUsuarioConfirmada')

    #Checa se um dos campos não estão preenchidos
    if not username or not email or not password or not password_confirm:
        messages.error(request, 'Todos os campos devem ser preenchidos.')
        return render(request, 'cadastrarPage.html')

    #Checa se as senhas são iguais
    if password != password_confirm:
        messages.error(request, 'As senhas não coincidem.')
        return render(request, 'cadastrarPage.html')
    
    #Checa se o nome de usuário já existe
    if User.objects.filter(username=username).exists():
        messages.error(request, 'O nome de usuário já está em uso.')
        return render(request, 'cadastrarPage.html')
    
    #Checa se o email já está sendo usado
    if User.objects.filter(email=email).exists():
        messages.error(request, 'O e-mail já está em uso.')
        return render(request, 'cadastrarPage.html')
    
    #Criação do usuário
    usuarioNovo = User.objects.create_user(username=username, email=email, password=password)
    usuarioNovo.save()

    #Faz o login automático após o cadastro
    login(request, usuarioNovo)

    #Redireciona até a página de edição de perfil
    return redirect ('editarPerfil')

###

#Configuração para redirecionamento de volta para a homepage após o login

def loginPage(request):

    #Caso o método for o POST, ele irá pegar as informações desses campos e, então, usa-lás para autentificação 
    if request.method == 'POST':
        username = request.POST.get('nomeUsuario')
        password = request.POST.get('senhaUsuario')

        #Autentificação, usada a embutida no django
        usuario = authenticate(request, username=username, password=password)
        if User is not None:
            login(request, usuario) #Loga o usuário caso esteja tudo correto
            return redirect('homePage') #Redireciona a homepage
        else:
            messages.error(request, 'Nome de usuário ou senha incorretos')
    return render(request, 'loginPage.html') #Redireciona de volta a homepage caso tenha algum erro

###

#View para a permissão da visualização da página e do formulário

from django import forms
#Biblioteca de User já importada anteriormente
from .forms import editarPerfilForm
from .models import perfil

def editarPerfilView(request):
    user_profile, created = perfil.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        formulario = editarPerfilForm(request.POST, request.FILES, instance=user_profile, user=request.user)

        if formulario.is_valid():
            formulario.save(user=request.user)
            return redirect('editarPerfil') #Redireciona ao perfil
        
    else:
        formulario = editarPerfilForm(instance=user_profile, user=request.user)

    context = {
        'form': formulario,
        'profile': user_profile
    }
    return render(request, 'editarPerfil.html', context)
        
###

#Página de logout

from django.contrib.auth import logout
from django.shortcuts import redirect

def logoutPageView(request):
    logout(request)
    return redirect('homePage')
