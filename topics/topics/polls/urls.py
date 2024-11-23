from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name="index"),  # Página inicial com a listagem de tópicos
    path('signup/', views.signup, name='signup'),  # Página de registro
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Página de login
    path('logout/', views.userLogout, name='logout'),  # Logout personalizado,
    path('topic/<int:topic_id>/', views.details, name="topic_detail"),  # Detalhes de um tópico
    path('create/', views.create_topic, name="create_topic"),  # Criação de tópicos
    path('edit/<int:topic_id>/', views.edit_topic, name="edit_topic"),  # Edição de tópicos
    path('delete/<int:topic_id>/', views.delete_topic, name="delete_topic"),  # Exclusão de tópicos
    path('comment/<int:topic_id>/', views.add_comment, name="add_comment"),  # Adicionar comentários
    path('comment/edit/<int:comment_id>/', views.edit_comment, name="edit_comment"),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name="delete_comment"),
]
