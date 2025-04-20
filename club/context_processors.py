from .models import ClubInfo, Discipline

def club_info(request):
    try:
        info = ClubInfo.objects.first()
        return {
            'club_name': info.name,
            'club_logo': info.logo.url if info.logo else None
        }
    except ClubInfo.DoesNotExist:
        return {
            'club_name': 'Club Social y Deportivo',
            'club_logo': None
        }

def disciplines_context(request):
    disciplines = Discipline.objects.all()
    return {
        'disciplines': disciplines
    }
