from django.db import models
from base.models import User
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.utils.text import slugify  
from datetime import datetime 
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin


# Create your models here.


class ChatGroup(models.Model):
    admin = models.ManyToManyField(User, default = None,related_name="chat_groups")
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.name


class Member(models.Model):
    group = models.ForeignKey(
        "ChatGroup", on_delete=models.CASCADE, related_name="members"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member")
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + " enrolled " + str(self.group)


class TextMessage(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_messages",
    )
    text = models.CharField(max_length=500) 
    group = models.ForeignKey(
        ChatGroup, on_delete=models.CASCADE, related_name="messages"
    )
    created_on = models.DateTimeField(auto_now_add=True)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = ChatGroup.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s"%(slug, qs.first().id)
        return create_slug(instance, new_slug = new_slug)
    return slug

def pre_blog_created_signal(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    

pre_save.connect(pre_blog_created_signal, sender = ChatGroup)
