from django.forms import ModelForm
from django.forms import ModelForm, TextInput, NumberInput
from .models import Artist, Song
from crispy_forms.helper import FormHelper


class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = "__all__"

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()

        widgets = {
            'name': TextInput(attrs={'required': True, 'class': "form-control", 'placeholder': 'Artist Name'}),
            'age': NumberInput(attrs={'class': "form-control", 'placeholder': 'Age'}),
            'nationality': TextInput(attrs={'class': "form-control", 'placeholder': 'Nationality'}),
            'website': TextInput(attrs={'required': False, 'class': "form-control", 'placeholder': 'Website'}),
            'label': TextInput(attrs={'class': "form-control", 'placeholder': 'Record Label'})
        }


class SongForm(ModelForm):
    class Meta:
        model = Song
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()