from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(
        regex=r'^collections/$',
        view=views.KanjiCardCollectionListView.as_view(),
        name='get_collections'
    ),
    url(
        regex=r'^collections/create/$',
        view=views.KanjiCardCollectionCreateView.as_view(),
        name='create_kanji_collection'
    ),
    url(
        regex=r'^collections/(?P<slug>\w+)/$',
        view=views.KanjiCardCollectionDetailView.as_view(),
        name='get_collection'
    ),
    url(
        regex=r'^collections/(?P<slug>\w+)/update/$',
        view=views.KanjiCardCollectionUpdateView.as_view(),
        name='update_collection'
    ),
    url(
        regex=r'^collections/(?P<slug>\w+)/delete/$',
        view=views.KanjiCardCollectionDeleteView.as_view(),
        name='delete_collection'
    ),
]
