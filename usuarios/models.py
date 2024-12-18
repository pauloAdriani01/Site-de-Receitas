#Configuração para a insercção de imagem ao usuário (user padrão do django não vem com essa determinada função)
#A instalação do pillow é necessária 

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='padrao.png', upload_to='fotoPerfil')
    aniversario = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
#Sinal para criar um perfil ao criar um usuário
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def salvar_perfil(sender, instance, **kwargs):
    instance.perfil.save()

