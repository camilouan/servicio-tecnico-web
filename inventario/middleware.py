from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime


class InactivityTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = timezone.now()
            last_activity_raw = request.session.get('last_activity')

            if last_activity_raw:
                last_activity = parse_datetime(last_activity_raw)
                if last_activity is not None and timezone.is_naive(last_activity):
                    last_activity = timezone.make_aware(last_activity, timezone.get_current_timezone())

                if last_activity is not None:
                    elapsed = (now - last_activity).total_seconds()
                    if elapsed > getattr(settings, 'SESSION_INACTIVITY_TIMEOUT', 1800):
                        logout(request)
                        messages.warning(request, 'Tu sesión se cerró por inactividad. Inicia sesión nuevamente.')
                        if request.path != reverse('login'):
                            return redirect('login')

            request.session['last_activity'] = now.isoformat()

        return self.get_response(request)
