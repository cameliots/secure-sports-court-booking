import logging
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

security_logger = logging.getLogger('security')


@staff_member_required
def test_court_modified(request):
    # Simulate court modification
    security_logger.info(
        f"Court modified by admin {request.user.username}"
    )

    return HttpResponse(
        "<h1>Court Updated</h1><p>Court modification logged successfully.</p>"
    )

