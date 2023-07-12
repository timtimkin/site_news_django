from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps


@receiver(post_save, sender='newspaperapp.Post')
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        Post = apps.get_model('newspaperapp', 'Post')
        instance.send_new_post_notification()
