from django.shortcuts import render

from datetime import date

from club.models import Discipline, Article


def home(request):
    return render(request, 'website/home.html', {
        'year': date.today().year,
    })

def about(request):
    return render(request, 'website/about.html', {
        'year': date.today().year,
    })

def articles(request):
    articles = Article.objects.all()
    return render(request, 'website/articles.html', {
        'articles': articles,
        'year': date.today().year,
    })

def disciplines(request):
    disciplines = Discipline.objects.all()
    return render(request, 'website/disciplines.html', {
        'disciplines': disciplines,
        'year': date.today().year,
    })