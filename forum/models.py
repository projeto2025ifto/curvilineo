from django.db import models
from django.contrib.auth.models import User, Group


# Modelo para Sala
class Sala(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    grupos_permitidos = models.ManyToManyField(Group, blank=True, related_name='salas')
    usuarios_permitidos = models.ManyToManyField(User, blank=True, related_name='salas')
    publico = models.BooleanField(default=True)  # Define se é acessível a todos ou não

    def __str__(self):
        return self.name


# Modelo para Categoria (associada a Sala)
class Categoria(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='categorias')

    def __str__(self):
        return self.name


# Modelo para Tag (associada a Tópicos)
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Modelo para Tópico
class Topico(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='topicos')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, related_name="topicos", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Modelo para Resposta
class Resposta(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topico = models.ForeignKey(Topico, related_name='respostas', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    votos = models.IntegerField(default=0)  # Contador de votos

    def __str__(self):
        return f"Resposta para {self.topico.title}"


# Modelo para Voto
class Voto(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    resposta = models.ForeignKey('Resposta', on_delete=models.CASCADE, related_name='votos_relacionados')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'resposta')

    def __str__(self):
        return f"Voto de {self.user.username if self.user else 'Desconhecido'} na resposta {self.resposta.id}"