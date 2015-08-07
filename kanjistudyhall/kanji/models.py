import datetime

from django.conf import settings
from django.db import models


class Kanji(models.Model):
    """Represents a single Chinese character, with a unique keyword taken
    from Heisig's book. Keywords are not intended to be modified.
    Ditto for the heisig_index field, which inidicates the order in which
    Heisig introduces the characters.

    """
    character = models.CharField(max_length=1, unique=True)
    keyword = models.CharField(max_length=50, unique=True)
    heisig_index = models.PositiveIntegerField(unique=True)

    
class KanjiCardCollection(models.Model):
    """Represents a collection of KanjiCards for a given user.
    Users can have multiple collections, but a given Kanji should
    not be represented on more than one card per collection.
    Mnemonics should also be unique per collection.

    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=250)

    class Meta:
        unique_together = (('owner', 'name'),)

    def next_scheduled_card(self):
        """Find the next scheduled card.
        Save cards that were already reviewed today until last.

        """
        today = datetime.date.today()
        next_card = self.kanjicard_set.filter(
            next_review=today).order_by(
                '-last_missed', 'consecutive_correct', 'efactor'
            ).first()
        return next_card
        


class KanjiCard(models.Model):
    """Represents a single kanji flash card. Associates a kanji
    with a user-defined mnemonic. Also tracks state such as the
    most recent date reviewd, and how difficult it was for the user
    to recall.

    """
    collection = models.ForeignKey(KanjiCardCollection)
    kanji = models.ForeignKey(Kanji)
    mnemonic = models.TextField()
    total_reviews = models.PositiveIntegerField(default=0)
    consecutive_correct = models.PositiveIntegerField(default=0)
    last_reviewed = models.DateField(auto_now_add=True)
    last_missed = models.DateField(auto_now_add=True)
    next_review = models.DateField(auto_now_add=True)
    efactor = models.FloatField(default=2.5)

    class Meta:
        unique_together = (
            ('collection', 'kanji'),
            ('collection', 'mnemonic'),
        )

    def set_review_score(self, score):
        """Scores a card on a range of 0-5 and adjusts the review
        schedule accordingly.

        """
        if score not in range(0, 6):
            raise ValueError("Review Score must be between 0 and 5")
        self._calculate_next_review(score)

    def _calculate_next_review(self, score):
        """Adjusts the e-factor and the next scheduled review according
        to the SM2 algorithm.
        Algorithm described here: http://www.supermemo.com/english/ol/sm2.htm
        
        """
        today = datetime.date.today()
        self.last_reviewed = today
        new_total = self.total_reviews + 1
        self.total_reviews = new_total
        if score > 2:
            ef = self.efactor + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02))
            if ef < 1.3:
                ef = 1.3
            self.efactor = ef
            new_streak = self.consecutive_correct + 1
            self.consecutive_correct = new_streak
        else:
            self.consecutive_correct = 0
            self.last_missed = today
        if score < 4:
            self.next_review = today
        else:
            interval = 1
            if self.consecutive_correct == 2:
                interval = 6
            elif self.consecutive_correct > 2:
                interval = (self.consecutive_correct - 1) * self.efactor
            scheduled_review = today + datetime.timedelta(days=interval)
            self.next_review = scheduled_review
        self.save()
