from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from unittest import skip

from .models import Kanji, KanjiCard, KanjiCardCollection

User = get_user_model()

class KanjiTest(TestCase):

    def test_create_kanji_fails_without_character(self):
        kanji = Kanji()
        kanji.heisig_index = 13
        kanji.keyword = 'month'
        kanji.character = None
        with self.assertRaises(IntegrityError):
            kanji.save()

    def test_create_kanji_fails_without_keyword(self):
        kanji = Kanji()
        kanji.heisig_index = 13
        kanji.keyword = None
        kanji.character = '月'
        with self.assertRaises(IntegrityError):
            kanji.save()

    def test_create_kanji_fails_without_heisig_index(self):
        kanji = Kanji()
        kanji.heisig_index = None
        kanji.keyword = 'month'
        kanji.character = '月'
        with self.assertRaises(IntegrityError):
            kanji.save()

    def test_create_kanji_fails_with_duplicate_character(self):
        kanji = Kanji(character='月', keyword='month', heisig_index=13)
        kanji.save()
        dup = Kanji(character='月', keyword='neck', heisig_index=70)
        with self.assertRaises(IntegrityError):
            dup.save()

    def test_create_kanji_fails_with_duplicate_keyword(self):
        kanji = Kanji(character='月', keyword='month', heisig_index=13)
        kanji.save()
        dup = Kanji(character='首', keyword='month', heisig_index=70)
        with self.assertRaises(IntegrityError):
            dup.save()

    def test_create_kanji_fails_with_duplicate_heisig_index(self):
        kanji = Kanji(character='月', keyword='month', heisig_index=13)
        kanji.save()
        dup = Kanji(character='首', keyword='neck', heisig_index=13)
        with self.assertRaises(IntegrityError):
            dup.save()

    def test_create_kanji_fails_with_empty_character(self):
        kanji = Kanji()
        kanji.heisig_index = 13
        kanji.keyword = 'month'
        kanji.character = ''
        with self.assertRaises(ValidationError):
            kanji.full_clean()

    def test_create_kanji_fails_with_empty_keyword(self):
        kanji = Kanji()
        kanji.heisig_index = 13
        kanji.keyword = ''
        kanji.character = '月'
        with self.assertRaises(ValidationError):
            kanji.full_clean()

    def test_create_kanji_fails_with_multiple_characters(self):
        kanji = Kanji()
        kanji.heisig_index = 13
        kanji.keyword = 'month'
        kanji.character = '月光'
        with self.assertRaises(ValidationError):
            kanji.full_clean()

    def test_create_kanji_fails_with_negative_heisig_index(self):
        kanji = Kanji()
        kanji.heisig_index = -1
        kanji.keyword = 'month'
        kanji.character = '月'
        with self.assertRaises(ValidationError):
            kanji.full_clean()

    def test_create_valid_kanji_succeeds(self):
        kanji = Kanji()
        kanji.heisig_index = 13
        kanji.keyword = 'month'
        kanji.character = '月'
        # should not raise
        kanji.save()
        kanji.full_clean()

        
