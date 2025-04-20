from datetime import date

from django.shortcuts import render, get_object_or_404

from club.models import Article, AuditCommittee, ClubBoard, ClubInfo, Discipline


def home(request):
    return render(request, 'website/home.html', {
        'year': date.today().year,
    })


# INSTITUCIONAL

def institutional_overview(request):
    club_info = ClubInfo.objects.first()
    club_board = ClubBoard.objects.first()
    audit_committee = AuditCommittee.objects.first()

    context = {
        'club_info': club_info,
        'club_board': club_board,
        'audit_committee': audit_committee,
    }
    return render(request, 'website/institutional_overview.html', context)
    
def authorities(request):
    club_board = ClubBoard.objects.first()
    audit_committee = AuditCommittee.objects.first()

    context = {
        'club_board': club_board,
        'audit_committee': audit_committee,
    }
    return render(request, 'website/authorities.html', context)

def statute(request):
    club_info = ClubInfo.objects.first()

    context = {
        'club_info': club_info,
    }
    return render(request, 'website/statute.html', context)


# DISCIPLINAS

def disciplines(request):
    disciplines = Discipline.objects.all()
    return render(request, 'website/disciplines_overview.html', {
        'disciplines': disciplines,
        'year': date.today().year,
    })


# NOTICIAS

def articles(request):
    articles = Article.objects.all()
    return render(request, 'website/articles.html', {
        'articles': articles,
        'year': date.today().year,
    })

