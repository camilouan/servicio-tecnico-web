from django.utils import timezone

from .models import Apartado


def admin_apartados_popup(request):
    user = getattr(request, 'user', None)

    if not user or not user.is_authenticated or not (user.is_staff or user.is_superuser):
        return {'admin_popup_summary': None}

    if not request.path.startswith('/admin'):
        return {'admin_popup_summary': None}

    estados_visibles = ['pendiente', 'confirmado']
    recientes_qs = (
        Apartado.objects.filter(estado__in=estados_visibles)
        .select_related('usuario', 'producto')
        .order_by('-fecha_apartado')[:8]
    )

    limite_nuevos = timezone.now() - timezone.timedelta(hours=24)

    return {
        'admin_popup_summary': {
            'pendientes': Apartado.objects.filter(estado='pendiente').count(),
            'confirmados': Apartado.objects.filter(estado='confirmado').count(),
            'nuevos_hoy': Apartado.objects.filter(
                estado__in=estados_visibles,
                fecha_apartado__gte=limite_nuevos,
            ).count(),
            'recientes': list(recientes_qs),
        }
    }
