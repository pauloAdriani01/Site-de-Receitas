#Define a condiguração da página de login padrão do django, usando a minha configuração

from django.contrib.auth.views import LoginView 

class loginPageView(LoginView):
    template_name = 'usuarios/loginPage.html'

    #Redireciona a página do perfil após o login
    def get_success_url(self):
        return redirect('editarPerfil')

###

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class cadastrarPageView(TemplateView):
    template_name = 'cadastrarPage.html'

class editarPerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'editarPerfil.html'


#Define a confirguração de criação do usuário utilizando o email, após isso, ele é redirecionado até a página de login

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

def register(request):
    if request.method == 'POST':

        #Novo usuário com formulário customizado (usando o email)
        email = request.POST.get('email')
        senhaUsuario = request.POST.get('senhaUsuario')
        senhaUsuarioConfirmada = request.POST.get('senhaUsuarioConfirmada')

        #Checa se as senhas estão funcionando
        if senhaUsuario != senhaUsuarioConfirmada:
            return render(request, 'cadastrarPage.html', {'erro': 'As senha não coincidem.'})

        #Cria e salva o usuário
        user = user.objects.create_user(username=email, email=email, password=senhaUsuario)
        user.save()


        #Faz o login automático após o cadastro
        login(request, user)

        #Redireciona até a página de login
        return redirect ('editarPerfil')
    
    return render(request, 'cadastrarPage.html')

###

