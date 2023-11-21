from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncDay


class LikesManager(models.Manager):

    def test_aggregation(self, user):
        return (self.get_queryset().filter(user=user).annotate(day=TruncDay('created_at')).values('day').
                annotate(likes_count=Count('id')).order_by('day'))
