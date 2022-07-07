from django import forms
from .models import ChatGroup, Member, TextMessage
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin


class GroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ["name",]
    def save(self, user, commit=False, **kwargs):
        m = super(GroupForm, self).save()
        m.admin.add(user.id)
        Member.objects.create(group=m, user = user, accepted = True)
        return m


class MessageForm(forms.ModelForm):
    long_text = forms.CharField(widget=EmojiPickerTextareaAdmin)
    class Meta:
        model = TextMessage
        fields = []

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['long_text'].label = ""

 