from django.db.models.signals import post_save
from django.dispatch import receiver
from redmine.models import RedmineGroup
from redmine.tasks import update_redmine_groups_data


@receiver(post_save, sender=RedmineGroup)
def update_redmine_data(sender, instance, created, **kwargs):
    if not instance.is_valid:
        update_redmine_groups_data.delay(groups_ids=[instance.group_id])
