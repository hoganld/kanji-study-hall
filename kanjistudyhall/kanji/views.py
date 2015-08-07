from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, View

from braces.views import LoginRequiredMixin

from .models import KanjiCardCollection, KanjiCard

def user_collections(request):
    
    return render(request, 'kanji/user_collections.html')


class KanjiCardCollectionListView(ListView):
    model = KanjiCardCollection
    pass


class KanjiCardCollectionDetailView(LoginRequiredMixin, DetailView):
    model = KanjiCardCollection
    slug_field = 'name'
    template_name = 'kanji/collection_detail.html'

    def get_queryset(self):
        return KanjiCardCollection.objects.filter(owner=self.request.user)

