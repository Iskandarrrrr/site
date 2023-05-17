from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Article
from .forms import ArticleForm, LoginForm, RegistrationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q


# Create your views here.

def index(request):
    articles = Article.objects.all()
    sort_field = request.GET.get('sort')

    if sort_field:
        articles = articles.order_by(sort_field)

    context = {
        'title': 'Главная страница',
        'articles': articles
    }
    # print(context['title'])
    return render(request, 'blog/index.html', context)


def category_page(request, category_id):
    articles = Article.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    sort_field = request.GET.get('sort')

    if sort_field:
        articles = articles.order_by(sort_field)
    context = {
        'title': f"Категория: {category.title}",
        'articles': articles
    }

    return render(request, 'blog/index.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.views += 1
    article.save()
    articles = Article.objects.all()
    articles = articles.order_by('-views')

    context = {
        'article': article,
        'articles': articles[:4]
    }

    return render(request, 'blog/article_detail.html', context)


@login_required(login_url='login')
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = Article.objects.create(**form.cleaned_data)
            article.save()
            return redirect('article', article.pk)
    else:
        form = ArticleForm()

    context = {
        'form': form,
        'title': 'Добавить статью'
    }

    return render(request, 'blog/article_form.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Вы успешно авторизовались !')
                return redirect('index')
            else:
                messages.error(request, "Не верное имя пользователя.пароль !")
                return redirect('login')
        else:
            messages.error(request, "Не верное имя пользователя.пароль !")
            return redirect('login')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'title': 'Авторизация'
    }

    return render(request, 'blog/user_login.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, "Вы вышли из аккаунта !")
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Регистрация прошла успешно. Войдите в аккаунт !")
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
        'title': 'Регистрация пользователя'
    }

    return render(request, 'blog/register.html', context)


def search_results(request):
    word = request.GET.get('q')
    articles = Article.objects.filter(
        Q(title__icontains=word) | Q(content__icontains=word)
    )
    context = {
        'articles': articles
    }

    return render(request, 'blog/index.html', context)


@login_required(login_url='login')
def update_article(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('update', id)
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
    else:
        form = ArticleForm(instance=article)

    context = {
        'title': 'Обновление статьи',
        'form': form
    }
    return render(request, 'blog/article_form.html', context)


@login_required(login_url='login')
def delete_article(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        article.delete()
        return redirect('index')
    context = {
        'article': article
    }
    return render(request, 'blog/confirm_delete.html', context)


def about_dev(request):
    return render(request, 'blog/about_dev.html')


def user_page(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'blog/user_page.html', context)
