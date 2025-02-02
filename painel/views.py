from django.shortcuts import render
from django.contrib.auth.models import User
from forum.models import Sala, Categoria, Topico, Resposta, Voto  

def dashboard_view(request):
    # Contadores de usuários
    total_users = User.objects.count()
    total_egressos = User.objects.filter(groups__name="Egressos").count()
    total_visitantes = User.objects.filter(groups__name="Visitantes").count()

    # Dados das Salas, Categorias, Tópicos, Respostas e Votos
    salas_data = []
    salas = Sala.objects.all()
    for sala in salas:  
        total_categorias = sala.categorias.count()  
        total_topicos = Topico.objects.filter(categoria__sala=sala).count()  
        total_respostas = Resposta.objects.filter(topico__categoria__sala=sala).count()  
        total_votos = Voto.objects.filter(resposta__topico__categoria__sala=sala).count()  

        salas_data.append({
            'sala': sala.name,  # Corrigido para 'name' se for o nome correto do campo no modelo
            'total_categorias': total_categorias,  
            'total_topicos': total_topicos,
            'total_respostas': total_respostas,
            'total_votos': total_votos
        })

    context = {
        'total_users': total_users,
        'total_egressos': total_egressos,
        'total_visitantes': total_visitantes,
        'salas_data': salas_data,
    }
    return render(request, 'dashboard.html', context)
