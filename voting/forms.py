from django.forms import ModelForm
from django.forms.widgets import TextInput
from .models import KadiCandidate

class KadiCandidateForm(ModelForm):
	class Meta:
		model = KadiCandidate
		fields = '__all__'
		widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }