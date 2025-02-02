from django import forms
from django.contrib.auth.models import User
from contas.models import UserProfile
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

#-----------------------------------------------------------------------------------------

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Usuário'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))

#-----------------------------------------------------------------------------------------

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar senha'}))
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="Selecione um grupo")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError('As senhas não coincidem.')

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if User.objects.filter(username=username).exists():
            raise ValidationError('Nome de usuário já está em uso.')
        if User.objects.filter(email=email).exists():
            raise ValidationError('E-mail já está cadastrado.')

        return cleaned_data

#-----------------------------------------------------------------------------------------

class EditProfileForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False,
        label="Biografia"
    )
    avata = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False,
        label="Foto de Perfil"
    )
    remove_avata = forms.BooleanField(
        required=False,
        label="Remover Foto de Perfil"
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': None,  # Remove o texto de ajuda
        }

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        if user_profile:
            self.fields['bio'].initial = user_profile.bio
            self.fields['avata'].initial = user_profile.avata

    def save(self, commit=True, user_profile=None):
        user = super().save(commit=False)
        if commit:
            user.save()

            if user_profile:
                user_profile.bio = self.cleaned_data.get('bio', user_profile.bio)

                # Se o campo de remover foto estiver marcado, remove a foto de perfil
                if self.cleaned_data.get('remove_avata') and user_profile.avata:
                    try:
                        user_profile.avata.delete(save=False)
                    except:
                        pass
                    user_profile.avata = None

                if not self.cleaned_data.get('remove_avata'):
                    avata = self.cleaned_data.get('avata')
                    if avata:
                        user_profile.avata = avata

                user_profile.save()
        return user

#-----------------------------------------------------------------------------------------