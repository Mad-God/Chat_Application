from email.message import Message
from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ChatGroup)
# admin.site.register(TextMessage)
admin.site.register(Member)

@admin.register(TextMessage)
class ratesAdmin(admin.ModelAdmin):
  list_display = ('id','sender', 'text', "group",'created_on')
  display = ('sender', 'text', "group",'created_on')