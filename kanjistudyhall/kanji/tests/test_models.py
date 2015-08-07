import datetime

from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.utils import DataError, IntegrityError
from django.test import TestCase

from .models import Kanji, KanjiCard, KanjiCardCollection

User = get_user_model()

class KanjiTest(TestCase):

    def _create_kanji(self, index=13, keyword='month', character='月'):
        kanji = Kanji()
        kanji.heisig_index = index
        kanji.keyword = keyword
        kanji.character = character
        kanji.save()
        return kanji

    def test_create_kanji_fails_without_character(self):
        with self.assertRaises(IntegrityError):
            self._create_kanji(character=None)

    def test_create_kanji_fails_without_keyword(self):
        with self.assertRaises(IntegrityError):
            self._create_kanji(keyword=None)

    def test_create_kanji_fails_without_heisig_index(self):
        with self.assertRaises(IntegrityError):
            self._create_kanji(index=None)

    def test_create_kanji_fails_with_duplicate_character(self):
        self._create_kanji()
        with self.assertRaises(IntegrityError):
            # set index and keyword to be different, but leave char as dup
            self._create_kanji(index=70, keyword='neck')

    def test_create_kanji_fails_with_duplicate_keyword(self):
        self._create_kanji()
        with self.assertRaises(IntegrityError):
            # set index and char to be different, but leave keyword as dup
            self._create_kanji(index=70, character='首')

    def test_create_kanji_fails_with_duplicate_heisig_index(self):
        self._create_kanji()
        with self.assertRaises(IntegrityError):
            # set keyword and char to be different, but leave index as dup
            self._create_kanji(keyword='neck', character='首')

    def test_create_kanji_fails_with_empty_character(self):
        kanji = self._create_kanji(character='')
        with self.assertRaises(ValidationError):
            kanji.full_clean()

    def test_create_kanji_fails_with_empty_keyword(self):
        kanji = self._create_kanji(keyword='')
        with self.assertRaises(ValidationError):
            kanji.full_clean()

    def test_create_kanji_fails_with_multiple_characters(self):
        with self.assertRaises(DataError):
            self._create_kanji(character='月光')

    def test_create_kanji_fails_with_negative_heisig_index(self):
        with self.assertRaises(IntegrityError):
            self._create_kanji(index=-1)

    def test_create_valid_kanji_succeeds(self):
        # should not raise
        kanji = self._create_kanji()
        kanji.full_clean()

        
class KanjiCardTest(TestCase):

    def _create_collection(self):
        owner = User.objects.create()
        collection = KanjiCardCollection(owner=owner, name='default')
        collection.save()
        return collection

    def _create_kanji(self, character='日', keyword='day', index=12):
        kanji = Kanji(character=character, keyword=keyword, heisig_index=index)
        kanji.save()
        return kanji
    
    def _create_card(self,
                     mnemonic='midday sun',
                     default_collection=None,
                     default_kanji=None,
                     assign_collection=True,
                     assign_kanji=True):
        """Creates a KanjiCard. If default_collection or default_kanji params
        are given, they are used. If they are not, defaults will be 
        automatically assigned, unless assign_collection or assign_kanji
        are explicitly set to False.
        
        """
        card = KanjiCard(mnemonic=mnemonic)
        if default_collection:
            card.collection = default_collection
        elif assign_collection:
            card.collection = self._create_collection()
        if default_kanji:
            card.kanji = default_kanji
        elif assign_kanji:
            card.kanji = self._create_kanji()
        card.save()
        return card

    def test_create_card_fails_without_kanji(self):
        with self.assertRaises(IntegrityError):
            self._create_card(assign_kanji=False)

    def test_create_card_fails_without_mnemonic(self):
        with self.assertRaises(IntegrityError):
            self._create_card(mnemonic=None)

    def test_create_card_fails_without_collection(self):
        with self.assertRaises(IntegrityError):
            self._create_card(assign_collection=False)

    def test_create_card_with_empty_mnemonic(self):
        card = self._create_card(mnemonic='')
        with self.assertRaises(ValidationError):
            card.full_clean()

    def test_create_valid_card_succeeds(self):
        # should not raise
        self._create_card()
        self.assertEqual(KanjiCard.objects.count(), 1)

    def test_review_card_score_too_low_rejected(self):
        card = self._create_card()
        with self.assertRaises(ValueError):
            card.set_review_score(-1)

    def test_review_card_score_too_high_rejected(self):
        card = self._create_card()
        with self.assertRaises(ValueError):
            card.set_review_score(6)

    def test_review_score_above_3_advances_review_schedule(self):
        card = self._create_card()
        original_review = card.next_review
        card.set_review_score(4)
        card.refresh_from_db()
        self.assertTrue(original_review < card.next_review)
        
    def test_setting_review_score_below_4_schedules_review_today(self):
        card = self._create_card()
        original_review = card.next_review
        card.set_review_score(3)
        card.refresh_from_db()
        self.assertEqual(datetime.date.today(), card.next_review)
        
    def test_two_cards_same_efactor_same_score_reschedule_together(self):
        collection = self._create_collection()
        card1 = self._create_card(default_collection=collection)
        kanji = self._create_kanji(index=13, character='月', keyword='month')
        card2 = self._create_card(mnemonic='waxing moon',
                                  default_kanji=kanji,
                                  default_collection=collection)
        card1.set_review_score(4)
        card2.set_review_score(4)
        self.assertEqual(card1.next_review, card2.next_review)

    def test_two_cards_different_history_same_score_reschedule_separately(self):
        collection = self._create_collection()
        card1 = self._create_card(default_collection=collection)
        kanji = self._create_kanji(index=13, character='月', keyword='month')
        card2 = self._create_card(mnemonic='waxing moon',
                                  default_kanji=kanji,
                                  default_collection=collection)
        card1.efactor = 2.6
        card1.consecutive_correct = 6
        card1.save()
        card2.efactor = 1.8
        card2.save()
        card1.set_review_score(4)
        card2.set_review_score(4)
        self.assertTrue(card1.next_review > card2.next_review)
    
    def test_two_cards_same_history_different_score_reschedule_separately(self):
        collection = self._create_collection()
        card1 = self._create_card(default_collection=collection)
        kanji = self._create_kanji(index=13, character='月', keyword='month')
        card2 = self._create_card(mnemonic='waxing moon',
                                  default_kanji=kanji,
                                  default_collection=collection)
        card1.efactor = 2.6
        card1.consecutive_correct = 6
        card2.efactor = 2.6
        card2.consecutive_correct = 6
        card1.set_review_score(5)
        card2.set_review_score(4)
        self.assertTrue(card1.next_review > card2.next_review)


    def test_review_total_increments_correctly(self):
        card = self._create_card()
        review_total = card.total_reviews
        card.set_review_score(3)
        new_total = card.total_reviews
        self.assertEqual(review_total + 1, new_total)
    

