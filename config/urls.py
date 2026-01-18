from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.core.exceptions import BadRequest, PermissionDenied

from accounts import views as accounts_views


# ==========================
# GLOBAL ERROR HANDLERS
# ==========================
handler400 = accounts_views.bad_request_view
handler403 = accounts_views.permission_denied_view
handler404 = accounts_views.page_not_found_view
handler500 = accounts_views.server_error_view


# ==========================
# ERROR TEST ROUTES
# ==========================
def test_400(request):
    raise BadRequest()

def test_403(request):
    raise PermissionDenied()

def test_500(request):
    raise Exception("Intentional server error")


# ==========================
# URL PATTERNS
# ==========================
urlpatterns = [
    path("", lambda request: render(request, "home.html"), name="home"),

    path("admin/", admin.site.urls),

    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),

    path("bookings/", include("bookings.urls")),
    path("courts/", include("courts.urls")),
    path("logs/", include("logs.urls")),

    # ERROR TEST
    path("test-400/", test_400),
    path("test-403/", test_403),
    path("test-500/", test_500),
]