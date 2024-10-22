from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def resize_avatar(sender, instance, **kwargs):
    if instance.avatar:
        img = Image.open(instance.avatar)
        img.thumbnail((200, 200), Image.ANTIALIAS)
        img.save(instance.avatar.path)