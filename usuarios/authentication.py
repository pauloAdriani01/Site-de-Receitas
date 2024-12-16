### CÓDIGO PARA MUDAR O MODO PADRÃO QUE O DJANGO ENXERGA OS USUÁRIOS (NESSE CASO, ELE VAI SUBSTITUIR O USERNAME PELO EMAIL DA PESSOA)

from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):

    def authenticate(self, request, username = None, password = None, **kwargs):
        if username is None: 
            username = kwargs.get('email')
        try:

            #Tenta pegar o usuário pelo email
            user = User.objects.get(email=username)

            #Checa se a senha está correta
            if user.check_password(password):
                return user
        
        except User.DoesNotExist:
            return None
    