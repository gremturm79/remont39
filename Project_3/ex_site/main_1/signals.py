from django.dispatch import receiver
from django.core.signals import request_finished
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import ProfileUser, Review


@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")


@receiver(post_save, sender=User)
def create_profile_user(sender, instance, created, **kwargs):
    if created:
        ProfileUser.objects.create(owner=instance)


@receiver(post_save, sender=User)
def save_review_user(sender, instance, **kwargs):
    instance.profileuser.save()



