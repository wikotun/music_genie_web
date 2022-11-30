from django.forms import ModelForm
from django.forms import ModelForm, TextInput, NumberInput,FileInput
from .models import Artist, Song
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Column, Layout, Row,
)


class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = "__all__"

        widgets = {
            'name': TextInput(attrs={'required': True, 'class': "form-control", 'placeholder': 'Artist Name'}),
            'age': NumberInput(attrs={'class': "form-control", 'placeholder': 'Age'}),
            'nationality': TextInput(attrs={'class': "form-control", 'placeholder': 'Nationality'}),
            'website': TextInput(attrs={'required': False, 'class': "form-control", 'placeholder': 'Website'}),
            'label': TextInput(attrs={'class': "form-control", 'placeholder': 'Record Label'}),
            'image': FileInput(attrs ={'class':"img-thumbnail"})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    "image", css_class="img-thumbnail",
                ),
            ),
        )



class SongForm(ModelForm):
    class Meta:
        model = Song
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

