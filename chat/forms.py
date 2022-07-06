from django import forms
from .models import ChatGroup, Member


class GroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ["name",]
    def save(self, user, commit=False, **kwargs):
        m = super(GroupForm, self).save()
        m.admin.add(user.id)
        Member.objects.create(group=m, user = user, accepted = True)
        return m
