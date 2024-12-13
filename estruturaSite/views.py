from django.views.generic import TemplateView

class homePageView(TemplateView):
    template_name = 'homePage.html'

class loginPageView(TemplateView):
    template_name = 'loginPage.html'