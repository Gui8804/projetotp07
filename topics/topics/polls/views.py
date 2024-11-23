from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Topic, Comment
from .forms import TopicForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

class CustomLoginView(LoginView):
    template_name = 'polls/login.html'
    
# Página inicial com listagem de tópicos
@login_required(login_url='/polls/login/')  # Redireciona para o login se não autenticado
def index(request):
    topics_list = Topic.objects.all().order_by('-created_at')  # Lista de tópicos ordenados pela data de criação
    return render(request, 'polls/index.html', {'topics': topics_list})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redireciona para a página de login após o cadastro
    else:
        form = SignUpForm()

    return render(request, 'polls/signup.html', {'form': form})

# Detalhes de um tópico
@login_required(login_url='/polls/login/') 
# Detalhes de um tópico
def details(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    comments = Comment.objects.filter(topic=topic).order_by('-created_at')  # Comentários do tópico
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.topic = topic
            comment.author = request.user
            comment.save()
            return redirect('topic_detail', topic_id=topic.id)  # Redireciona para a página de detalhes do tópico
    else:
        comment_form = CommentForm()

    return render(request, 'polls/topic_detail.html', {'topic': topic, 'comments': comments, 'comment_form': comment_form})


@login_required(login_url='/polls/login/') 
def userLogout(request):
    logout(request)  # Limpa a sessão do usuário
    return redirect('login')  # Redireciona para a página de login

# Criação de um novo tópico
@login_required(login_url='/polls/login/')  # Garante redirecionamento para a página de login se não autenticado
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect('index')  # Redireciona para a página inicial com a lista de tópicos
    else:
        form = TopicForm()
    return render(request, 'polls/create_topic.html', {'form': form})

# Edição de um tópico
@login_required(login_url='/polls/login/')  # Garante redirecionamento para a página de login se não autenticado
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.user != topic.author:
        return HttpResponse("Você não tem permissão para editar este tópico.")
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = TopicForm(instance=topic)
    return render(request, 'polls/create_topic.html', {'form': form, 'topic': topic})

# Exclusão de um tópico
@login_required(login_url='/polls/login/')  # Garante redirecionamento para a página de login se não autenticado
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.user != topic.author:
        return HttpResponse("Você não tem permissão para excluir este tópico.")
    if request.method == 'POST':
        topic.delete()
        return redirect('index')  # Redireciona para a página de listagem de tópicos
    return render(request, 'polls/delete_topic.html', {'topic': topic})

# Adicionar um comentário a um tópico
@login_required(login_url='/polls/login/')  # Garante redirecionamento para a página de login se não autenticado
def add_comment(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.topic = topic
            comment.author = request.user
            comment.save()
            return redirect('topic_detail', topic_id=topic.id)  # Redireciona para a página de detalhes do tópico
    else:
        form = CommentForm()
    return render(request, 'polls/add_comment.html', {'form': form, 'topic': topic})

# Editar comentário
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    topic = comment.topic  # Obtém o tópico relacionado ao comentário
    
    if request.user != comment.author:
        return HttpResponse("Você não tem permissão para editar este comentário.")
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', topic_id=topic.id)  # Redireciona para a página de detalhes do tópico
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'polls/edit_comment.html', {'form': form, 'topic': topic})

# Excluir comentário
@login_required
def delete_comment(request, comment_id):
    # Recupera o comentário que queremos excluir
    comment = get_object_or_404(Comment, pk=comment_id)

    # Verifica se o usuário é o autor do comentário
    if request.user != comment.author:
        return HttpResponse("Você não tem permissão para excluir este comentário.")

    # Recupera o tópico associado ao comentário
    topic = comment.topic

    if request.method == 'POST':
        # Exclui o comentário
        comment.delete()
        # Redireciona para a página de detalhes do tópico
        return redirect('topic_detail', topic_id=topic.id)

    return render(request, 'polls/delete_comment.html', {'comment': comment, 'topic': topic})
