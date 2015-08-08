from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from braces.views import LoginRequiredMixin

from .models import KanjiCardCollection, KanjiCard

def user_collections(request):
    
    return render(request, 'kanji/user_collections.html')


class KanjiCardCollectionListView(ListView):
    model = KanjiCardCollection
    context_object_name = 'collections'
    template_name = 'kanji/user_collections.html'

    def get_queryset(self):
        return KanjiCardCollection.objects.filter(owner=self.request.user)


class KanjiCardCollectionDetailView(LoginRequiredMixin, DetailView):
    model = KanjiCardCollection
    slug_field = 'name'
    template_name = 'kanji/collection_detail.html'
    context_object_name = 'collection'

    def get_queryset(self):
        return KanjiCardCollection.objects.filter(owner=self.request.user)


class KanjiCardCollectionDeleteView(LoginRequiredMixin, DeleteView):
    model = KanjiCardCollection
    slug_field = 'name'
    template_name = 'kanji/delete_collection.html'
    success_url = reverse_lazy('get_collections')

    def get_queryset(self):
        return KanjiCardCollection.objects.filter(owner=self.request.user)

    
class KanjiCardCollectionUpdateView(LoginRequiredMixin, UpdateView):
    model = KanjiCardCollection
    fields = ['name']
    slug_field = 'name'
    template_name = 'kanji/update_collection.html'
    success_url = reverse_lazy('get_collection', kwargs={'slug': slug_field})

    def get_queryset(self):
        return KanjiCardCollection.objects.filter(owner=self.request.user)
