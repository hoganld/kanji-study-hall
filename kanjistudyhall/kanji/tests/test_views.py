import unittest

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase

from kanji import views
from kanji.models import Kanji, KanjiCard, KanjiCardCollection

User = get_user_model()

class KanjiCardCollectionTest(TestCase):

    def test_wrong_user_cannot_view_collection(self):
        password='pass'
        good = User.objects.create_user(username="goodguy", password=password)
        bad = User.objects.create_user(username="baddie", password=password)
        collection = KanjiCardCollection.objects.create(owner=good, name='a')
        self.client.login(username=bad.username, password=password)
        response = self.client.get(
            reverse('get_collection', kwargs={'slug': collection.name}))
        self.assertEqual(response.status_code, 404)

    def test_wrong_user_cannot_modify_collection(self):
        password='pass'
        good = User.objects.create_user(username="goodguy", password=password)
        bad = User.objects.create_user(username="baddie", password=password)
        collection = KanjiCardCollection.objects.create(owner=good, name='a')
        self.client.login(username=bad.username, password=password)
        response = self.client.post(
            reverse('update_collection', kwargs={'slug': collection.name,}),
            {'name': 'pwned'}
        )
        self.assertEqual(response.status_code, 404)

    def test_wrong_user_cannot_delete_collection(self):
        password='pass'
        good = User.objects.create_user(username="goodguy", password=password)
        bad = User.objects.create_user(username="baddie", password=password)
        collection = KanjiCardCollection.objects.create(owner=good, name='a')
        self.client.login(username=bad.username, password=password)
        response = self.client.delete(
            reverse('delete_collection', kwargs={'slug': collection.name})
        )
        self.assertEqual(response.status_code, 404)

    def test_get_collections_200(self):
        password = 'pass'
        owner = User.objects.create_user(username="goodguy", password=password)
        collection = KanjiCardCollection.objects.create(owner=owner, name='a')
        self.client.login(username=owner.username, password=password)
        response = self.client.get(reverse('get_collections'))
        self.assertEqual(response.status_code, 200)

    def test_get_collections_data(self):
        password = 'pass'
        owner = User.objects.create_user(username="goodguy", password=password)
        collection = KanjiCardCollection.objects.create(owner=owner, name='a')
        self.client.login(username=owner.username, password=password)
        response = self.client.get(reverse('get_collections'))
        self.assertIn(collection, response.context['collections'])

    def test_get_collections_returns_only_user_data(self):
        password = 'pass'
        owner = User.objects.create_user(username="goodguy", password=password)
        otherguy = User.objects.create_user(username="ty", password=password)
        coll1 = KanjiCardCollection.objects.create(owner=owner, name='a')
        coll2 = KanjiCardCollection.objects.create(owner=otherguy, name='b')
        self.client.login(username=owner.username, password=password)
        response = self.client.get(reverse('get_collections'))
        self.assertNotIn(coll2, response.context['collections'])

    def test_owner_gets_200(self):
        password = 'pass'
        owner = User.objects.create_user(username="goodguy", password=password)
        collection = KanjiCardCollection.objects.create(owner=owner, name='a')
        self.client.login(username=owner.username, password=password)
        response = self.client.get(
            reverse('get_collection', kwargs={'slug': collection.name}))
        self.assertEqual(response.status_code, 200)

    def test_owner_gets_collection_data(self):
        password = 'pass'
        owner = User.objects.create_user(username="goodguy", password=password)
        collection = KanjiCardCollection.objects.create(owner=owner, name='a')
        self.client.login(username=owner.username, password=password)
        response = self.client.get(
            reverse('get_collection', kwargs={'slug': collection.name}))
        self.assertEqual(response.context['collection'], collection)
        
    def test_modify_collection(self):
        password='pass'
        good = User.objects.create_user(username="goodguy", password=password)
        collection = KanjiCardCollection.objects.create(owner=good, name='a')
        self.client.login(username=good.username, password=password)
        new_name = 'favorite_ice_create'
        response = self.client.post(
            reverse('update_collection', kwargs={'slug': collection.name,}),
            {'name': new_name}
        )
        collection.refresh_from_db()
        self.assertEqual(collection.name, new_name)

    def test_user_cannot_change_collection_owner(self):
        password='pass'
        good = User.objects.create_user(username="goodguy", password=password)
        bad = User.objects.create_user(username="baddie", password=password)
        collection = KanjiCardCollection.objects.create(owner=good, name='a')
        self.client.login(username=good.username, password=password)
        response = self.client.post(
            reverse('update_collection', kwargs={'slug': collection.name,}),
            {'owner': bad.id}
        )
        collection.refresh_from_db()
        self.assertEqual(collection.owner, good)

    @unittest.skip
    def test_delete_collection(self):
        pass

    @unittest.skip
    def test_get_nonexistant_collection(self):
        pass

    @unittest.skip
    def test_modify_nonexistant_collection(self):
        pass

    @unittest.skip
    def test_delete_nonexistant_collection(self):
        pass

    @unittest.skip
    def test_add_invalid_card(self):
        pass

    @unittest.skip
    def test_modify_card_invalidly(self):
        pass


