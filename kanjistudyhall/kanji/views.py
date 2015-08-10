from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)

from braces.views import LoginRequiredMixin

from .models import KanjiCardCollection, KanjiCard
from .forms import KanjiCardCollectionForm


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


class KanjiCardCollectionCreateView(LoginRequiredMixin, CreateView):
    model = KanjiCardCollection
    template_name = 'kanji/create_collection.html'
    slug_field = 'name'
    form_class = KanjiCardCollectionForm

    def get_success_url(self):
        return reverse_lazy('get_collection', kwargs={'slug': self.object.name})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(KanjiCardCollectionCreateView, self).form_valid(form)


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

    def get_success_url(self):
        return reverse_lazy('get_collection', kwargs={'slug': self.object.name})
    
    def get_queryset(self):
        return KanjiCardCollection.objects.filter(owner=self.request.user)
