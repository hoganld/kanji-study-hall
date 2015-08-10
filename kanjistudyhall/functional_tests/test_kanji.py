import unittest

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from .functionalbase import FunctionalTest
from kanji.models import Kanji, KanjiCard, KanjiCardCollection
User = get_user_model()

class KanjiCardCollectionTest(TestCase):
    """Test the access restrictions and CRUD operations for KanjiCardCollection
    objects.

    """

    def _login_user(self, username):
        password='pass'
        user = User.objects.create_user(username=username, password=password)
        self.client.login(username=user.username, password=password)
        return user

    def _create_collection(self, user, name):
        return KanjiCardCollection.objects.create(owner=user, name=name)

    def _nefarious_setup(self):
        baddie = self._login_user('badguy')
        goodie = User.objects.create_user(username="goodguy")
        collection = self._create_collection(goodie, "col")
        return collection

    def _legitimate_setup(self):
        goodie = self._login_user('goodguy')
        collection = self._create_collection(goodie, "col")
        return collection

    def test_wrong_user_cannot_view_collection(self):
        collection = self._nefarious_setup()
        response = self.client.get(
            reverse('get_collection', kwargs={'slug': collection.name}))
        self.assertEqual(response.status_code, 404)

    def test_wrong_user_cannot_modify_collection(self):
        collection = self._nefarious_setup()
        response = self.client.post(
            reverse('update_collection', kwargs={'slug': collection.name,}),
            {'name': 'pwned'}
        )
        self.assertEqual(response.status_code, 404)

    def test_wrong_user_cannot_delete_collection(self):
        collection = self._nefarious_setup()
        response = self.client.delete(
            reverse('delete_collection', kwargs={'slug': collection.name})
        )
        self.assertEqual(response.status_code, 404)

    def test_get_collections_200(self):
        collection = self._legitimate_setup()
        response = self.client.get(reverse('get_collections'))
        self.assertEqual(response.status_code, 200)

    def test_get_collections_data(self):
        collection = self._legitimate_setup()
        response = self.client.get(reverse('get_collections'))
        self.assertIn(collection, response.context['collections'])

    def test_get_collections_returns_only_user_data(self):
        owner = self._login_user('goodguy')
        otherguy = User.objects.create_user(username="ty")
        coll1 = KanjiCardCollection.objects.create(owner=owner, name='a')
        coll2 = KanjiCardCollection.objects.create(owner=otherguy, name='b')
        response = self.client.get(reverse('get_collections'))
        self.assertNotIn(coll2, response.context['collections'])

    def test_owner_gets_200(self):
        collection = self._legitimate_setup()
        response = self.client.get(
            reverse('get_collection', kwargs={'slug': collection.name}))
        self.assertEqual(response.status_code, 200)

    def test_owner_gets_collection_data(self):
        collection = self._legitimate_setup()
        response = self.client.get(
            reverse('get_collection', kwargs={'slug': collection.name}))
        self.assertEqual(response.context['collection'], collection)


    def test_modify_collection_modifies_correctly(self):
        collection = self._legitimate_setup()
        new_name = 'favorite_ice_create'
        response = self.client.post(
            reverse('update_collection', kwargs={'slug': collection.name,}),
            {'name': new_name}
        )
        collection.refresh_from_db()
        self.assertEqual(collection.name, new_name)

    def test_modify_collection_redirects(self):
        collection = self._legitimate_setup()
        new_name = 'favorite_ice_create'
        response = self.client.post(
            reverse('update_collection', kwargs={'slug': collection.name,}),
            {'name': new_name}
        )
        collection.refresh_from_db()
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_change_collection_owner(self):
        owner = self._login_user('goodguy')
        otherguy = User.objects.create_user(username="ty")
        collection = self._create_collection(owner, 'col')
        response = self.client.post(
            reverse('update_collection', kwargs={'slug': collection.name,}),
            {'owner': otherguy.id}
        )
        collection.refresh_from_db()
        self.assertEqual(collection.owner, owner)

    def test_delete_collection_decrements_collection_count(self):
        collection = self._legitimate_setup()
        pre_count = KanjiCardCollection.objects.count()
        response = self.client.delete(
            reverse('delete_collection', kwargs={'slug': collection.name})
        )
        post_count = KanjiCardCollection.objects.count()
        self.assertEqual(pre_count, post_count + 1)

    def test_get_nonexistant_collection(self):
        user = self._login_user('user')
        response = self.client.get(
            reverse('get_collection', kwargs={'slug': 'nil'})
        )
        self.assertEqual(response.status_code, 404)

    def test_modify_nonexistant_collection(self):
        user = self._login_user('user')
        response = self.client.post(
            reverse('update_collection', kwargs={'slug': 'nil'}),
            {'name': 'null'}
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistant_collection(self):
        user = self._login_user('user')
        response = self.client.delete(
            reverse('delete_collection', kwargs={'slug': 'nil'})
        )
        self.assertEqual(response.status_code, 404)

    def test_add_collection_without_name(self):
        user = self._login_user('user')
        response = self.client.post(
            "/kanji/collections/create/",
            {'name': ''}
        )
        self.assertEqual(response.status_code, 200)

    def test_add_collection_anonymously_fails(self):
        create_url = reverse('create_kanji_collection')
        response = self.client.post(create_url, {'name': 'anonymous'})
        self.assertEqual(response.status_code, 302)

    def test_add_valid_collection_redirects_to_collection_detail_view(self):
        user = self._login_user('user')
        name = 'validcollection'
        response = self.client.post(
            "/kanji/collections/create/",
            {'name': name}
        )
        self.assertRedirects(response,
                             reverse('get_collection', kwargs={'slug': name}))


class KanjiCardTest(TestCase):

    @unittest.skip
    def test_wrong_user_cannot_create_card(self):
        pass
    
    @unittest.skip
    def test_wrong_user_cannot_view_card(self):
        pass

    @unittest.skip
    def test_wrong_user_cannot_modify_card(self):
        pass

    @unittest.skip
    def test_wrong_user_cannot_delete_card(self):
        pass

    @unittest.skip
    def test_get_card(self):
        pass

    @unittest.skip
    def test_add_card(self):
        pass
    
    @unittest.skip
    def test_modify_card(self):
        pass

    @unittest.skip
    def test_delete_card(self):
        pass

    @unittest.skip
    def test_get_nonexistant_card(self):
        pass

    @unittest.skip
    def test_modify_nonexistant_card(self):
        pass

    @unittest.skip
    def test_delete_nonexistant_card(self):
        pass

    @unittest.skip
    def test_add_card_with_empty_mnemonic(self):
        pass

    @unittest.skip
    def test_add_card_with_invalid_kanji(self):
        pass

    @unittest.skip
    def test_modify_card_with_empty_mnemonic(self):
        pass

    @unittest.skip
    def test_modify_card_with_invalid_kanji(self):
        pass

    @unittest.skip
    def test_next_review_date_tampering(self):
        pass

    @unittest.skip
    def test_efactor_tampering(self):
        pass

    @unittest.skip
    def test_modify_card_with_valid_input(self):
        pass
    

class ReviewTest(TestCase):

    @unittest.skip
    def test_wrong_user_cannot_review_cards(self):
        pass

    @unittest.skip
    def test_cannot_review_with_invalid_score(self):
        pass

    @unittest.skip
    def test_cannot_review_with_empty_score(self):
        pass

    @unittest.skip
    def test_missed_card_reviewed_at_the_end(self):
        pass
