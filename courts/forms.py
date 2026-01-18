from django.forms import ModelForm
from .models import Court

class CourtForm(ModelForm):
    class Meta:
        model = Court
        fields = "__all__"