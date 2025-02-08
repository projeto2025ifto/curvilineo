from django.urls import path
from . import views

urlpatterns = [
    # Página de Informes
    path('informes/', views.informes, name='informes'),
    
    # URLs para Links
    path('link/list/', views.link_list, name='link_list'),
    path('link/create/', views.link_create, name='link_create'),
    path('link/<int:link_id>/', views.link_detail, name='link_detail'),
    path('link/<int:link_id>/edit/', views.link_update, name='link_update'),
    path('link/<int:link_id>/delete/', views.link_delete, name='link_delete'),
    
    # URLs para Banners
    path('banner/list/', views.banner_list, name='banner_list'),
    path('banner/create/', views.banner_create, name='banner_create'),
    path('banner/<int:pk>/edit/', views.banner_update, name='banner_update'),
    path('banner/<int:pk>/delete/', views.banner_delete, name='banner_delete'),
]
