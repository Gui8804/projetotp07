from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Topic, Comment

class ForumTestCase(TestCase):
    
    def setUp(self):
        # Criação de um usuário para autenticação nos testes
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Criação de um tópico para testes
        self.topic = Topic.objects.create(
            title='Test Topic',
            description='Test Description',
            author=self.user
        )
    
    def test_create_topic(self):
        # Testando a criação de um novo tópico
        response = self.client.post(reverse('create_topic'), {
            'title': 'New Topic',
            'description': 'New Description'
        })
        self.assertEqual(response.status_code, 302)  # Verifica se foi redirecionado
        self.assertEqual(Topic.objects.count(), 2)   # Agora deve haver 2 tópicos
    
    def test_edit_topic(self):
        # Testando a edição de um tópico existente
        response = self.client.post(reverse('edit_topic', args=[self.topic.id]), {
            'title': 'Updated Topic',
            'description': 'Updated Description'
        })
        self.assertEqual(response.status_code, 302)  # Verifica se foi redirecionado
        
        # Atualiza o objeto e verifica se o título foi alterado
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.title, 'Updated Topic')
    
    def test_delete_topic(self):
        # Testando a exclusão de um tópico
        response = self.client.post(reverse('delete_topic', args=[self.topic.id]))
        self.assertEqual(response.status_code, 302)  # Verifica se foi redirecionado
        self.assertEqual(Topic.objects.count(), 0)   # Agora deve haver 0 tópicos
    
    def test_add_comment(self):
        # Testando a adição de um comentário a um tópico
        response = self.client.post(reverse('add_comment', args=[self.topic.id]), {
            'text': 'This is a test comment'
        })
        self.assertEqual(response.status_code, 302)  # Verifica se foi redirecionado
        self.assertEqual(Comment.objects.count(), 1)  # Agora deve haver 1 comentário
    
    def test_edit_comment(self):
        # Criando um comentário para testar a edição
        comment = Comment.objects.create(
            text='Original Comment',
            topic=self.topic,
            author=self.user
        )
        
        response = self.client.post(reverse('edit_comment', args=[comment.id]), {
            'text': 'Edited Comment'
        })
        self.assertEqual(response.status_code, 302)  # Verifica se foi redirecionado
        
        # Atualiza o comentário e verifica se o texto foi alterado
        comment.refresh_from_db()
        self.assertEqual(comment.text, 'Edited Comment')
    
    def test_delete_comment(self):
        # Criando um comentário para testar a exclusão
        comment = Comment.objects.create(
            text='Comment to Delete',
            topic=self.topic,
            author=self.user
        )
        
        response = self.client.post(reverse('delete_comment', args=[comment.id]))
        self.assertEqual(response.status_code, 302)  # Verifica se foi redirecionado
        self.assertEqual(Comment.objects.count(), 0)  # Deve haver 0 comentários
