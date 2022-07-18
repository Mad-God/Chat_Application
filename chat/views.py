from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.views.generic import (
    View,
    CreateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
import pdb

# self imports

from chat.models import ChatGroup, TextMessage, Member
from base.models import User
from .forms import GroupForm, MessageForm
from .mixins import MemberRequiredMixin, AdminRequiredMixin, NotAdminMixin


# Create your views here.


class HomeView(View):
    """
    Shows all the available groups and creates new groups
    """
    template_name = "chat/home.html"

    def get_context_data(self, **kwargs):
        context = {}
        if self.request.user.is_authenticated:
            # breakpoint()
            context["joined_groups"] = ChatGroup.objects.annotate(mem_count = Count('members')).filter(members__user = self.request.user, members__accepted=True, mem_count__gt = 0)
            context["applied_groups"] = ChatGroup.objects.annotate(mem_count = Count('members')).filter(members__user = self.request.user, members__accepted=False, mem_count__gt = 0)
            context["other_groups"] = ChatGroup.objects.annotate(mem_count = Count('members')).exclude(members__user = self.request.user, members__gt = 0).filter(mem_count__gt = 0)
        else:
            context["other_groups"] = ChatGroup.objects.annotate(mem_count = Count('members')).filter(mem_count__gt = 0)
        context["users"] = User.objects.all()
        return context

    def get(self, request):
        context = self.get_context_data()
        context["form"] = GroupForm()

        return render(
            request, self.template_name, context
        )

    def post(self,*args,**kwargs): 
        form = GroupForm(self.request.POST)
        if form.is_valid():
            # chat_group = ChatGroup.objects.create(name=self.request.POST.get("name"), admin=self.request.user)
            chat_group = form.save(commit=False, user = self.request.user)
            # breakpoint()
            return redirect("chat:chat", name=chat_group.slug)
        return render(
        self.request, self.template_name,{"form":form})



class Lobby(MemberRequiredMixin, View):
    '''
    Get a few previous messages of the group and render the chat lobby
    '''

    def get(self, args, **kwargs):
        name = kwargs["name"]
        form = MessageForm()
        group = ChatGroup.objects.get(slug=name)
        admin = self.request.user in group.admin.all()
        members = Member.objects.filter(group=group, accepted=True)
        messages = TextMessage.objects.filter(group=group).order_by('-created_on')
        requested = None
        if admin:
            requested = Member.objects.filter(group=group, accepted=False)

        return render(self.request, 'chat/lobby.html', {"group":group, 'name':name, 'previous_messages':messages[:10], "members":members, "requests":requested, "admin":admin, "form":form})


 

class DirectLobby(LoginRequiredMixin, View):
    '''
    Get a few previous messages of the direct message conversation and render the chat lobby
    '''

    def get(self, args, **kwargs):
        uid = int(kwargs["user_id"])

        # create the sluug for the given DM pair slug
        form = MessageForm()
        if self.request.user.id < int(uid):
            slug = f"direct-{str(self.request.user.id)}-{str(uid)}"
            pass
        else:
            slug = f"direct-{str(uid)}-{str(self.request.user.id)}"
            pass
        group, _ = ChatGroup.objects.get_or_create(slug=slug, name=slug)
        # breakpoint()
        messages = TextMessage.objects.filter(group=group).order_by('-created_on')
        # messages = None
        return render(self.request, 'chat/lobby.html', {'group':group,'previous_messages':messages, "form":form})



class ApplyForMemberShip(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        Member.objects.create(user=self.request.user, group=ChatGroup.objects.get(slug=kwargs["name"]), accepted=False)
        return redirect("chat:home")


class AcceptMemberShip(AdminRequiredMixin, View):
    def get(self,*args,**kwargs):
        user_id = kwargs["user"]
        Member.objects.filter(user=User.objects.get(id=user_id), group=ChatGroup.objects.get(slug=kwargs["name"]), accepted = False).update(accepted=True)
        return redirect("chat:chat", name=kwargs["name"])


class DenyMemberShip(AdminRequiredMixin, View):
    def get(self,*args,**kwargs):
        user_id = kwargs["user"]
        Member.objects.filter(user=User.objects.get(id=user_id), group=ChatGroup.objects.get(slug=kwargs["name"]), accepted = False).delete()
        return redirect("chat:chat", name=kwargs["name"])


class RevokeMemberShip(NotAdminMixin, View):
    def get(self,*args,**kwargs):
        user_id = kwargs["user"]
        Member.objects.filter(user=User.objects.get(id=user_id), group=ChatGroup.objects.get(slug=kwargs["name"]), accepted=True).delete()
        return redirect("chat:chat", name=kwargs["name"])



class InviteMemberShip(LoginRequiredMixin, View):
    def dispatch(self, *args, **kwargs):
        user = self.request.user
        group = ChatGroup.objects.get(id=kwargs["group_id"])
        Member.objects.get_or_create(user=user, group=group, accepted = True)
        return redirect("chat:chat", name=group.slug)


