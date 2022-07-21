from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect, HttpResponse


# self imports
from .models import Member, ChatGroup
from base.models import User


class MemberRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return Member.objects.filter(
            user=self.request.user, group__slug=self.kwargs["name"], accepted = True
        ).exists()

    def handle_no_permission(self):
        return HttpResponse(
            "You are not a member of this group. Please apply for membership on homepage", status = 403
        )


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return ChatGroup.objects.filter(
            slug=self.kwargs["name"], admin=self.request.user
        ).exists()

    def handle_no_permission(self):
        return HttpResponse(
            "You are not an Admin of this group. Please Contact someone who is an Admin for this operation."
        )


class NotAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return not ChatGroup.objects.filter(
            slug=self.kwargs["name"], admin=User.objects.get(id=self.kwargs["user"])
        ).exists() and AdminRequiredMixin.test_func(self)

    def handle_no_permission(self):
        return HttpResponse(
            "The requested operation can't be performed on an Admin user"
        )

