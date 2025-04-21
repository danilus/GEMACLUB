from .models import ClubInfo, Discipline


def club_info(request):
    info = ClubInfo.objects.first()
    return {
        'club_name': info.name if info else 'Nombre del Club',
        'club_logo': info.logo.url if info else '',
        # podés agregar más valores por defecto si querés
    }

def disciplines_context(request):
    disciplines = Discipline.objects.all()
    return {
        'disciplines': disciplines
    }
