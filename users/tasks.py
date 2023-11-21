import re

from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from django.core.cache import cache

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    user_namespace_keys = cache.iter_keys('user__*')
    user_model = get_user_model()
    instances_to_update = []

    for user_key in user_namespace_keys:
        user_id = re.sub(r'^user__', '', user_key)

        user = user_model.objects.get(pk=user_id)
        user.last_request_time = cache.get(user_key)

        instances_to_update.append(user)
        cache.delete(user_key)

    user_model.objects.bulk_update(instances_to_update, fields=['last_request_time'])

    logger.info('Cache has been cleared')
