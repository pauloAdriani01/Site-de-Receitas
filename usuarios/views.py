from django.views.generic import TemplateView


class loginPageView(TemplateView):
    template_name = 'loginPage.html'

class cadastrarPageView(TemplateView):
    template_name = 'cadastrarPage.html'

class editarPerfilView(TemplateView):
    template_name = 'editarPerfil.html'


#Configuração da página de cadastro para o redirecionamento até a página de edição de perfil

from django.contrib.auth import login, authenticate ###ESSES CÓDIGOS DAS BIBLIOTECAS SERVEM TANTO PARA O LOGIN QUANTO PARA O CADASTRO
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):

    #Padrões são enviados assim caso seja um GET
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
    
    #Checa se o email já existe
    if User.objects.filter(email=email).exists():
        messages.error(request, 'O e-mail já está em uso.')
        return render(request, 'cadastrarPage.html')
    
    #Criação do usuário
    usuarioNovo = User.objects.create_user(username=username, email=email, password=password)
    usuarioNovo.save()

    #Mensagem de sucesso
    messages.success(request, 'Perfil criado com sucesso. Seja bem-vindo(a) ao Site de Receitas! =)')

    #Faz o login automático após o cadastro
    login(request, usuarioNovo)

    #Redireciona até a página de login
    return redirect ('editarPerfil')

###

#Configuração para redirecionamento de volta para a homepage após o login

def loginPage(request):

    #Caso o método for o POST, ele irá pegar as informações desses campos e, então, usa-lás para autentificação 
    if request.method == 'POST':
        username = request.POST.get('nomeUsuario')
        password = request.POST.get('senhaUsuario')

        #Autentificação
        usuario = authenticate(request, username=username, password=password)
        if User is not None:
            login(request, usuario) #Loga o usuário
            messages.success(request, f'Bem-vindo(a) de volta, {usuario.username}!')
            return redirect('homePage') #Redireciona a homepage
        else:
            messages.error(request, 'Nome de usuário ou senha incorretos')

    return render(request, 'loginPage.html') #Redireciona de volta a homepage caso tenha um GET ou algum erro