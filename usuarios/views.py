#Define a condiguração da página de login padrão do django, usando a minha configuração

from django.contrib.auth.views import LoginView 

class LoginPageView(LoginView):
    template_name = 'usuarios/loginPage.html'

###
