from django import forms

from .models import KanjiCardCollection

class KanjiCardCollectionForm(forms.ModelForm):
    name = forms.CharField(max_length=50, min_length=1)

    class Meta:
        model = KanjiCardCollection
        fields = ['name']
