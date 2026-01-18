from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)
def audit_log_view(request):
    log_entries = []

    try:
        with open('logs/security.log', 'r') as file:
            log_entries = file.readlines()
    except FileNotFoundError:
        log_entries = ["No logs available."]

    return render(
        request,
        'logs/audit_log.html',
        {'logs': log_entries}
    )
