from django import forms
from .models import Sala, Categoria, Topico, Resposta, Tag
from django.contrib.auth.models import User, Group

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['name', 'description', 'grupos_permitidos', 'usuarios_permitidos', 'publico']

    # Adicionando campos para selecionar usuários ou grupos
    grupos_permitidos = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), 
        required=False,
        widget=forms.CheckboxSelectMultiple(), 
        label="Grupos Permitidos"
    )
    usuarios_permitidos = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(), 
        label="Usuários Permitidos"
    )
    publico = forms.BooleanField(
        required=False,
        initial=True,
        label="Público",
        help_text="Marque para permitir que qualquer usuário tenha acesso à Sala."
    )


# Formulário para Categoria
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['name', 'description']


class TopicoForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Tags"
    )

    class Meta:
        model = Topico
        fields = ['title', 'content', 'tags']


# Formulário para Resposta
class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['content']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']