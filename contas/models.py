from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import os

#-----------------------------------------------------------------------------------------

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)  # Campo para bio
    avata = models.ImageField(upload_to='ft-profile/', blank=True, null=True)  # Foto de perfil

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # Se a foto de perfil foi alterada, exclui a antiga
        if self.pk:  # Verifica se já existe uma instância salva
            old_profile = UserProfile.objects.get(pk=self.pk)
            if old_profile.avata != self.avata:
                # Se a foto foi removida, exclui a antiga
                if old_profile.avata:
                    if os.path.isfile(old_profile.avata.path):
                        os.remove(old_profile.avata.path)
        super().save(*args, **kwargs)

#-----------------------------------------------------------------------------------------