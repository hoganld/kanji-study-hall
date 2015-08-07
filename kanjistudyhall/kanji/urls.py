from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(
        regex=r'^collections/$',
        view=views.KanjiCardCollectionListView.as_view(),
        name='collections'
    ),
    url(
        regex=r'collections/(?P<slug>\w+)/$',
        view=views.KanjiCardCollectionDetailView.as_view(),
        name='collection'
    ),
]
