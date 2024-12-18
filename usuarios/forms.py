#Página para o input de formulários, itens capazes de atribuir dados enviados pelo usuário

from django import forms
from django.contrib.auth.models import User
from .models import perfil

#Criação do formulário para a edição de informações do perfil

class editarPerfilForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Seu nome de usuário'
    }))

    aniversario = forms.DateField(required=False, widget=forms.FileInput(attrs={
        'type': 'date',
        'class': 'form-control'
    }))

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = perfil
        fields = ['aniversario', 'image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username

    def save(self, commit=True, user=None):
        perfil = super().save(commit=False)
        if user:
            user.username = self.cleaned_data['username']
            user.save()
        if commit:
            perfil.save()
        return perfil
        
