from django.urls import path
from .views import test_court_modified

urlpatterns = [
    path('test-court-modified/', test_court_modified, name='test_court_modified'),
]