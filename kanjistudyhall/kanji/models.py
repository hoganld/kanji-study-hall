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
    last_reviewed = models.DateTimeField(auto_now=True)
    last_missed = models.DateTimeField(auto_now=True)
    next_review = models.DateField(auto_now=True)
    efactor = models.FloatField(default=2.5)

    class Meta:
        unique_together = (
            ('collection', 'kanji'),
            ('collection', 'mnemonic'),
        )

    def set_review_score(self, score):
        if score not in range(0, 6):
            raise ValueError("Review Score must be between 0 and 5")
        new_total = self.total_reviews + 1
        self.total_reviews=new_total
        self.save()