class KanjiCardCollectionTest(TestCase):

    def _create_collection(self, name='default', assign_owner=True):
        collection = KanjiCardCollection(name=name)
        if assign_owner:
            collection.owner = User.objects.create()
        collection.save()
        return collection

    def test_add_card_with_duplicate_kanji_fails(self):
        collection = self._create_collection()
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
        collection = self._create_collection()
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
        collection = self._create_collection()
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
        with self.assertRaises(IntegrityError):
            self._create_collection(name=None)

    def test_create_collection_with_empty_name_fails(self):
        collection = self._create_collection(name='')
        with self.assertRaises(ValidationError):
            collection.full_clean()

    def test_create_collection_with_existing_name_fails(self):
        self._create_collection()
        with self.assertRaises(IntegrityError):
            # without changing the default name, this should raise
            self._create_collection()

    def test_get_next_card_for_review(self):
        collection = self._create_collection()
        kanji1 = Kanji.objects.create(character='日',
                                      keyword='day',
                                      heisig_index=12)
        card1 = KanjiCard.objects.create(kanji=kanji1,
                                         mnemonic='midday sun',
                                         collection=collection)
        self.assertEqual(collection.next_scheduled_card(), card1)

    def test_get_next_card_for_review_when_caught_up_returns_none(self):
        collection = self._create_collection()
        kanji1 = Kanji.objects.create(character='日',
                                      keyword='day',
                                      heisig_index=12)
        card1 = KanjiCard.objects.create(kanji=kanji1,
                                         mnemonic='midday sun',
                                         collection=collection)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        card1.next_review = tomorrow
        card1.save()
        self.assertEqual(collection.next_scheduled_card(), None)

    def test_cards_scored_lt_4_reviewed_last(self):
        collection = self._create_collection()
        kanji1 = Kanji.objects.create(character='日',
                                      keyword='day',
                                      heisig_index=12)
        kanji2 = Kanji.objects.create(character='月',
                                      keyword='month',
                                      heisig_index=13)
        KanjiCard.objects.create(kanji=kanji1,
                                 mnemonic='midday sun',
                                 collection=collection)
        KanjiCard.objects.create(kanji=kanji2,
                                 mnemonic='waxing moon',
                                 collection=collection)
        first_card = collection.next_scheduled_card()
        first_card.set_review_score(3)
        second_card = collection.next_scheduled_card()
        second_card.set_review_score(4)
        third_card = collection.next_scheduled_card()
        self.assertEqual(third_card, first_card)