class KanjiCardTest(TestCase):

    def test_create_card_fails_without_kanji(self):
        owner = User.objects.create()
        collection = KanjiCardCollection(owner=owner, name='default')
        collection.save()
        card = KanjiCard()
        card.mnemonic = 'waxing moon'
        card.collection = collection
        with self.assertRaises(IntegrityError):
            card.save()

    def test_create_card_fails_without_mnemonic(self):
        owner = User.objects.create()
        collection = KanjiCardCollection(owner=owner, name='default')
        collection.save()
        card = KanjiCard()
        kanji = Kanji.objects.create(character='日',
                                      keyword='day',
                                      heisig_index=12)
        card.kanji = kanji
        card.mnemonic = None
        card.collection = collection
        with self.assertRaises(IntegrityError):
            card.save()

    def test_create_card_fails_without_collection(self):
        owner = User.objects.create()
        card = KanjiCard()
        kanji = Kanji.objects.create(character='日',
                                      keyword='day',
                                      heisig_index=12)
        card.kanji = kanji
        card.mnemonic = None
        with self.assertRaises(IntegrityError):
            card.save()

    def test_create_card_with_empty_mnemonic(self):
        owner = User.objects.create()
        collection = KanjiCardCollection(owner=owner, name='default')
        collection.save()
        card = KanjiCard()
        kanji = Kanji.objects.create(character='日',
                                      keyword='day',
                                      heisig_index=12)
        card.kanji = kanji
        card.mnemonic = ''
        card.collection = collection
        with self.assertRaises(ValidationError):
            card.full_clean()

    @skip
    def test_review_card_score_too_low_ignored(self):
        pass

    @skip
    def test_review_card_score_too_high_ignored(self):
        pass

    @skip
    def test_two_card_same_efactor_same_score_reschedule_together(self):
        pass

    @skip
    def test_two_card_different_efactor_same_score_reschedule_separately(self):
        pass
    
    @skip
    def test_two_card_same_efactor_different_score_reschedule_separately(self):
        pass

    @skip
    def test_review_total_increments_correctly(self):
        pass
    

class KanjiCardCollectionTest(TestCase):

    def test_add_card_with_duplicate_kanji_fails(self):
        owner = User.objects.create()
        collection = KanjiCardCollection(owner=owner, name="default")
        collection.save()
        kanji = Kanji.objects.create(character='月',
                                     keyword='month',
                                     heisig_index=13)
        card1 = KanjiCard.objects.create(kanji=kanji,
                                         mnemonic='waxing moon',
                                         collection=collection)
        with self.assertRaises(IntegrityError):
            card2 = KanjiCard.objects.create(kanji=kanji,
                                             mnemonic='waning moon',
                                             collection=collection)

    def test_add_card_with_duplicate_mnemonic_fails(self):
        owner = User.objects.create()
        collection = KanjiCardCollection(owner=owner, name="default")
                                         
        collection.save()
        kanji1 = Kanji.objects.create(character='日',
                                     keyword='day',
                                     heisig_index=12)
        kanji2 = Kanji.objects.create(character='月',
                                     keyword='month',
                                     heisig_index=13)
        card1 = KanjiCard.objects.create(kanji=kanji1,
                                         mnemonic='waxing moon',
                                         collection=collection)
        with self.assertRaises(IntegrityError):
            card2 = KanjiCard.objects.create(kanji=kanji2,
                                             mnemonic='waxing moon',
                                             collection=collection)
        
    def test_add_two_different_cards_succeeds(self):
        owner = User.objects.create()
        collection = KanjiCardCollection(owner=owner, name="default")
        collection.save()
        kanji1 = Kanji.objects.create(character='日',
                                      keyword='day',
                                      heisig_index=12)
        kanji2 = Kanji.objects.create(character='月',
                                      keyword='month',
                                      heisig_index=13)
        card1 = KanjiCard.objects.create(kanji=kanji1,
                                         mnemonic='midday sun',
                                         collection=collection)
        card2 = KanjiCard.objects.create(kanji=kanji2,
                                         mnemonic='waxing moon',
                                         collection=collection)
        self.assertEqual(collection.kanjicard_set.count(), 2)
        
    def test_create_collection_without_name_fails(self):
        owner = User.objects.create()
        collection = KanjiCardCollection(owner=owner)
        with self.assertRaises(ValidationError):
            collection.full_clean()

    def test_create_collection_with_empty_name_fails(self):
        owner = User.objects.create()
        collection = KanjiCardCollection(owner=owner, name="")
        with self.assertRaises(ValidationError):
            collection.full_clean()

    def test_create_collection_with_existing_name_fails(self):
        owner = User.objects.create()
        KanjiCardCollection.objects.create(owner=owner, name="default")
        collection = KanjiCardCollection(owner=owner, name="default")
        with self.assertRaises(IntegrityError):
            collection.save()

    @skip
    def test_get_next_card_for_review(self):
        pass

    @skip
    def test_get_next_card_for_review_when_caught_up_returns_empty_list(self):
        pass
