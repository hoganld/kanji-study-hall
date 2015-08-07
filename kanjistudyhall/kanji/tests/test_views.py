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
            reverse('collection', kwargs={'slug': collection.name}))
        self.assertEqual(response.status_code, 404)

    @unittest.skip
    def test_wrong_user_cannot_modify_collection(self):
        password='pass'
        good = User.objects.create_user(username="goodguy", password=password)
        bad = User.objects.create_user(username="baddie", password=password)
        collection = KanjiCardCollection.objects.create(owner=good, name='a')
        self.client.login(username=bad.username, password=password)
        response = self.client.post(
            reverse('collection', args=[collection.id]),
            data={'name': 'pwned'}
        )
        self.assertEqual(response.status_code, 403)

    @unittest.skip
    def test_wrong_user_cannot_delete_collection(self):
        password='pass'
        good = User.objects.create_user(username="goodguy", password=password)
        bad = User.objects.create_user(username="baddie", password=password)
        collection = KanjiCardCollection.objects.create(owner=good, name='a')
        self.client.login(username=bad.username, password=password)
        response = self.client.delete(
            reverse('collection', args=[collection.id])
        )
        self.assertEqual(response.status_code, 403)

    @unittest.skip
    def test_get_collections(self):
        pass

    def test_owner_gets_200(self):
        password = 'pass'
        owner = User.objects.create_user(username="goodguy", password=password)
        collection = KanjiCardCollection.objects.create(owner=owner, name='a')
        self.client.login(username=owner.username, password=password)
        response = self.client.get(
            reverse('collection', kwargs={'slug': collection.name}))
        self.assertEqual(response.status_code, 200)

    @unittest.skip
    def test_owner_gets_collection_data(self):
        password = 'pass'
        owner = User.objects.create_user(username="goodguy", password=password)
        collection = KanjiCardCollection.objects.create(owner=owner, name='a')
        self.client.login(username=owner.username, password=password)
        response = self.client.get(
            reverse('collection', args=[collection.id]))
        self.assertEqual(response.context['collection'], collection)
        
    @unittest.skip
    def test_modify_collection(self):
        pass

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


class KanjiCardTest(TestCase):

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
