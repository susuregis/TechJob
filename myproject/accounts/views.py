from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import IntegrityError
from .models import CustomUser, Skill, Project, Portfolio, Message

def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not username or not password or not email or not user_type:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe.')
            return redirect('register')

        try:
            if user_type == 'freelancer':
                cpf = request.POST.get('cpf')
                if not cpf:
                    messages.error(request, 'CPF é obrigatório para freelancers.')
                    return redirect('register')
                user = CustomUser.objects.create_user(username=username, password=password, email=email, is_freelancer=True, cpf=cpf)
            elif user_type == 'company':
                company_name = request.POST.get('company_name')
                cnpj = request.POST.get('cnpj')
                if not company_name or not cnpj:
                    messages.error(request, 'Nome da empresa e CNPJ são obrigatórios para empresas.')
                    return redirect('register')
                user = CustomUser.objects.create_user(username=username, password=password, email=email, is_company=True, company_name=company_name, cnpj=cnpj)

            user.save()
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('home')

        except IntegrityError:
            messages.error(request, 'Ocorreu um erro com seu registro. Tente novamente.')
            return redirect('register')

    return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')

    return render(request, 'login.html')


def home(request):
    projetos = Project.objects.all()
    return render(request, 'home.html', {'projetos': projetos})


def projetos(request):
    return render(request, 'projetos.html')


def perfil(request):
    user = request.user
    return render(request, 'perfil.html', {'user': user})


def edit_profile(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_description = request.POST.get('description')
        new_profile_picture = request.FILES.get('profile_picture')

        if CustomUser.objects.filter(username=new_username).exclude(id=request.user.id).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
            return redirect('edit_profile')

        user = request.user
        user.username = new_username
        user.description = new_description
        if new_profile_picture:
            user.profile_picture = new_profile_picture
        user.save()

        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')

    return render(request, 'edit_profile.html', {'user': request.user})


def portfolio(request):
    user_portfolios = Portfolio.objects.filter(user=request.user)
    return render(request, 'portfolio.html', {'portfolios': user_portfolios})


def portfolios(request):
    if request.user.is_authenticated:
        portfolios = request.user.portfolios.all()
        return render(request, 'portfolio.html', {'portfolios': portfolios})
    else:
        return render(request, 'portfolio.html', {'portfolios': []})


def add_portfolio(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if title and description:
            Portfolio.objects.create(user=request.user, title=title, description=description)
            messages.success(request, 'Portfólio adicionado com sucesso!')
            return redirect('portfolio')

        messages.error(request, 'Por favor, preencha todos os campos.')

    return render(request, 'add_portfolio.html')


def edit_skills(request):
    user = request.user

    if request.method == 'POST':
        skill_name = request.POST.get('skill_name')
        if skill_name:
            Skill.objects.create(name=skill_name, user=user)
            messages.success(request, 'Skill adicionada com sucesso!')
            return redirect('edit_skills')

    user_skills = user.skills.all()
    return render(request, 'edit_skills.html', {'user_skills': user_skills})


def send_message(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            recipient_id = request.POST.get('recipient_id')
            recipient = get_object_or_404(CustomUser, id=recipient_id)
            message_content = request.POST.get('message_content')

            if message_content:
                Message.objects.create(sender=request.user, recipient=recipient, content=message_content)
                messages.success(request, 'Mensagem enviada com sucesso!')
                return redirect('perfil')

        recipient_id = request.GET.get('recipient_id')
        recipient = get_object_or_404(CustomUser, id=recipient_id)
        return render(request, 'send_message.html', {'recipient': recipient})
    else:
        messages.error(request, 'Você precisa estar logado para enviar mensagens.')
        return redirect('login_view')


def adicionar_projeto(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')

        if titulo and descricao:
            novo_projeto = Project(titulo=titulo, descricao=descricao, usuario=request.user)
            novo_projeto.save()
            return redirect('home')

    return render(request, 'adicionar_projeto.html')


def projeto_detalhes(request, id):
    projeto = get_object_or_404(Project, id=id)
    return render(request, 'projetos/projeto_detalhes.html', {'projeto': projeto})
