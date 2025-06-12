from django.forms import ModelForm
from django.forms.widgets import TextInput
from .models import KadiCandidate
from cloudinary.forms import CloudinaryFileField

class KadiCandidateForm(ModelForm):
	image = CloudinaryFileField(label='Kép')
	class Meta:
		model = KadiCandidate
		fields = '__all__'
		widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }